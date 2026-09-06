from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("create/", views.create_article, name="create_article"),
    path("article/<int:pk>/bookmarks/", views.toggle_bookmark, name="toggle_bookmark"),
    path("bookmarks/", views.my_bookmarks, name="my_bookmarks"),
    path("notifications/<int:pk>", views.mark_notification_as_read, name="mark_notification_as_read"),
    path("notifications/read-all", views.mark_all_notification_as_read, name="mark_all_notification_as_read"),
    path("my-subscriptions/", views.my_subscriptions, name="my_subscriptions"),
    path("author/<int:author_id>/toggle-subscription/", views.toggle_subscription, name="toggle_subscription"),
    path(
        "login/", 
        auth_views.LoginView.as_view(
            template_name="articles/login.html"
            ), 
            name="login"
        ),

    path("notifications/", views.notification_list, name="notification_list"),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path("signup/", views.signup, name="signup"),
    path("export/excel", views.export_articles_to_excel, name="export_articles_to_excel")
]