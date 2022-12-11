from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("enter", views.enternew, name="enter"),
    path("showgroup", views.showgroup, name="showgroup"),
    path("listingpage/<int:id>", views.listingpage, name="listingpage")
]
