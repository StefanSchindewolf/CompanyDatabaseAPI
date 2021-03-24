from datetime import datetime
from setup import db, ma
from marshmallow import fields


# Additional notes per line item
class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('company.c_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Define Company class
class Company(db.Model):
    __tablename__ = 'company'

    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(32))
    c_legent = db.Column(db.String(32))
    c_employed = db.Column(db.Integer)
    c_shacap = db.Column(db.Integer)
    c_other = db.Column(db.Text)
    c_cdate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.relationship('Note', backref='company', cascade='all, delete, delete-orphan', single_parent=True,  order_by='desc(Note.timestamp)')


# Define Company Schema
class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        sqla_session = db.session
        load_instance = True
    notes = fields.Nested('NoteCompanySchema', default=[], many=True)


# Define Company Note Schema
class CompanyNoteSchema(ma.SQLAlchemyAutoSchema):
    note_id = fields.Int()
    c_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()


# Define Notes schema
class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        sqla_session = db.session
    company = fields.Nested('NoteCompanySchema', default=None)


# Define Note Company Schema
class NoteCompanySchema(ma.SQLAlchemyAutoSchema):
    note_id = fields.Int()
    c_id = fields.Int()
    content = fields.Str()
    timestamp = fields.Str()
