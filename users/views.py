from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from users.models import User, Payment
from users.permissons import UserPermission

from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date_payment',)

    def perform_create(self, serializer):
        """
        Создает платеж.
        """

        payment = serializer.save(user=self.request.user)

        if payment.payment_method == "bank transfer":
            product = create_stripe_product(payment)
            price = create_stripe_price(int(payment.payment_amount), product.name)
            session_id, link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = link
        payment.save()
