# core/views.py
from django.contrib.auth import get_user_model
from django.db.models import Avg, F, Q
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Cart, CartItem, Order, OrderItem
from .serializers import OrderSerializer

from .models import Service, Cart, CartItem, Review, Order, OrderItem
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    AdminPromotionSerializer, ClientProfileSerializer,
    ServiceSerializer, CartSerializer, CartItemSerializer,
    ReviewSerializer, OrderSerializer
)

def redirect_to_api(request):
    return redirect("/api/")

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(s.validated_data)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class PromoteToAdminView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminPromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(role="client")
    def update(self, request, *args, **kwargs):
        if getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can promote users"}, status=403)
        return super().update(request, *args, **kwargs)

class ClientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# ---- Services with ordering by avg rating ----
from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer

# core/views.py
from rest_framework import filters

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.OrderingFilter]       # ✅ Add this line
    ordering_fields = ['avg_rating', 'price', 'name']  # Allow sorting by rating, price, name
    ordering = ['-avg_rating']                        # Default ordering


    def get_queryset(self):
        return Service.objects.all().annotate(avg_rating=Avg("reviews__rating"))

    def create(self, request, *args, **kwargs):
        # Only admins can create services
        if not request.user.is_authenticated or getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can add services"}, status=403)
        return super().create(request, *args, **kwargs)

# ---- Cart ----
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cart.objects.all()  # ✅ add this

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "delete", "patch"]
    queryset = CartItem.objects.all()  # ✅ add this

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

# ---- Reviews ----
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---- Orders (service history) ----
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch"]  # list, create (from cart), update status (admin)

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", "client") == "admin":
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Create an Order from the current user's Cart (checkout).
        Moves items to an Order and clears the cart.
        """
        user = request.user
        # Ensure cart exists and has items
        cart, _ = Cart.objects.get_or_create(user=user)
        items = list(cart.items.select_related("service"))
        if not items:
            return Response({"detail": "Cart is empty"}, status=400)

        # Create order
        order = Order.objects.create(user=user, status="pending", total_amount=0)
        total = 0
        for ci in items:
            OrderItem.objects.create(
                order=order,
                service=ci.service,
                quantity=ci.quantity,
                price_at_purchase=ci.service.price,
            )
            total += ci.quantity * ci.service.price

        order.total_amount = total
        order.save()

        # Clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=201)

    def partial_update(self, request, *args, **kwargs):
        # Admin can update status
        if getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can update order status"}, status=403)
        return super().partial_update(request, *args, **kwargs)



# core/views.py
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = Order.objects.create(user=user, status="pending")
        total = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                service=item.service,
                quantity=item.quantity,
                price_at_purchase=item.service.price
            )
            total += item.quantity * item.service.price

        order.total_amount = total
        order.save()

        # Clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import PaymentSerializer, OrderSerializer

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Simulate payment success
        order.payment_status = 'paid'
        order.status = 'completed'
        order.save()

        return Response({"detail": "Payment successful", "order": OrderSerializer(order).data})

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import Service, Cart, CartItem, Order


def home(request):
    return render(request, 'core/home.html')

def services_page(request):
    services = Service.objects.all().annotate(avg_rating=Avg("reviews__rating"))
    return render(request, 'core/services.html', {'services': services})

def cart_page(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, 'core/cart.html', {'cart_items': cart.items.all()})
    return redirect('login')

def checkout_page(request):
    if request.method == "POST":
        # call CheckoutView logic here or redirect
        return redirect('orders-list')
    return render(request, 'core/checkout.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_page(request):
    # You can pass user info or related data to template
    context = {
        'user': request.user,
        # You can also pass orders, cart, etc.
    }
    return render(request, 'core/profile.html', context)

# core/views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Service, Cart, CartItem

def add_to_cart(request, service_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    service = get_object_or_404(Service, id=service_id)
    
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)
    
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart-page')
from django.shortcuts import redirect, get_object_or_404
from .models import CartItem

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart-page')  # redirect back to cart page

