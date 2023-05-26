from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, TextAreaField, SubmitField


class create_post(FlaskForm):
    Title = StringField("Title", validators=[DataRequired()])
    Content = TextAreaField("Content", validators=[DataRequired()])
    Submit = SubmitField("Post")


class postForm(FlaskForm):
    Title = StringField("Title", validators=[DataRequired()])
    Content = TextAreaField("Content", validators=[DataRequired()])
    Submit = SubmitField("Post")
