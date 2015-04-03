from app import db

class Testmariadb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    birth = db.Column(db.DateTime())
    death = db.Column(db.DateTime())

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.lastname)
