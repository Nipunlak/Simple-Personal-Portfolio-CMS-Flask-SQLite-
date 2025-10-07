import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


from werkzeug.security import check_password_hash, generate_password_hash

from email_validator import validate_email, EmailNotValidError


from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute("SELECT * FROM USER WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kargs)
    return wrapped_view


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        image_path = request.form["image_path"]

        db = get_db()
        error = None

        if not email:
            error = "Email is Required."
        else:
            try:
                validate_email(email)
            except EmailNotValidError as err:
                error = err

        if not username:
            error = "User name is required."

        if not password:
            error = "Please Provide a Password."

        if not role:
            error = "Please Provide a Role"

        if not image_path:
            image_path = None

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username,email,password,role,image_path) VALUES (?,?,?,?,?)",
                    (
                        username,
                        email,
                        generate_password_hash(password),
                        role,
                        image_path,
                    ),
                )
                db.commit()
            except db.IntegrityError as error:
                error = "User Already exist"

            except Exception as err:
                error = err

            else:
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        error = None

        if not email:
            error = "Email is Required"

        if not password:
            error = "Password is Required"

        user = db.execute("SELECT * FROM USER WHERE email = ?", (email,)).fetchone()

        if user is None:

            error = "Invalid credentials"
        elif not check_password_hash(user["password"], password):

            error = "Invalid credentials"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("auth/login.html")


bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
