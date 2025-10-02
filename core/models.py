from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ---------------- User ----------------
class User(AbstractUser):
    ROLE_CHOICES = (("admin", "Admin"), ("client", "Client"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="client")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username

# FK helper
AUTH_USER = settings.AUTH_USER_MODEL

# ---------------- Service ----------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ---------------- Cart ----------------
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.service.name}"

# ---------------- Review ----------------
class Review(models.Model):
    user = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.rating})"

# ---------------- Order ----------------
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.name}"

# ---------------- OrderItem ----------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.price_at_purchase
