from rest_framework import serializers
from .models import user_info, question_book, setting


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_info
        fields = ('id', 'user_id', 'password')
class QuestionBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = question_book
        fields = ('id', 'uuid', 'file_name', 'image_folder', 'contents')
class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = setting
        fields = ('id', 'user_id', 'data')