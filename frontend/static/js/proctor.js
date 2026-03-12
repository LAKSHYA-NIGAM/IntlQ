/* ═══════════════════════════════════════════════════════════════════════════
   IntlQ — AI Proctoring Engine
   Camera monitoring, gaze detection, tab-switch warnings, screen sharing
   ═══════════════════════════════════════════════════════════════════════════ */

const Proctor = {
    sessionId: null,
    warningCount: 0,
    maxWarnings: 3,
    gazeViolationStreak: 0,
    gazeThreshold: 5,   // consecutive gaze violations before warning
    cameraStream: null,
    screenStream: null,
    detectionInterval: null,
    isActive: false,

    // ── Initialize ──────────────────────────────────────────────────────────
    async init(sessionId) {
        this.sessionId = sessionId;
        this.isActive = true;

        // Tab switch detection
        document.addEventListener('visibilitychange', () => this.onVisibilityChange());
        window.addEventListener('blur', () => this.onWindowBlur());

        // Start camera
        await this.startCamera();

        // Attempt screen share (non-blocking)
        this.startScreenShare();

        // Start gaze detection after face-api loads
        if (typeof faceapi !== 'undefined') {
            await this.loadFaceModels();
            this.startGazeDetection();
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
            const video = document.getElementById('proctor-camera');
            if (video) {
                video.srcObject = this.cameraStream;
                video.play();
            }
            const panel = document.getElementById('proctor-camera-panel');
            if (panel) panel.classList.add('active');
        } catch (err) {
            console.warn('Camera access denied:', err);
            const panel = document.getElementById('proctor-camera-panel');
            if (panel) {
                panel.classList.add('active', 'denied');
                panel.innerHTML = '<div class="camera-denied">📷 Camera access required</div>';
            }
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
        } catch (err) {
            console.warn('Face detection models failed to load:', err);
        }
    },

    startGazeDetection() {
        const video = document.getElementById('proctor-camera');
        if (!video) return;

        this.detectionInterval = setInterval(async () => {
            if (!this.isActive || video.paused || video.ended) return;

            try {
                const detection = await faceapi
                    .detectSingleFace(video, new faceapi.TinyFaceDetectorOptions({ scoreThreshold: 0.4 }))
                    .withFaceLandmarks(true);

                const indicator = document.getElementById('gaze-indicator');

                if (!detection) {
                    // No face detected
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

                    if (deviation > 0.35) {
                        // Face turned significantly
                        this.gazeViolationStreak++;
                        if (indicator) {
                            indicator.textContent = '⚠️ Please look at the screen';
                            indicator.className = 'gaze-indicator warning';
                        }
                    } else {
                        this.gazeViolationStreak = 0;
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
        }, 2500);
    },

    // ═══════════════════════════════════════════════════════════════════════
    // CLEANUP
    // ═══════════════════════════════════════════════════════════════════════

    cleanup() {
        if (this.detectionInterval) clearInterval(this.detectionInterval);
        if (this.cameraStream) this.cameraStream.getTracks().forEach(t => t.stop());
        if (this.screenStream) this.screenStream.getTracks().forEach(t => t.stop());
    },
};
