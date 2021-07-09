from api import views

from django.urls import path

urlpatterns = [
    path("products", views.ProductsCurrentInfoView.as_view()),
    path("products/<int:pk>/history", views.ProductBidHistoryView.as_view()),
    path("products/<int:pk>", views.ProductBidView.as_view()),
    path("user/bids", views.UserAutoBidView.as_view()),
]
