from Rollladensteuerung import db


class Shutter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String, unique=True, nullable=False)
    ip = db.Column(db.String, unique=True, nullable=False)
    state = db.Column(db.String, nullable=False)


if __name__ == '__main__':
    #db.create_all()
    Shutter.query.all()
