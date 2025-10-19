from flask import g, redirect, render_template, flash, Blueprint, request
from .db import get_db


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # fix permisson only admin can register a user.
    # disply news three project and post in the index page.
    # give user the ablity to change the hero image and the text in it.
    db = get_db()
    latest_three_posts = db.execute(
        "SELECT  * FROM post ORDER BY time_stamp DESC"
    ).fetchmany(3)

    latest_three_projects = db.execute(
        "SELECT  * FROM project ORDER BY time_stamp DESC"
    ).fetchmany(3)
    return render_template(
        "main/index.html",
        latest_posts=latest_three_posts,
        latest_projects=latest_three_projects,
    )
