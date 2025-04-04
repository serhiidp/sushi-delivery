from django.http import JsonResponse

from .models.auth import APIKey


class PaymentAPIAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/payments/"):
            api_key = request.headers.get("X-API-Key")

            if not api_key:

                return JsonResponse({"error": "API key required"}, status=401)

            try:
                key_obj = APIKey.objects.get(key=api_key, is_active=True)
                request.api_client = key_obj.user
            except APIKey.DoesNotExist:

                return JsonResponse({"error": "Invalid API key"}, status=401)

        return self.get_response(request)
