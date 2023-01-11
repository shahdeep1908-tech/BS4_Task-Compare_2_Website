import json
import re

from flask import Flask, request, render_template, jsonify
from forms import BlogForm, SplitDataForm, DataDivisonForm, CheckDataDivisionURL
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
            blog_data = form.blog_url.data
            system_jidipi_data = form.jidipi_url.data
            arch_jidipi_data = form.arch_jidipi_url.data
            if not system_jidipi_data and not arch_jidipi_data:
                return render_template('index.html', form=form, jidipi_error='This field is required.')
            elif system_jidipi_data:
                flag, blog_string, jidipi_string = compare_data.get_urls(form.blog_url.data, system_jidipi_data, '')
                return render_template('index.html', form=form, flag=flag,
                                       blog_string=' '.join(blog_string.splitlines()),
                                       jidipi_string=' '.join(jidipi_string.splitlines()))
            else:
                flag, blog_string, jidipi_string = compare_data.get_urls(form.blog_url.data, '',
                                                                         arch_jidipi_data)
                return render_template('index.html', form=form, flag=flag,
                                       blog_string=' '.join(blog_string.splitlines()),
                                       jidipi_string=' '.join(jidipi_string.splitlines()))
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
            status, data_lst, max_data = split_url_data.get_data_to_split(form.blog_url.data, form.data_split_num.data,
                                                                          name='split_data')
            return render_template('split_blog_data.html', form=form, status=status, data_lst=data_lst,
                                   max_data=max_data)
    return render_template('split_blog_data.html', form=form)


@app.route('/split-data-by-parts', methods=['POST', 'GET'])
def split_data_by_parts():
    """
    Split data into chunks

    :return: Template
    """
    try:
        form = CheckDataDivisionURL()
        if request.method == 'POST':
            if request.data:
                blog_paragraph = json.loads(request.data.decode('utf-8'))
                if not blog_paragraph.get('new_limit'):
                    return jsonify([])

                lst_of_sentences = [i[0] for i in re.findall(
                    r'([A-Z]([^\.]+|([A-Z][a-z]\.)|([A-Z][a-z][a-z]\.)|([A-Z]\.)|([0-9]\.))+[^A-Z][a-z]{2}[\”|\’|0-9| ]?[\.|\?|\!])',
                    re.sub(" [0-9]+", lambda ele: "" + ele[0], blog_paragraph.get('searchText')))]

                limit = int(blog_paragraph.get('limit'))
                new_limit = int(blog_paragraph.get('new_limit'))

                if new_limit > limit or new_limit < 0:
                    return jsonify("Error")

                new_lst = [' '.join(lst_of_sentences[(i * len(lst_of_sentences)) // new_limit:((i + 1) * len(
                    lst_of_sentences)) // new_limit]) for i in range(new_limit)]

                return jsonify(new_lst)

            if form.validate_on_submit():
                form1 = DataDivisonForm()
                status, data_lst = split_url_data.get_data_to_split(form.blog_url.data, 5, name='split_data_by_parts')
                num = []
                for i in data_lst:
                    num.append(len([i[0] for i in re.findall(
                        r'([A-Z]([^\.]+|([A-Z][a-z]\.)|([A-Z][a-z][a-z]\.)|([A-Z]\.)|([0-9]\.))+[^A-Z][a-z]{2}[\”|\’|0-9| ]?[\.|\?|\!])',
                        re.sub(" [0-9]+", lambda ele: "" + ele[0], i))]))

                return render_template('split_blog_data_by_parts.html', form=form, form1=form1,
                                       data_lst=zip(data_lst, num), status=status)
        return render_template('split_blog_data_by_parts.html', form=form)

    except Exception as e:
        print(e, ':::')


if __name__ == '__main__':
    app.run(debug=True)
