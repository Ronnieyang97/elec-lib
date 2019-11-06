# 只有在涉及表单相关项时才使用bootstrap
import flask_wtf
import wtforms


class NameForm(flask_wtf.FlaskForm):  # 定义表单类（newindex中用到）
    data = wtforms.StringField('input the data', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('submit')
