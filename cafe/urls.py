from django.urls import path

from cafe.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
