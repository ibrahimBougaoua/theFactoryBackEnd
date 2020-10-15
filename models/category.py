from . import db

# Category Model
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, slug, description, created_at,updated_at):
        self.name = customer_id
        self.slug = slug
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at