from flask import Blueprint,render_template,url_for

bp = Blueprint('map', __name__, url_prefix='/map')

@bp.route('/')
def map():
    return render_template('map/map.html')