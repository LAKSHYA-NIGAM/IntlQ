"""
API Routes
Flask Blueprint with all application endpoints.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from api.schemas import StartInterviewRequest, SubmitAnswerRequest
from config.settings import load_roles_config
from core.interview_engine import get_questions, get_question_by_id
from core.evaluator import evaluate
from core.scoring import calculate_score
from core.feedback_engine import generate_feedback
from database.crud import (
    create_session,
    create_user,
    get_session,
    complete_session,
    save_answer,
    get_session_results,
    get_session_answers,
    get_user_sessions,
    get_user_by_username,
    get_user_by_email,
    record_violation,
    terminate_session,
)

api_bp = Blueprint("api", __name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTH ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@api_bp.route("/login", methods=["GET", "POST"])
def login_page():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("api.index"))
        else:
            return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


@api_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    """Signup page."""
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            return render_template("signup.html", error="All fields are required.")
        if len(username) < 3:
            return render_template("signup.html", error="Username must be at least 3 characters.")
        if len(password) < 6:
            return render_template("signup.html", error="Password must be at least 6 characters.")
        if password != confirm:
            return render_template("signup.html", error="Passwords do not match.")
        if get_user_by_username(username):
            return render_template("signup.html", error="Username already taken.")
        if get_user_by_email(email):
            return render_template("signup.html", error="Email already registered.")

        user = create_user(username, email, password)
        login_user(user, remember=True)
        return redirect(url_for("api.index"))

    return render_template("signup.html")


@api_bp.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("api.login_page"))


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTES (serve HTML templates)
# ═══════════════════════════════════════════════════════════════════════════════

@api_bp.route("/")
@login_required
def index():
    """Landing page — role selection."""
    config = load_roles_config()
    roles = config.get("roles", [])
    topics = config.get("topics", [])
    return render_template("index.html", roles=roles, topics=topics)


@api_bp.route("/interview/<int:session_id>")
@login_required
def interview_page(session_id):
    """Interview session page."""
    session = get_session(session_id)
    if not session:
        return render_template("index.html", error="Session not found.", roles=load_roles_config().get("roles", [])), 404
    return render_template("interview.html", session=session)


@api_bp.route("/history")
@login_required
def history_page():
    """Past performances — list user's interview sessions."""
    sessions = get_user_sessions(current_user.id)
    return render_template("history.html", sessions=sessions)


@api_bp.route("/results/<int:session_id>")
@login_required
def results_page(session_id):
    """Results / performance dashboard page."""
    results = get_session_results(session_id)
    if not results:
        return render_template("index.html", error="Session not found.", roles=load_roles_config().get("roles", [])), 404
    return render_template("results.html", results=results)


# ═══════════════════════════════════════════════════════════════════════════════
#  API ENDPOINTS (JSON)
# ═══════════════════════════════════════════════════════════════════════════════

@api_bp.route("/api/roles", methods=["GET"])
def get_roles():
    """List available interview roles."""
    roles = load_roles_config().get("roles", [])
    return jsonify({"roles": roles})


