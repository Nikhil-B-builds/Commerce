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
    path('<str:name>-<int:id>/comment',views.comment,name='comment'),

    path('<str:name>-<int:id>/wishlist/add',views.wishlist_add,name='wishlist_add'),
    path('<str:name>-<int:id>/wishlist/del',views.wishlist_del,name='wishlist_del'),
    path('<str:name>/wishlist',views.wishlist,name='wishlist'),

    path('category',views.category,name='category')
]
