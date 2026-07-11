from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem, Wishlist
import os
from django.conf import settings

def product_list(request):
    products = Product.objects.all()

    data = []

    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": float(product.price),
            "image": product.image,
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def create_order(request):
    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")

        user = None

        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        order = Order.objects.create(
            user=user,
            full_name=data["full_name"],
            email=data["email"],
            address=data["address"],
            total_amount=data["total_amount"],
            payment_id=data["payment_id"],
            payment_status="Paid",
        )

        for item in data["items"]:

            product = Product.objects.get(id=item["id"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
            )

        return JsonResponse(
            {
                "message": "Order saved successfully!"
            },
            status=201,
        )

    return JsonResponse(
        {
            "error": "Invalid request"
        },
        status=400,
    )
def my_orders(request):
    username = request.GET.get("username")

    if not username:
        return JsonResponse(
            {"error": "Username required"},
            status=400,
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User not found"},
            status=404,
        )

    orders = Order.objects.filter(user=user).order_by("-created_at")

    data = []

    for order in orders:
        items = []

        for item in order.items.all():
            items.append({
                "product": item.product.name,
                "quantity": item.quantity,
                "price": float(item.price),
            })

        data.append({
            "id": order.id,
            "total": float(order.total_amount),
            "payment": order.payment_status,
            "date": order.created_at.strftime("%d-%m-%Y %H:%M"),
            "items": items,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def add_to_wishlist(request):
    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")
        product_id = data.get("product_id")

        try:
            user = User.objects.get(username=username)
            product = Product.objects.get(id=product_id)

            Wishlist.objects.get_or_create(
                user=user,
                product=product
            )

            return JsonResponse(
                {"message": "Added to Wishlist"},
                status=201
            )

        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        except Product.DoesNotExist:
            return JsonResponse(
                {"error": "Product not found"},
                status=404
            )

    return JsonResponse(
        {"error": "Invalid request"},
        status=400
    )

def load_products(request):
    if Product.objects.exists():
        return JsonResponse({"message": "Products already exist."})

    file_path = os.path.join(settings.BASE_DIR, "products.json")

    with open(file_path, "r") as file:
        data = json.load(file)

    for item in data:
        fields = item["fields"]

        Product.objects.create(
            name=fields["name"],
            description=fields["description"],
            category=fields["category"],
            price=fields["price"],
            image=fields["image"],
        )

    return JsonResponse({"message": "Products loaded successfully!"})