from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('tags/', views.tag_list, name='tags'),
    path('create-tag/', views.create_tag, name='create-tag'),
    path('questions/', views.question_list, name='question-list'),
    path('create-question/', views.create_question, name='create-question'),
    path('question/<int:pk>/', views.question_detail, name='question-detail'),
    path('question-answer/<int:question_id>/', views.post_answer, name='post-answer'),
    path('answer/vote/<int:answer_id>/', views.vote_answer, name='vote-answer'),
]