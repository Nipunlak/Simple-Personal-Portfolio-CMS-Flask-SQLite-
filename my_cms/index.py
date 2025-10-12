from flask import (g, redirect, render_template, flash, Blueprint, request)


bp = Blueprint("main",__name__)

@bp.route('/')
def index():
    return render_template("main/index.html")