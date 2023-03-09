import os
from flask import Flask, redirect, request

import stripe
# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
# stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

app = Flask(__name__)



@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.form
    line_items = []
    for price_id, qty in data.items():
        line_items.append({
            'price': price_id,
            'quantity': qty
        }
        )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items= line_items,
            mode='payment',
            success_url='http://localhost:3000/home' + '?success=true', # route once payment goes through
            cancel_url='http://localhost:3000/shop' + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run()
