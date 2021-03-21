from datetime import datetime
from setup import db, ma

# Define Company class and schema

class Company(db.Model):
    __tablename__ = 'company'

    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(32))
    c_legent = db.Column(db.String(32))
    c_employed = db.Column(db.Integer)
    c_shacap = db.Column(db.Integer)
    c_other = db.Column(db.Text)
    c_cdate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CompanySchema(ma.SQLAlchemyAutoSchema):
#class CompanySchema(ModelSchema):
    class Meta:
        model = Company
        sqla_session = db.session


