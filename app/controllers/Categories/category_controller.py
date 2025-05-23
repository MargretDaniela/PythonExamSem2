from flask import Blueprint ,request , jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.category_model import Category
from app.extensions import db
from flask_jwt_extended  import create_access_token, jwt_required,get_jwt_identity, create_refresh_token

# Categories blueprint
categories = Blueprint('categories',__name__,url_prefix='/api/v1/categories')

# creating  categories
@categories.route('/create', methods=['POST'])
@jwt_required()
def createCategory():

    #Storing request values
    data = request.json
    name = data.get('name')
    description = data.get('description')

# Validations of the incoming request
    if not name or not description:
        return jsonify({
            'error': "All Fields are required"
        }), HTTP_400_BAD_REQUEST
    

    if Category.query.filter_by(name=name).first() is not None:
        return jsonify({
            'error':"Category name is already in use"
        }),HTTP_409_CONFLICT
    
    try:
        #creating a new Category
        new_category = Category(name=name,
                         description=description)
        
    
        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            'message' : name +"has been successfully created ",
            'category':{
                "name":new_category.name,
                "description":new_category.description
            }
        }), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({    
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

