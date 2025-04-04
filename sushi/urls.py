from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import auth, orders, payments, sushi

router = DefaultRouter()
router.register(r"sushi", sushi.SushiViewSet)
router.register(r"categories", sushi.CategoryViewSet)
router.register(r"orders", orders.OrderViewSet, basename="order")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", auth.UserRegistrationView.as_view(), name="register"),
    path("login/", auth.CustomAuthToken.as_view(), name="login"),
    path(
        "payments/<int:order_id>/create/",
        payments.PaymentIntentAPIView.as_view(),
        name="create-payment",
    ),
    path(
        "payments/confirm/<str:transaction_id>/",
        payments.PaymentConfirmationAPIView.as_view(),
        name="confirm-payment",
    ),
]
