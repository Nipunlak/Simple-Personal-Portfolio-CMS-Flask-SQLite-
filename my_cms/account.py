from flask import (request, redirect, render_template, g, Blueprint, flash)

from .auth import login_required
from .db import get_db

bp = Blueprint('account',__name__)


@bp.route('/my_dashboard', methods = ('GET', 'POST'))
@login_required
def dashboard():
    if request.method == "POST":
        pass

    return render_template('account/user_dashboard.html')
