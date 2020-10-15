from . import db

# point of sale Model
class pointOfSale(db.Model):
    point_sale_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    address = db.Column(db.Text)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.factory_id'),nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, address, created_at, updated_at):
        self.name = name
        self.address = address
        self.created_at = created_at
        self.updated_at = updated_at