from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('Add',views.add,name="add"),
    path("<str:name>-<int:id>",views.entry,name="entry"),
    path('<str:name>-<int:id>/close',views.close,name='close'),
]
