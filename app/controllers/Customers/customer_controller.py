from flask import Blueprint ,request , jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
import validators
from app.models.customer_model import Customer
from app.extensions import db
from flask_jwt_extended  import  jwt_required,get_jwt_identity

# Customers blueprint
customers = Blueprint('users',__name__,url_prefix='/api/v1/customers')

# creating  customers
@customers.route('/create', methods=['POST'])
def createCustomer():

    #Storing request values
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

# Validations of the incoming request
    if not first_name or not last_name or not email:
        return jsonify({
            'error': "All Fields are required"
        }), HTTP_400_BAD_REQUEST
    

    if Customer.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error':"Email is already in use"
        }),HTTP_409_CONFLICT
    
    try:
        #creating a new customer
        new_customer = Customer(first_name= first_name,
                                last_name=last_name,
                                created_at = created_at,
                                updated_at = updated_at
                         )
        db.session.add(new_customer)
        db.session.commit()
        customer_names = new_customer.full_name()

        return jsonify({
            'message' : customer_names +"has been successfully created ",
            'customer':{
                "first_name":new_customer.first_name,
                "last_name":new_customer.last_name,
                "email":new_customer.email,
                "created_at":new_customer.created_at,
                "updated_at":new_customer.created_at
            }
        }), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({    
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

