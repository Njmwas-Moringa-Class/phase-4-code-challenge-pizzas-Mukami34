#!/usr/bin/env python3

import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Migrate setup
migrate = Migrate(app, db)

# Initialize db
db.init_app(app)

# Routes
@app.route('/')
def index():
    """Home route."""
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    """Get all restaurants."""
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.serialize() for restaurant in restaurants]), 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = restaurant = Restaurant.query.get_or_404(id)
    if restaurant:
        return jsonify(restaurant.serialize_with_pizzas()), 200
    else:
        return jsonify({"error": "Restaurant not found"}), 404


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    """Delete a restaurant and all associated restaurant_pizzas"""
    restaurant = Restaurant.query.get(id)
    if restaurant:
        for rp in restaurant.restaurant_pizzas:
            db.session.delete(rp)
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    """Get all pizzas."""
    pizzas = Pizza.query.all()
    return jsonify([pizza.serialize() for pizza in pizzas]), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    """Create a new restaurant pizza."""
    try:
        new_restaurant_pizza = RestaurantPizza(
            price=request.json.get('price'),
            pizza_id=request.json.get('pizza_id'),
            restaurant_id=request.json.get('restaurant_id'),
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Retrieve the associated pizza and restaurant
        pizza = Pizza.query.get(new_restaurant_pizza.pizza_id)
        restaurant = Restaurant.query.get(new_restaurant_pizza.restaurant_id)

        return jsonify({
            'id': new_restaurant_pizza.id,
            'price': new_restaurant_pizza.price,
            'pizza': pizza.serialize(),
            'pizza_id': new_restaurant_pizza.pizza_id,
            'restaurant': restaurant.serialize(),
            'restaurant_id': new_restaurant_pizza.restaurant_id
        }), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
