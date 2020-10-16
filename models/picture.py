from . import db

# picture product Model
class Picture(db.Model):
    picture_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    size = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'),nullable=False)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, size, product_id, created_at):
        self.name = name
        self.size = size
        self.product_id = product_id
        self.created_at = created_at