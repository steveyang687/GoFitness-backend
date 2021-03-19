from flask import request, g
from libs.nestable_blueprint import NestableBlueprint
from flask_restful import Api, Resource
from libs.handler import default_error_handler
from models.user import UserProfile
from models.base import db
from libs.response import generate_response
from serializer.user import user_schema
from forms.user import RegisterForm, LoginForm
from libs.error_code import FormValidateException, ArgsTypeException
from libs.authorize import create_token, auth

user_bp = NestableBlueprint('user_v1', __name__, url_prefix='user/')
# 定义restapi对象
api = Api(user_bp)


# 指定当出现异常时，所调用的处理方法
# 当需要看到真实的错误信息时，请把下面这一句注释掉
# api.handle_error = default_error_handler

class RegisterView(Resource):
    # @auth.login_required
    def post(self):
        # 获取用户传过来的数据
        data = request.json

        # 验证参数有效性
        # RequestParse: 验证参数类型 => 弱
        # wtforms：更灵活，参数类型、参数值... => 推荐！！
        # 构建表单 => 设置参数的要求 => data与表单绑定 => 验证数据有效性
        form = RegisterForm(data=data)
        if form.validate():

            # 注意： form.email.data
            UserProfile.create_user(user_profile_email=form.email.data,
                                    user_profile_name=form.username.data,
                                    password=form.password.data,
                                    user_profile_mobile=form.phone.data)
            user = UserProfile.query.filter_by(user_profile_email=data.get("email")).first()
            result = user_schema.dump(user)
            # 返回结果
            return generate_response(data=result)
        else:
            result = form.errors
            raise FormValidateException(message=result)


class LoginView(Resource):
    def post(self):
        # 接收用户数据
        data = request.json
        if not data:
            raise ArgsTypeException(message="传参的方式不对，或没有传参")

        # 验证用户输入数据合法性
        # 创建Form -> data绑定 -> validate
        form = LoginForm(data=data)
        # validate函数返回了合法的用户
        user = form.validate()
        # 生成token
        token = create_token(uid=user.user_profile_id)
        return generate_response(data={"token": token})


class UserView(Resource):
    @auth.login_required
    def get(self):
        """获取用户，并返回用户信息"""
        user = UserProfile.query.get(g.user["uid"])
        user_dict = user_schema.dump(user)
        user_dict[
            "avatar"] = "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1016301861,2773103463&fm=26&gp=0.jpg"
        return generate_response(data=user_dict)


# @app.route("/api/v1/check_token/")
# def check_token():
# 	params = request.args
# 	print(params)
# 	token = params.get("token")
# 	# 如果token不为False或false
# 	if token and token != "false":
# 		return "ok"
# 	else:
# 		return "notok"


api.add_resource(RegisterView, 'register/')
api.add_resource(LoginView, 'login/')
api.add_resource(UserView, '/')
