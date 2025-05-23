from flask import Blueprint ,request , jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.product_model import Product
from app.models.category_model import Category
from app.extensions import db
from flask_jwt_extended  import jwt_required, get_jwt_identity

# Products blueprint
products = Blueprint('products',__name__,url_prefix='/api/v1/products')

# creating a new product
@products.route('/create', methods=['POST'])
def creatingProduct():

    #Storing request values
    data = request.json
    name = data.get('name')
    categories = data.get('categories')
    category_id = data.get('category_id')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

# Validations of the incoming request data
    if not name or not categories or category_id:
        return jsonify({
            'error': "All Fields are required"
        }), HTTP_400_BAD_REQUEST
    

    if Category.query.filter_by(name=name, category_id=category_id).first() is not None:
        return jsonify({
            'error':f"Product name and category_is{category_id} already exists"
        }),HTTP_409_CONFLICT
    
    try:
        #creating a new product
        new_product = Product(name=name,
                         categories=categories,
                         products=products,
                         category_id = category_id,
                         created_at=created_at,
                         updated_at=updated_at)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            'message' : name +"product has been successfully created ",
            'product':{
                'id':new_product.id,
                "name":new_product.name,
                "created_at":new_product.created_at,
                "updated":new_product.updated_at,
                'categories':{
                    'id':new_product.category.id,
                    'name': new_product.category.name,
                    'description':new_product.category.description
                },
            }
        }), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({    
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

# #Getting all products from the database
@products.get('/all')
def getAllProducts():

    try:
        all_products = Product.query.all()

        products_data =[]

        for product in all_products:
            products_info={
                'id':product.id,
                "name":product.name,
                "description":product.description,
                "created_at": product.created_at,
                "updated_at":product.updated_at,
                'category':{
                    'id':product.category.id,
                    'name': product.category.name,
                    'description':product.category.description,
                }
            }
            products_info.append(products_data)
        return jsonify({
            'message':"All products retrieved successfully",
            'total_products':len(products_data),
            'products': products_data
        }),HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


# Edit The product
@products.route('/edit/<int:id>', methods =['PUT','PATCH'])
def editProduct(id):

    try:

        #edit product by id
        product = Product.query.filter_by(id = id).first()

        if not product:
            return jsonify({'error':"Product not found"}),HTTP_404_NOT_FOUND
        
        else:
            #Store  request data
            name = request.get_json.get('name',product.name)
            created_at = request.get_json.get('created_at',product.created_at)
            updated_at = request.get_json.get('updated_at',product.updated_at)

            if name  != product.name  and Product.query.filter_by(name =name ).first():
                return jsonify({'error':"name  address already in use "}),HTTP_409_CONFLICT

            product.name = name
            product.created_at = created_at
            product.updated_at = updated_at

            db.session.commit()

            return jsonify({
                'message': name + " 's Details have been updated successfully updated ",
                "product": {
                   'id':product.id,
                   'name': product.name,
                   'created_at': product.created_at,
                   'updated_at': product.updated_at
                }
            }),HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    

#Delete the product
@products.route('/delete/<int:id>', methods =['DELETE'])
def deleteProduct(id):

    try:
#get product by id
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({
                "error": "book not found"
            }),HTTP_404_NOT_FOUND
        
        else:
            #delete associated products
            db.session.delete(product)
            db.session.commit()

            return jsonify({
                'message': f"Product with id {id}deleted successfully"
            })

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
