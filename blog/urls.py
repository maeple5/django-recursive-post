from django.urls import path, register_converter

from blog import views
from . import converters

app_name = 'blog'
register_converter(converters.FourDigitYearConverter, 'yyyy')
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path("detail/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path('comment/<int:pk>/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
    path("new/", views.post_new, name="post_new"), 
    # path("<int:post_id>/", views.post_detail, name="post_detail"),
    # path("<int:post_id>/comments/new/", views.comment_new, name="comment_new"),
    # path("<int:snippet_id>/comments/<int:comment_id>", views.comment_detail, name="comment_detail"),
    # path("<yyyy:year>/", views.year_archive),
    # path("hello/", views.hello, name="hello"),
    # # path("users/", views.user_list, name="user_list"),
    # # path("users/<str:name>", views.user_detail, name="user_detail"),
    # path("hello/", views.hello, name="hello"),
    
]
