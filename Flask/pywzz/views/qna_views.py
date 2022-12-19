from flask import Blueprint, render_template
from pywzz.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/')
def Question():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)
    # return redirect(url_for('auth.login'))
