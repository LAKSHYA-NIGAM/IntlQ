/* ═══════════════════════════════════════════════════════════════════════════
   IntlQ — AI Proctoring Engine
   Camera monitoring, gaze detection, tab-switch warnings, screen sharing
   ═══════════════════════════════════════════════════════════════════════════ */

const Proctor = {
    sessionId: null,
    warningCount: 0,
    maxWarnings: 5,
    gazeViolationStreak: 0,
    gazeThreshold: 8,    // consecutive gaze violations before warning (~24s at 3s interval)
    cameraDenied: false,
    cameraStream: null,
    screenStream: null,
    detectionInterval: null,
    isActive: false,
    modelsLoaded: false,
    gracePeriodOver: false,

    // ── Initialize ──────────────────────────────────────────────────────────
    async init(sessionId) {
        this.sessionId = sessionId;
        this.isActive = true;

        // Tab switch detection
        this._onVisChange = () => this.onVisibilityChange();
        this._onBlur = () => this.onWindowBlur();
        document.addEventListener('visibilitychange', this._onVisChange);
        window.addEventListener('blur', this._onBlur);

        // Start camera
        await this.startCamera();

        // Attempt screen share (non-blocking)
        this.startScreenShare();

        // Start gaze detection after face-api loads (with grace period)
        if (typeof faceapi !== 'undefined') {
            await this.loadFaceModels();
            // Give user 15 seconds to settle before starting gaze checks
            setTimeout(() => {
                this.gracePeriodOver = true;
                // Start gaze detection even if camera denied — it will count violations
                if (this.modelsLoaded || this.cameraDenied) {
                    this.startGazeDetection();
                }
            }, 15000);
        }
    },

    // ═══════════════════════════════════════════════════════════════════════
    // TAB-SWITCH DETECTION
    // ═══════════════════════════════════════════════════════════════════════

    onVisibilityChange() {
        if (!this.isActive) return;
        if (document.hidden) {
            this.addWarning('tab_switch', 'You switched away from the interview tab.');
        }
    },

    onWindowBlur() {
        if (!this.isActive) return;
        // Small delay to avoid false positives from permission dialogs
        setTimeout(() => {
            if (document.hidden && this.isActive) {
                // Already handled by visibilitychange
            }
        }, 300);
    },

    addWarning(type, message) {
        this.warningCount++;

        // Log violation to server
        fetch('/api/proctor/violation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: this.sessionId, violation_type: type }),
        }).catch(() => { });

        // Update UI counter
        const counter = document.getElementById('violation-count');
        if (counter) counter.textContent = this.warningCount;

        if (this.warningCount >= this.maxWarnings) {
            this.terminateSession();
        } else {
            this.showWarningOverlay(message, this.warningCount);
        }
    },

    showWarningOverlay(message, count) {
        const overlay = document.getElementById('proctor-warning-overlay');
        const msg = document.getElementById('proctor-warning-message');
        const cnt = document.getElementById('proctor-warning-count');
        if (overlay && msg && cnt) {
            msg.textContent = message;
            cnt.textContent = `Warning ${count} of ${this.maxWarnings}`;
            overlay.classList.add('visible');
            setTimeout(() => overlay.classList.remove('visible'), 4000);
        }
    },

    async terminateSession() {
        this.isActive = false;
        this.cleanup();

        // Notify server
        await fetch('/api/proctor/terminate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: this.sessionId }),
        }).catch(() => { });

        // Show termination overlay
        const overlay = document.getElementById('proctor-warning-overlay');
        const msg = document.getElementById('proctor-warning-message');
        const cnt = document.getElementById('proctor-warning-count');
        if (overlay && msg && cnt) {
            msg.textContent = 'Interview terminated due to repeated violations.';
            cnt.textContent = 'Session Ended';
            overlay.classList.add('visible', 'terminated');
        }

        // Redirect after delay
        setTimeout(() => {
            window.location.href = `/results/${this.sessionId}`;
        }, 3000);
    },

    // ═══════════════════════════════════════════════════════════════════════
    // CAMERA MONITORING
    // ═══════════════════════════════════════════════════════════════════════

    async startCamera() {
        try {
            this.cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 320, height: 240, facingMode: 'user' },
                audio: false,
            });

            // Detect when camera stream is stopped or disabled
            const track = this.cameraStream.getVideoTracks()[0];
            if (track) {
                track.addEventListener('ended', () => this.handleCameraStop());
            }

            const video = document.getElementById('proctor-camera');
            if (video) {
                video.srcObject = this.cameraStream;
                video.play();
            }
            const panel = document.getElementById('proctor-camera-panel');
            if (panel) panel.classList.add('active');
        } catch (err) {
            console.warn('Camera access denied:', err);
            this.cameraDenied = true;
            this.blockUIForCamera('Camera access is required for proctoring. Please allow camera permissions to continue.');
            setTimeout(() => {
                this.terminateSession();
            }, 3000);
        }
    },

    // ═══════════════════════════════════════════════════════════════════════
    // SCREEN SHARING
    // ═══════════════════════════════════════════════════════════════════════

    async startScreenShare() {
        try {
            this.screenStream = await navigator.mediaDevices.getDisplayMedia({
                video: { cursor: 'always' },
                audio: false,
            });

            const preview = document.getElementById('proctor-screen-preview');
            if (preview) {
                preview.srcObject = this.screenStream;
                preview.play();
            }

            const panel = document.getElementById('proctor-screen-panel');
            if (panel) panel.classList.add('active');

            // Detect when user stops sharing
            this.screenStream.getVideoTracks()[0].addEventListener('ended', () => {
                if (this.isActive) {
                    this.addWarning('tab_switch', 'Screen sharing was stopped.');
                    if (panel) panel.classList.remove('active');
                }
            });
        } catch (err) {
            console.warn('Screen share declined:', err);
        }
    },

    // ═══════════════════════════════════════════════════════════════════════
    // GAZE / FACE DETECTION
    // ═══════════════════════════════════════════════════════════════════════

    async loadFaceModels() {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.7.12/model/';
        try {
            await Promise.all([
                faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
                faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL),
            ]);
            this.modelsLoaded = true;
        } catch (err) {
            console.warn('Face detection models failed to load — gaze proctoring disabled:', err);
            this.modelsLoaded = false;
        }
    },

    startGazeDetection() {
        const video = document.getElementById('proctor-camera');
        // Allow starting even without models if camera is denied (to count violations)
        if (!video && !this.cameraDenied) return;
        if (!this.modelsLoaded && !this.cameraDenied) return;

        this.detectionInterval = setInterval(async () => {
            if (!this.isActive || !this.gracePeriodOver) return;

            // If camera was denied or video isn't playing, count as face not detected
            if (this.cameraDenied || !video || video.paused || video.ended || !video.srcObject) {
                this.gazeViolationStreak++;
                const indicator = document.getElementById('gaze-indicator');
                if (indicator) {
                    indicator.textContent = '⚠️ Camera off — Face not detected';
                    indicator.className = 'gaze-indicator warning';
                }

                if (this.gazeViolationStreak >= this.gazeThreshold) {
                    this.gazeViolationStreak = 0;
                    this.addWarning('gaze', 'Face not detected — camera may be off or covered.');
                }
                return;
            }

            try {
                const detection = await faceapi
                    .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions({ scoreThreshold: 0.3 }))
                    .withFaceLandmarks(true);

                const indicator = document.getElementById('gaze-indicator');

                if (!detection) {
                    // No face detected — increment violation streak
                    this.gazeViolationStreak++;
                    if (indicator) {
                        indicator.textContent = '⚠️ Face not detected';
                        indicator.className = 'gaze-indicator warning';
                    }
                } else {
                    // Check if face is centered (using nose position relative to bounding box)
                    const box = detection.detection.box;
                    const nose = detection.landmarks.getNose();
                    const noseTip = nose[3]; // tip of nose
                    const centerX = box.x + box.width / 2;
                    const deviation = Math.abs(noseTip.x - centerX) / box.width;

                    if (deviation > 0.45) {
                        // Face turned significantly — more lenient threshold
                        this.gazeViolationStreak++;
                        if (indicator) {
                            indicator.textContent = '⚠️ Please look at the screen';
                            indicator.className = 'gaze-indicator warning';
                        }
                    } else {
                        // Reset streak — face looks fine
                        this.gazeViolationStreak = Math.max(0, this.gazeViolationStreak - 2);
                        if (indicator) {
                            indicator.textContent = '✅ Monitoring';
                            indicator.className = 'gaze-indicator ok';
                        }
                    }
                }

                // Sustained gaze violations trigger a warning
                if (this.gazeViolationStreak >= this.gazeThreshold) {
                    this.gazeViolationStreak = 0;
                    this.addWarning('gaze', 'Looking away from the screen detected.');
                }
            } catch (err) {
                // Silent fail for detection errors
            }
        }, 3000);
    },

    handleCameraStop() {
        if (this.isActive) {
            this.cameraDenied = true;
            this.blockUIForCamera('Camera was turned off. Camera access is required to continue the interview.');
            setTimeout(() => {
                this.terminateSession();
            }, 3000);
        }
    },

    blockUIForCamera(message) {
        const overlay = document.getElementById('proctor-warning-overlay');
        const msg = document.getElementById('proctor-warning-message');
        const cnt = document.getElementById('proctor-warning-count');
        if (overlay && msg && cnt) {
            msg.textContent = message;
            cnt.textContent = 'Camera Blocked';
            overlay.classList.add('visible', 'terminated');
        }
        // Disable inputs
        const textarea = document.getElementById('answer-input');
        if (textarea) textarea.disabled = true;
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn) submitBtn.disabled = true;
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) voiceBtn.disabled = true;
    },

    // ═══════════════════════════════════════════════════════════════════════
    // CLEANUP
    // ═══════════════════════════════════════════════════════════════════════

    cleanup() {
        if (this.detectionInterval) clearInterval(this.detectionInterval);
        if (this.cameraStream) this.cameraStream.getTracks().forEach(t => t.stop());
        if (this.screenStream) this.screenStream.getTracks().forEach(t => t.stop());
        if (this._onVisChange) document.removeEventListener('visibilitychange', this._onVisChange);
        if (this._onBlur) window.removeEventListener('blur', this._onBlur);
    },
};
