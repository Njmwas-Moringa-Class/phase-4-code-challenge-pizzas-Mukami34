from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    # Add serialization rules
    def serialize(self):
        serialized_pizzas = [rp.serialize() for rp in self.restaurant_pizzas] if self.restaurant_pizzas else []
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'restaurant_pizzas': serialized_pizzas
        }

    def serialize_with_pizzas(self):
        serialized_pizzas = [rp.serialize() for rp in self.restaurant_pizzas] if self.restaurant_pizzas else []
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'restaurant_pizzas': serialized_pizzas
        }

    def __repr__(self):
        return f'<Restaurant id={self.id}, name={self.name}, address={self.address}>'





class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')
    
    # add serialization rules
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    def serialize(self):
        return {
        'id': self.id,
        'price': self.price,
        'pizza': self.pizza.serialize(),  
        'pizza_id': self.pizza_id,
        'restaurant_id': self.restaurant_id
    }

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("validation errors")
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
