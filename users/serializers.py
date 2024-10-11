from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_payments(self, instance):
        """
        Возвращает все платежи пользователя.
        """

        return [payment.payment_amount for payment in instance.payment.all()]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
