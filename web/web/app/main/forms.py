from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,DateField,RadioField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class TypeForm(FlaskForm):
    type = RadioField('Label', choices=[('全部', '全部'),('剧情', '剧情'), ('爱情', '爱情'), ('喜剧', '喜剧'),
                                         ('科幻', '科幻'), ('动作', '动作'), ('悬疑', '悬疑'),('犯罪', '犯罪'),
                                         ('恐怖', '恐怖'), ('儿童', '儿童'),('音乐', '音乐'),('战争', '战争'),
                                        ('歌舞', '歌舞'), ('传记', '传记')],
                      default='全部', validators=[Required()])
    submit = SubmitField('确定')


class EditProfileForm(FlaskForm):
    birthday = DateField('出生日期',render_kw={'placeholder':u'输入出生日期格式为YYYY-MM-DD'})
    location = StringField('所在地区', validators=[Length(0, 64)])
    interests = TextAreaField('兴趣喜好')
    about_me = TextAreaField('关于自己')
    submit = SubmitField('确认修改')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
