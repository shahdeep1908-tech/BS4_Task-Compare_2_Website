from flask import Flask, request, render_template
from forms import BlogForm
import utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/', methods=['POST', 'GET'])
def check_text():
    form = BlogForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flag = utils.get_urls(form.blog_url.data, form.jidipi_url.data)
            return render_template('index.html', form=form, flag=flag)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
