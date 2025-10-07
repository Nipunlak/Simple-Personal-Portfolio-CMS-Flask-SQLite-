from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    abort,
)

from .db import get_db
from .auth import login_required


bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/allposts")
def index():
    db = get_db()
    posts = db.execute("SELECT * FROM post").fetchall()

    return render_template("blog/index.html", posts=posts)


@bp.route("/newpost", methods=("GET", "POST"))
@login_required
def newpost():
    if request.method == "POST":
        post_name = request.form["post_name"]
        post_text = request.form["post_text"]
        image_path = request.form["image_path"]

        author_id = g.get("user_id", None)
        db = get_db()
        error = None

        if not post_name:
            error = "Name is required"

        if not post_text:
            error = "Post Text is required"

        if not image_path:
            error = "Image is required"

        if error is None and author_id is not None:
            try:
                db.execute(
                    "INSERT INTO post (post_name,post_text,author_id,image_path) VALUES (?,?,?,?)",
                    (post_name, post_text, author_id, image_path),
                )
                db.commit()

            except db.IntegrityError:
                error = "Post Name Already exist"

            except Exception:
                error = "Post creation failed"
            else:
                return redirect(url_for("blog.index"))

        flash(error)
        return redirect(url_for("blog.newpost"))

    return render_template("blog/newpost.html")


@bp.route("/posts/<int:id>")
def get_post(id):
    db = get_db()
    post = db.execute("SELECT * FROM post WHERE id = ?", (id,)).fetchone()

    if post is None:
        abort(404, "Not Found")

    return render_template("blog/post.html", post=post)


@bp.route("/posts/<int:id>/update", methods=("GET", "POST"))
@login_required
def post_update(id):
    if request.method == "POST":

        allowed_feilds = ["post_name", "post_text", "image_path"]
        inputs = request.form.to_dict()

        updates = {
            key: value
            for key, value in inputs.items()
            if key in allowed_feilds and value.strip() != ""
        }

        error = None

        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = ?", (id,)).fetchone()

        if post is None:
            abort(404, "Not Found")

        if g.get("user_id") != post["author_id"]:

            abort(401, "Unauthorized")

        if not updates:
            error = "Please Provie values for updation"

        if error is None:

            fields = [f"{key} = ?" for key in updates.keys()]
            fields_str = ", ".join(fields)

            values = list(updates.values())
            values.append(post["id"])

            sql_query = f"UPDATE post SET {fields_str} WHERE id = ?"

            try:
                db.execute(sql_query, tuple(values))
                db.commit()
                return redirect(url_for("blog.get_post", id=id))
            except Exception as err:
                db.rollback()
                error = err

        flash(error)
        return redirect(url_for("blog.post_update", id=id))

    else:
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = ?", (id,)).fetchone()

        return render_template("blog/postupdate.html", post=post)


@bp.route("/post/<int:id>/delete", methods=("GET", "POST"))
@login_required
def post_delete(id):
    if request.method == "POST":
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = ?", (id,)).fetchone()

        if post is None:
            abort(404, "Not Found")

        if post["author_id"] != g.get("user_id"):
            abort(401, "Unauthorized")

        try:
            db.execute("DELETE FROM post WHERE id = ?", (post["id"],))
            db.commit()
            return redirect(url_for("blog.index"))
        except Exception as error:
            db.rollback()
            flash(error)
            return redirect(url_for("blog.get_post", id=id))
