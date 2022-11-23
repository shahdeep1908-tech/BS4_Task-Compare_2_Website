from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import InputRequired


class BlogForm(FlaskForm):
    blog_url = URLField('blog_url', validators=[InputRequired()])
    jidipi_url = URLField('jidipi_url', validators=[InputRequired()])
