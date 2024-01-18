from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.new,name="new"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("watchlist",views.watch,name="watchlist"),
    path("addwatchlist",views.addwatchlist,name="addwatchlist"),
    path("delete/<int:id>",views.deleteListing,name="delete"),
    path("close/<int:id>",views.closeListing,name="close"),
    path("deleteWatch",views.deleteWatch,name="deleteWatch")
]
