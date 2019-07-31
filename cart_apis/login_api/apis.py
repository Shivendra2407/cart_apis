from django.urls import path
from .views import *
from django.conf.urls import url
urlpatterns = [
    # path('login', login, name="login"),
    # path('login_count', user_count, name="user_count")
    url(r'^$', UserLoginView.as_view(), name="user-login")

]