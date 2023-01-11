from flask_wtf import FlaskForm
from wtforms import URLField, DecimalField
from wtforms.validators import InputRequired


class BlogForm(FlaskForm):
    """
    Form for URL Inputs.

    blog_url: URL from where the data comes.
    jidipi_url: URL for which data needs to be checked.
    """
    blog_url = URLField('blog_url', validators=[InputRequired()])
    jidipi_url = URLField('jidipi_url', render_kw={"placeholder": "Enter System JIDIPI URL"})
    arch_jidipi_url = URLField('arch_jidipi_url',
                               render_kw={"placeholder": "Enter Architectures JIDIPI URL"})


class SplitDataForm(FlaskForm):
    """
    Form for Slicing Data Inputs

    blog_url: URL from where the data comes.
    data_split_num: No of chunks required
    """
    blog_url = URLField('blog_url', validators=[InputRequired()])
    data_split_num = DecimalField('data_split_num', validators=[InputRequired()])


class CheckDataDivisionURL(FlaskForm):
    blog_url = URLField('blog_url', validators=[InputRequired()])


class DataDivisonForm(FlaskForm):
    """
        Form for Slicing Data Inputs

        data_division_num: No of chunks required
        """
    data_division_num = DecimalField('data_division_num', validators=[InputRequired()],
                                     render_kw={"id": "data_division_num",
                                                "placeholder": "Number of sentences you want!"})
