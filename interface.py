import flask
import flask_wtf
import flask_bootstrap
import form
import functions
import wtforms

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yyh970923'  # 密钥
bootstrap = flask_bootstrap.Bootstrap(app)

@app.route('/')
def main_gui():
    return flask.render_template('MainGui.html')


@app.route('/search')
def search():
    return flask.render_template('search.html')


@app.route('/search_by_title', methods=['GET', 'POST'])
def search_by_title():
    form0 = form.NameForm()
    if form0.validate_on_submit():  # 数据不为空
        title = form0.data.data
        form0.data.data = ''
    else:
        return flask.render_template('search_by_title.html', form=form0, data='')  # 输入为空
    data = functions.search_by_title(title)
    return flask.render_template('search_by_title.html', form=form0, data=data)


@app.route('/search_by_author')
def search_by_author():
    return flask.render_template('search_by_author.html')


@app.route('/search_by_type')
def search_by_type():
    return flask.render_template('serch_by_type.html')


if __name__ == '__main__':
    app.run(debug=True)
