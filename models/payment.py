from . import db

# payment Model
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(150))
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, payment_type, created_at,updated_at):
        self.payment_type = payment_type
        self.created_at = created_at
        self.updated_at = updated_at