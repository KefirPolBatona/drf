from datetime import datetime, timedelta

import pytz
import stripe

stripe.api_key = "sk_test_51QAxqqJTgni3y9ZDa0sokcTpXtKok8GqMuhq49JM1GVQeD6kZM5pFTacez71zKBp2mw65Ravm8BmVUBXpqC6R77d00vHlegx4n"


def create_stripe_product(instance):
    """
    Создает продукт в страйпе.
    """

    if instance.course:
        name = instance.course
    else:
        name = instance.lesson
    return stripe.Product.create(name=name)


def create_stripe_price(amount, name):
    """
    Создает цену в страйпе.
    """

    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": name},
    )


def create_stripe_session(price):
    """
    Создает сессию оплаты в страйпе.
    """

    session = stripe.checkout.Session.create(
        success_url='http://localhost:8000/' + 'users/payments/{CHECKOUT_SESSION_ID}',
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
