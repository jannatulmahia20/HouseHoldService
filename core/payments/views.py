import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def create_order(request):
    user = request.user
    data = request.data  

    # Use your live Render URL instead of localhost
    base_url = "https://householdservice-2.onrender.com"

    post_data = {
        "store_id": settings.SSLCZ_STORE_ID,
        "store_passwd": settings.SSLCZ_STORE_PASS,
        "total_amount": 1000, 
        "currency": "BDT",
        "tran_id": "ORDER12345", 
        "success_url": f"{base_url}/api/payment/success/",
        "fail_url": f"{base_url}/api/payment/fail/",
        "cancel_url": f"{base_url}/api/payment/cancel/",
        "cus_name": user.username if user.is_authenticated else "Guest User",
        "cus_email": getattr(user, 'email', 'customer@example.com'),
        "cus_add1": data.get("address", "Dhaka"), 
        "cus_phone": data.get("phone", "01700000000"), 
        "shipping_method": "NO",
        "product_name": data.get("service", "General Service"),
        "product_category": "Household",
        "product_profile": "general",
    }

    
    response = requests.post(settings.SSLCZ_API_URL, data=post_data)
    
    try:
        result = response.json()
    except Exception as e:
        return Response({"error": "SSLCommerz returned non-JSON response", "details": response.text}, status=500)

    if result.get("status") == "SUCCESS":
        return Response({"GatewayPageURL": result["GatewayPageURL"]})
    else:
        
        return Response({
            "error": "Failed to initiate payment", 
            "details": result.get("failedreason", "Unknown error"),
            "full_response": result
        }, status=400)