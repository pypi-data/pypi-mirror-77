from functools import wraps
from flask import g, request, jsonify
from furl import furl

PAYMENT_STATE_KEY = "_lonny_flask_payments"
PROTO_HEADER = "X-Forwarded-Proto"

class PaymentState:
    def __init__(self):
        self.success = False

def _get_payment_state():
    g.setdefault(PAYMENT_STATE_KEY, PaymentState())

def is_success():
    return _get_payment_state().success

class StripeStrategy:
    def __init__(self, client):
        self._client = client

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if "status" not in request.args:
                session_id = self._setup_session()
                return self.handle_session(session_id)
            if request.args["status"] == "success":
                self._attach_payment_method(request.args["session_id"])
                _get_payment_state().success = True
            fn(*args, **kwargs)
        return wrapped

    def update_payment_method(self, customer_id, payment_method_id):
        raise NotImplementedError()

    def get_customer_id(self):
        raise NotImplementedError()
    
    def handle_session(self, session_id):
        return jsonify(session_id = session_id)

    def _attach_payment_method(self, session_id):
        session = self._client.checkout.Session.retrieve(session_id)
        setup_intent = self._client.SetupIntent.retrieve(session["data"]["object"]["setup_intent"])
        self._client.PaymentMethod.attach(
            setup_intent["payment_method"],
            customer = setup_intent["customer"]
        )
        self.update_payment_method(setup_intent["customer"], setup_intent["payment_method"])

    def _setup_session(self):
        new_scheme = request.headers.get(PROTO_HEADER, request.scheme)
        parsed = furl(request.url).set(scheme = new_scheme)
        session = self._client.checkout.Session.create(
            payment_method_types = ["card"],
            mode = "setup",
            customer = self.get_customer_id(),
            success_url = furl(parsed).set(args = dict(status = "success", session_id = "{CHECKOUT_SESSION_ID}")),
            cancel_url = furl(parsed).set(args = dict(status = "cancel"))
        )
        return session["id"]