from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Cow(db.Model):
    __tablename__ = 'Cowlibrate'  # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True)
    milk_yield = db.Column(db.Float, nullable=False)
    health = db.Column(db.String(255), nullable=False)
    lactation_stage = db.Column(db.String(255), nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    enclosure_temp = db.Column(db.Float, nullable=True)
    outside_temp = db.Column(db.Float, nullable=True)
    country = db.Column(db.String(255), nullable=False)
    feed_type = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, milk_yield, health, lactation_stage, breed, enclosure_temp,
                outside_temp, country, feed_type, age):
        self.milk_yield = milk_yield
        self.health = health
        self.lactation_stage = lactation_stage
        self.breed = breed
        self.enclosure_temp = enclosure_temp
        self.outside_temp = outside_temp
        self.country = country
        self.feed_type = feed_type
        self.age = age
