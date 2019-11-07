# 只有在涉及表单相关项时才使用bootstrap
import flask_wtf
import wtforms


class NameForm(flask_wtf.FlaskForm):  # search相关的表单模板
    data = wtforms.StringField('input the data', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('submit')


class UpdateForm(flask_wtf.FlaskForm):  # update相关模板
    title = wtforms.StringField('input title', validators=[wtforms.validators.DataRequired()])
    author = wtforms.StringField('input author', validators=[wtforms.validators.DataRequired()])
    type = wtforms.StringField('input type', validators=[wtforms.validators.DataRequired()])
    introduction = wtforms.StringField('input introduction', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('submint')
    data = [title, author, type, introduction]
