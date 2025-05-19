from django.urls import path
from newsApp.views import (
    IndexView,
    about_view,
    like_post,
    post_view,
    contacts_view,
    NewsPostCreate,
    NewsPostDelete,
    NewsPostEdit,
    project_comment_view,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about", about_view, name="about"),
    path("contacts", contacts_view, name="contacts"),
    path("posts/<int:id>/", post_view, name="post-detail"),
    path("like-post/<int:post_id>/", like_post, name="post-like"),
    path("create-post", NewsPostCreate.as_view(), name="create-post"),
    path("edit-post/<int:pk>/", NewsPostEdit.as_view(), name="edit-post"),
    path("delete-post/<int:pk>/", NewsPostDelete.as_view(), name="delete-post"),
    path("comment-post/<int:pk>/", project_comment_view, name="comment-post"),
]
