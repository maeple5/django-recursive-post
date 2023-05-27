from django.urls import path, register_converter

from snippets import views
from . import converters


register_converter(converters.FourDigitYearConverter, 'yyyy')
urlpatterns = [
    path("new/", views.snippet_new, name="snippet_new"),
    path("<int:snippet_id>/", views.snippet_detail, name="snippet_detail"),
    path("<int:snippet_id>/edit/", views.snippet_edit, name="snippet_edit"),
    path("<int:snippet_id>/comments/new/", views.comment_new, name="comment_new"),
    path("<int:snippet_id>/comments/<int:comment_id>", views.comment_detail, name="comment_detail"),
    # path("<yyyy:year>/", views.year_archive),
    path("hello/", views.hello, name="hello"),
    # path("users/", views.user_list, name="user_list"),
    # path("users/<str:name>", views.user_detail, name="user_detail"),
    path("hello/", views.hello, name="hello"),
    
]
