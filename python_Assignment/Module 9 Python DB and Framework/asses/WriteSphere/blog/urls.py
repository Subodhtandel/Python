from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("post/new/", views.PostCreateView.as_view(), name="create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="edit"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("post/<slug:slug>/like/", views.toggle_like, name="like_toggle"),
    path(
        "authors/<str:username>/",
        views.AuthorProfileView.as_view(),
        name="author_profile",
    ),
    path(
        "authors/<str:username>/follow/",
        views.toggle_follow,
        name="follow_toggle",
    ),
    path(
        "comment/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="comment_edit",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
