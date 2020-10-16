from . import db

# employee point of sale Model
class EmployeePointOfSale(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'),nullable=False)
    point_sale_id = db.Column(db.Integer, db.ForeignKey('point_of_sale.point_sale_id'),nullable=False)
    date = db.Column(db.TIMESTAMP)

    def __init__(self, employee_id, point_sale_id, date):
        self.employee_id = employee_id
        self.point_sale_id = point_sale_id
        self.date = date