from . import db

# factory Sales Model
class Factory(db.Model):
    factory_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.Text)
    logo = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'),nullable=False)
    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    def __init__(self, name, desc, logo, phone, employee_id, created_at ,updated_at):
        self.name = name
        self.desc = desc
        self.logo = logo
        self.phone = phone
        self.employee_id = employee_id
        self.created_at = created_at
        self.updated_at = updated_at