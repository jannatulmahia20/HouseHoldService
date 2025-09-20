from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView
from .views import remove_from_cart

from .views import (
    redirect_to_api, RegisterView, LoginView, ProfileView,
    PromoteToAdminView, ClientProfileView, ServiceViewSet,
    CartViewSet, CartItemViewSet, ReviewViewSet, OrderViewSet,
    CheckoutView, PaymentView,
    home, services_page, cart_page, checkout_page, profile_page,
    add_to_cart   # <-- add this
)


# DRF router for API viewsets
router = DefaultRouter()
router.register(r"services", ServiceViewSet)
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cart-items")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    # Redirect root
    path("", home, name="home"),

    # Auth endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('profile/', profile_page, name='profile-page'),



    path("promote/<int:pk>/", PromoteToAdminView.as_view(), name="promote-to-admin"),
    path("client/profile/", ClientProfileView.as_view(), name="client-profile"),

    # DRF API endpoints
    path("api/checkout/", CheckoutView.as_view(), name="checkout"),
    path("api/payment/", PaymentView.as_view(), name="payment"),
    path("api/", include(router.urls)),

    # Frontend pages
    path('home-page/', home, name='home-page'),
    path('services-page/', services_page, name='services-page'),
    path('cart/', cart_page, name='cart-page'),

    path('checkout-page/', checkout_page, name='checkout-page'),
    
    path("logout/", LogoutView.as_view(next_page="home-page"), name="logout"),
    path('add-to-cart/<int:service_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove-from-cart'),


]
