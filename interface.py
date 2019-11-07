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


@app.route('/search_by_author', methods=['GET', 'POST'])
def search_by_author():
    form0 = form.NameForm()
    if form0.validate_on_submit():
        author = form0.data.data
        form0.data.data = ''
    else:
        return flask.render_template('search_by_author.html', form=form0, data='', data_favour='')
    data, data_favour = functions.search_by_author(author)
    return flask.render_template('search_by_author.html', form=form0, data=data, data_favour=data_favour)


@app.route('/search_by_type', methods=['GET', 'POST'])
def search_by_type():
    form0 = form.NameForm()
    if form0.validate_on_submit():
        thetype = form0.data.data
        form0.data.data = ''
    else:
        return flask.render_template('search_by_type.html', form=form0, data='', data_favour='')
    data, data_favour = functions.search_by_type(thetype)
    return flask.render_template('search_by_type.html', form=form0, data=data, data_favour=data_favour)


"""
    暂时的解决方案，试图完善通过href得到指定参数并传入表单中
"""
@app.route('/type/<thetype>')
def totype(thetype):
    return thetype


@app.route('/update')
def update():
    form0 = form.UpdateForm()
    if form0.validate_on_submit():
        data = form0.data
        form0.data = []
    return flask.render_template('update.html', form=form0)



if __name__ == '__main__':
    app.run(debug=True)
