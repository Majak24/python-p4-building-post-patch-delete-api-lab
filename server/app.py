#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    if request.method == 'PATCH':
        # Get data from form
        data = request.form
        
        # Update name if provided in form
        if 'name' in data:
            bakery.name = data['name']
            
        # Commit changes to database
        db.session.commit()
    
    bakery_serialized = bakery.to_dict()
    return make_response(bakery_serialized, 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'POST':
        # Get data from form
        data = request.form
        
        # Create new baked good
        new_baked_good = BakedGood(
            name=data['name'],
            price=float(data['price']),
            bakery_id=int(data['bakery_id'])
        )
        
        # Add to database and commit
        db.session.add(new_baked_good)
        db.session.commit()
        
        # Return the new baked good as JSON
        return make_response(new_baked_good.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Find the baked good
    baked_good = BakedGood.query.filter_by(id=id).first()
    
    # Delete from database
    db.session.delete(baked_good)
    db.session.commit()
    
    # Return success message
    return make_response(
        jsonify({"message": "Baked good successfully deleted"}),
        200
    )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response(baked_goods_by_price_serialized, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response(most_expensive_serialized, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)