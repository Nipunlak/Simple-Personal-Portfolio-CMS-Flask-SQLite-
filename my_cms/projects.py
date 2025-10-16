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


bp = Blueprint("project", __name__, url_prefix="/project")


@bp.route("/allprojects")
def index():
    db = get_db()
    projects = db.execute("SELECT * FROM project").fetchall()
    
   
    

    return render_template("project/index.html", projects=projects)


@bp.route("/newproject", methods=("GET", "POST"))
@login_required
def newproject():
    if request.method == "POST":
        project_name = request.form.get("project_name")
        description = request.form.get("description")
        image_path = request.form.get("image_path")

        author_id = g.get("user", None)['id']
        db = get_db()
        error = None

        if not project_name:
            error = "Name is required"

        if not description:
            error = "project description is required"

        if not image_path:
            error = "Image is required"

        if error is None and author_id is not None:
            try:
                db.execute(
                    "INSERT INTO project (project_name,description,author_id,image_path) VALUES (?,?,?,?)",
                    (project_name, description, author_id, image_path),
                )
                db.commit()

            except db.IntegrityError:
                error = "Project Name Already exist"

            except Exception:
                error = "Project creation failed"
            else:
                return redirect(url_for("project.index"))
        else:
            flash(error)
            return redirect(url_for("project.newproject"))

    return render_template("project/newproject.html")


@bp.route("/projects/<int:id>", methods=("GET", "POST"))
def get_project(id):
    if request.method == "GET":
        db = get_db()
        project = db.execute("SELECT * FROM project WHERE id = ?", (id,)).fetchone()

        if project is None:
            abort(404, "Not Found")

    return render_template("project/project.html", project=project)


@bp.route("/projects/<int:id>/update", methods=("GET", "POST"))
@login_required
def project_update(id):
    if request.method == "POST":

        allowed_feilds = ["project_name", "description", "image_path"]
        inputs = request.form.to_dict()

        updates = {
            key: value
            for key, value in inputs.items()
            if key in allowed_feilds and value.strip() != ""
        }

        error = None

        db = get_db()
        project = db.execute("SELECT * FROM project WHERE id = ?", (id,)).fetchone()

        if project is None:
            abort(404, "Not Found")

        if g.get("user")['id'] != project["author_id"]:

            abort(401, "Unauthorized")

        if not updates:
            error = "Please Provie values for updation"

        if error is None:

            fields = [f"{key} = ?" for key in updates.keys()]
            fields_str = ", ".join(fields)

            values = list(updates.values())
            values.append(project["id"])

            sql_query = f"UPDATE project SET {fields_str} WHERE id = ?"

            try:
                db.execute(sql_query, tuple(values))
                db.commit()
            except Exception as err:
                db.rollback()
                error = err

            else:
                return redirect(url_for("project.get_project", id=id))

        flash(error)
        return redirect(url_for("project.project_update", id=id))

    else:
        db = get_db()
        project = db.execute("SELECT * FROM project WHERE id = ?", (id,)).fetchone()

        return render_template("project/projectupdate.html", project=project)


@bp.route("/project/<int:id>/delete", methods=("GET", "POST"))
@login_required
def project_delete(id):
    if request.method == "POST":
        db = get_db()
        project = db.execute("SELECT * FROM project WHERE id = ?", (id,)).fetchone()

        if project is None:
            abort(404, "Not Found")

        if project["author_id"] != g.get("user")['id']:
            abort(401, "Unauthorized")

        try:
            db.execute("DELETE FROM project WHERE id = ?", (project["id"]))
            db.commit()
            return redirect(url_for("project.index"))
        except Exception as error:
            db.rollback()
            flash(error)
            return redirect(url_for("project.getproject", id=id))