@api_bp.route("/api/start", methods=["POST"])
@login_required
def start_interview():
    """Start a new interview session."""
    try:
        data = StartInterviewRequest(**request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Generate questions
    try:
        questions = get_questions(
            role_id=data.role_id,
            difficulty=data.difficulty,
            count=data.question_count,
        )
    except FileNotFoundError:
        return jsonify({"error": f"No questions found for role '{data.role_id}'."}), 404

    if not questions:
        return jsonify({"error": f"No questions found for role '{data.role_id}'."}), 404

    question_ids = [q["id"] for q in questions]

    # Create session in DB
    session = create_session(
        candidate_name=data.candidate_name,
        role_id=data.role_id,
        difficulty=data.difficulty,
        question_ids=question_ids,
        user_id=current_user.id,
    )

    return jsonify({
        "session_id": session.id,
        "role_id": session.role_id,
        "candidate_name": session.candidate_name,
        "question_count": len(questions),
        "questions": questions,
        "redirect_url": f"/interview/{session.id}",
    }), 201


@api_bp.route("/api/questions/<int:session_id>", methods=["GET"])
@login_required
def get_session_questions(session_id):
    """Get the questions for an existing session."""
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    question_ids = session.question_ids
    questions = []
    for qid in question_ids:
        q = get_question_by_id(session.role_id, qid)
        if q:
            questions.append(q)

    # Also return which questions are already answered
    answered = get_session_answers(session_id)
    answered_ids = [a.question_id for a in answered]

    return jsonify({
        "session_id": session_id,
        "role_id": session.role_id,
        "questions": questions,
        "answered_ids": answered_ids,
    })


@api_bp.route("/api/submit", methods=["POST"])
@login_required
def submit_answer():
    """Submit an answer for evaluation."""
    try:
        data = SubmitAnswerRequest(**request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    session = get_session(data.session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    # Check if session was terminated
    if session.terminated:
        return jsonify({"error": "This session has been terminated due to proctoring violations."}), 403

    # Get question text
    question = get_question_by_id(session.role_id, data.question_id)
    question_text = question["text"] if question else ""

    # ── Evaluate ─────────────────────────────────────────────────────────
    eval_result = evaluate(data.question_id, data.answer_text)
    score_result = calculate_score(eval_result["similarity_score"], eval_result["keyword_coverage"])
    feedback_result = generate_feedback(eval_result, score_result)

    # ── Save to DB ───────────────────────────────────────────────────────
    save_answer(
        session_id=data.session_id,
        question_id=data.question_id,
        question_text=question_text,
        answer_text=data.answer_text,
        similarity_score=eval_result["similarity_score"],
        keyword_score=eval_result["keyword_coverage"],
        total_score=score_result["total_score"],
        grade=score_result["grade"],
        feedback=feedback_result,
    )

    # Check if interview is complete
    answered = get_session_answers(data.session_id)
    answered_ids = [a.question_id for a in answered]
    is_complete = len(answered_ids) >= session.question_count

    if is_complete:
        # Calculate overall score
        all_scores = [a.total_score for a in answered]
        avg_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
        # Determine overall grade
        overall_grade_result = calculate_score(avg_score / 100, avg_score / 100)
        complete_session(data.session_id, avg_score, overall_grade_result["grade"])

    return jsonify({
        "question_id": data.question_id,
        "evaluation": eval_result,
        "score": score_result,
        "feedback": feedback_result,
        "is_complete": is_complete,
        "results_url": f"/results/{data.session_id}" if is_complete else None,
    })


@api_bp.route("/api/results/<int:session_id>", methods=["GET"])
@login_required
def api_results(session_id):
    """Get complete session results as JSON."""
    results = get_session_results(session_id)
    if not results:
        return jsonify({"error": "Session not found."}), 404
    return jsonify(results)


@api_bp.route("/api/sessions", methods=["GET"])
@login_required
def list_sessions():
    """List current user's interview sessions."""
    sessions = get_user_sessions(current_user.id)
    return jsonify({
        "sessions": [
            {
                "id": s.id,
                "candidate_name": s.candidate_name,
                "role_id": s.role_id,
                "overall_score": s.overall_score,
                "overall_grade": s.overall_grade,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            }
            for s in sessions
        ]
    })


# ═══════════════════════════════════════════════════════════════════════════════
#  PROCTORING ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@api_bp.route("/api/proctor/violation", methods=["POST"])
@login_required
def proctor_violation():
    """Log a proctoring violation."""
    data = request.get_json()
    session_id = data.get("session_id")
    violation_type = data.get("violation_type", "tab_switch")

    session = record_violation(session_id, violation_type)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    return jsonify({
        "tab_violations": session.tab_violations or 0,
        "gaze_violations": session.gaze_violations or 0,
    })


@api_bp.route("/api/proctor/terminate", methods=["POST"])
@login_required
def proctor_terminate():
    """Terminate a session due to proctoring violations."""
    data = request.get_json()
    session_id = data.get("session_id")

    session = terminate_session(session_id)
    if not session:
        return jsonify({"error": "Session not found."}), 404

    return jsonify({"terminated": True, "redirect_url": f"/results/{session_id}"})
