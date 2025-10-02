from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, ProfileView, PromoteToAdminView, ClientProfileView,
    ServiceViewSet, CartViewSet, CartItemViewSet, ReviewViewSet, OrderViewSet,
    CheckoutView, PaymentView, add_to_cart, remove_from_cart
)

router = DefaultRouter()
router.register(r"services", ServiceViewSet)
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cart-items")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    # Auth endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("promote/<int:pk>/", PromoteToAdminView.as_view(), name="promote-to-admin"),
    path("client/profile/", ClientProfileView.as_view(), name="client-profile"),

    # Cart actions
    path("add-to-cart/<int:service_id>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove-from-cart"),

    # Checkout & Payment
    path("api/checkout/", CheckoutView.as_view(), name="checkout"),
    path("api/payment/", PaymentView.as_view(), name="payment"),

    # DRF API router
    path("api/", include(router.urls)),
]
