from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="products"),
    path("create-order/", views.create_order, name="create_order"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path(
    "wishlist/add/",
    views.add_to_wishlist,
    name="add-to-wishlist"
),
path("load-products/", views.load_products, name="load-products"),
]