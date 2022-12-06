from flask import Flask, request, render_template
from forms import BlogForm, SplitDataForm
from utils import compare_data, split_url_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/', methods=['POST', 'GET'])
def check_text():
    """
    Match Sequence Endpoint.

    :return: Template
    """
    form = BlogForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flag, blog_string, jidipi_string = compare_data.get_urls(form.blog_url.data, form.jidipi_url.data)
            return render_template('index.html', form=form, flag=flag, blog_string=blog_string,
                                   jidipi_string=jidipi_string)
    return render_template('index.html', form=form)


@app.route('/split-data', methods=['POST', 'GET'])
def split_data():
    """
    Split data into chunks

    :return: Template
    """
    form = SplitDataForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            status, data_lst, max_data = split_url_data.get_data_to_split(form.blog_url.data, form.data_split_num.data)
            return render_template('split_blog_data.html', form=form, status=status, data_lst=data_lst,
                                   max_data=max_data)
    return render_template('split_blog_data.html', form=form)


@app.route('/split-data_by_parts', methods=['POST', 'GET'])
def split_data_by_parts():
    """
    Split data into chunks

    :return: Template
    """
    form = SplitDataForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            status, data_lst, max_data = split_url_data.get_data_to_split(form.blog_url.data, form.data_split_num.data)
            return render_template('split_blog_data.html', form=form, status=status, data_lst=data_lst,
                                   max_data=max_data)
    return render_template('split_blog_data.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
