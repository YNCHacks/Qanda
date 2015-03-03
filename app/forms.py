from flask.ext.wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import Question

class AnswerForm(Form):
    answer = TextAreaField("answer", validators=[Length(min=0, max=1023)])
