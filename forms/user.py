from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
from werkzeug.security import check_password_hash
from models.user import UserProfile
from libs.error_code import AuthorizedException


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Email(message="邮箱不合法")])
    # 必填，大写，小写，数字，下划线组成的6~18位的字符串
    password = StringField(validators=[DataRequired(), Regexp(r'^\w{6,18}$', message="密码复杂度不符合要求")])
    username = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired(), Regexp(r'^1[0-9]{10}$', message="手机号码不符合要求")])

    # 自定义字段检查方法(validate_你要检查的字段名)
    def validate_username(self, value):
        # 验证email是否在数据库已经存在
        print("check_username")
        if UserProfile.query.filter_by(user_profile_name=value.data).first():
            raise ValidationError("用户名已存在！")

    # 用户名长度6~16位之间
    def validate_name(self, value):
        print("check_name")
        # 对数据进行修改
        value.data = value.data

    def validate_password(self, value):
        print("check_password")

    # 整体验证
    def validate(self):
        print("整体验证！！！")
        return super().validate()


class LoginForm(Form):
    # 这里用这个名字接收数据是由于前端iview-admin使用的是这个名字，在那边修改成本比较大，因此改这边
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate(self):
        # 验证用户名密码(如果是由于邮箱不合法导致还是会提示用户名密码错误，考虑如何优化)
        super().validate()
        # if self.errors:
        #     return False
        user = UserProfile.query.filter_by(user_profile_name=self.username.data).first()
        if user and check_password_hash(user.password, self.password.data):
            return user
        else:
            raise AuthorizedException(message="用户名或密码错误")
