from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import generics, permissions, viewsets, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Service, Cart, CartItem, Review, Order, OrderItem
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    AdminPromotionSerializer, ClientProfileSerializer,
    ServiceSerializer, CartSerializer, CartItemSerializer,
    ReviewSerializer, OrderSerializer, PaymentSerializer
)

User = get_user_model()

# ---------------- Auth ----------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class PromoteToAdminView(generics.UpdateAPIView):
    queryset = User.objects.filter(role="client")
    serializer_class = AdminPromotionSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        if getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can promote users"}, status=403)
        return super().update(request, *args, **kwargs)

class ClientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

# ---------------- Services ----------------
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().annotate(avg_rating=Avg("reviews__rating"))
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating', 'price', 'name']
    ordering = ['-avg_rating']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can add services"}, status=403)
        return super().create(request, *args, **kwargs)

# ---------------- Cart ----------------
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "delete", "patch"]
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

# ---------------- Reviews ----------------
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---------------- Orders ----------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", "client") == "admin":
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(user=user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        items = list(cart.items.select_related("service"))
        if not items:
            return Response({"detail": "Cart is empty"}, status=400)

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
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=201)

    def partial_update(self, request, *args, **kwargs):
        if getattr(request.user, "role", "client") != "admin":
            return Response({"detail": "Only admins can update order status"}, status=403)
        return super().partial_update(request, *args, **kwargs)

# ---------------- Checkout ----------------
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        if not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

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
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

# ---------------- Payment ----------------
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data['order_id']
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.payment_status = 'paid'
        order.status = 'completed'
        order.save()
        return Response({"detail": "Payment successful", "order": OrderSerializer(order).data})

# ---------------- Cart API ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return Response({"detail": "Item added to cart"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return Response({"detail": "Item removed from cart"})
