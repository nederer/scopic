from home_page import views

from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('autobid', views.AutoBiddingView.as_view()),
    path('<int:pk>', views.ProductView.as_view()),

]
