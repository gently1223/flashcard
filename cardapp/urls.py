from django.urls import path
from cardapp import views

urlpatterns = [
    path('user_info/', views.UserInfoList),
    path('question_book/', views.QuestionBookList),
    path('setting/', views.SettingList),
    path('setting/<int:pk>/', views.SettingDetail),
    path('getmaxcount/', views.getMaxCount)
]