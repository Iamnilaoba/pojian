from flask import Blueprint
from flask import render_template

bp=Blueprint('font',__name__)


@bp.route('/')
def loginView():
    return render_template('front/index.html')


