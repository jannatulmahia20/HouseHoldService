import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def create_order(request):
    data = request.data  

    post_data = {
        "store_id": settings.SSLCZ_STORE_ID,
        "store_passwd": settings.SSLCZ_STORE_PASS,
        "total_amount": 1000,  # 🔹 You can set based on service plan
        "currency": "BDT",
        "tran_id": "ORDER12345",  # Generate unique ID
        "success_url": "http://localhost:8000/api/payment/success/",
        "fail_url": "http://localhost:8000/api/payment/fail/",
        "cancel_url": "http://localhost:8000/api/payment/cancel/",
        "cus_name": data.get("name"),
        "cus_email": "customer@example.com",
        "cus_add1": data.get("address"),
        "cus_phone": data.get("phone"),
        "shipping_method": "NO",
        "product_name": data.get("service"),
        "product_category": "Household",
        "product_profile": "general",
    }

    response = requests.post(settings.SSLCZ_API_URL, data=post_data)
    result = response.json()

    if "GatewayPageURL" in result:
        return Response({"GatewayPageURL": result["GatewayPageURL"]})
    else:
        return Response({"error": "Failed to initiate payment", "details": result}, status=400)
