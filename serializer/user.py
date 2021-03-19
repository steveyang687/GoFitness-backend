from .base import ma
from models.user import UserProfile


class UserSchema(ma.Schema):
    class Meta:
        model = UserProfile
        fields = ('user_profile_name', 'user_profile_email', 'user_profile_id')


user_schema = UserSchema()