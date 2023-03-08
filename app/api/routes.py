from flask import Blueprint, request, jsonify
from ..models import Posters, User, Cart
from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth, token_auth
from flask_cors import cross_origin, CORS
from flask_login import current_user
import requests


api = Blueprint('api', __name__)


@api.route('/api/populate', methods = ['GET'])
@cross_origin()
def populate():

    url = "https://api.nasa.gov/planetary/apod?api_key=kFHR3AFVVyE6UWjaIGXtd1dHO4ey1Z9SZcGlG6J0&start_date=2022-01-01&end_date=2023-02-01"

    monthly_apod = {}

    response = requests.get(url)
    if response.status_code == 200:
        apod_month_list = response.json()
        # print(apod_month_list)
        for apod in apod_month_list:
            monthly_apod['title'] = apod['title']
            monthly_apod['img_url'] = apod['url']
            monthly_apod['price'] = 20 # RNG here next
            monthly_apod['media_type']=apod['media_type']

            title = monthly_apod['title']
            img_url = monthly_apod['img_url']
            price =  monthly_apod['price']
            quantity = 100
            media_type = monthly_apod['media_type']

            poster = Posters(title, img_url, price, quantity, media_type)
            poster.saveToDB()


            continue
            # return render_template('home.html', posts = posts)
    posters = Posters.query.all()
    print(posters)
    # return jsonify([posters.to_dict() for poster in posters]), 200, {'Content-Type': 'application/json'}
    return {
        'status': 'ok',
        'totalResults': len(posters),
        'posters': [p.to_dict() for p in posters]
    }
  
@api.route('/api/posters')
@cross_origin()
def getPrints():
    posters = Posters.query.all()
    print(posters)

    new_posters = []
    for p in posters:
        new_posters.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(posters),
        'posters': [p.to_dict() for p in posters]
    }

@api.route('/api/cart')
@cross_origin()
def getCart():
    cart = Cart.query.all()

    cart_items = []
    for p in cart:
        cart_items.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(cart),
        'posters': [p.to_dict() for p in cart]
    }

@api.post('/api/cart/add')
@token_auth.login_required
def addToCartAPI():
    data = request.json
    user = token_auth.current_user()
    poster_id = data['posterId']
    # poster = Posters.query.get(id)
    c = Cart(user.id, poster_id)
    c.saveToDB()
    return {
        'status': 'ok',
        # 'message': f'Succesfully added "{poster.title}" to your cart!'
    }   

@api.get('/api/cart/get')
@token_auth.login_required
def getCartAPI():
    user = token_auth.current_user()
    cart = [Posters.query.get(c.poster_id).to_dict() for c in user.cart]
    return {
        'status': 'ok',
        'cart': cart
    }

@api.post('/api/cart/remove')
@token_auth.login_required
def removeFromCartAPI():
    data = request.json
    user = token_auth.current_user()

    poster_id = data['posterId']
    

    c = Cart.query.filter_by(user_id=user.id).filter_by(poster_id=poster_id).first()
    print(c)
    c.deleteFromDB()
    
    return {
        'status': 'ok',
        'message': 'Succesfully removed item from cart!'
    }

# @api.post('/api/cart/removeall')
# @token_auth.login_required
# def removeAllFromCartAPI():
#     data = request.json
#     user = token_auth.current_user()

#     # poster_id = data['posterId']
    

#     c = Cart.query.filter_by(user_id=user.id).all()
#     print(c)
#     c.deleteFromDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfully removed item from cart!'
#     }

@api.post('/api/cart/removeall')
@token_auth.login_required
def removeAllFromCartAPI():
    user = token_auth.current_user()
    c = Cart.query.filter_by(user_id=user.id).all() #this was cart_items as in an array
    for item in c:
        item.deleteFromDB()
    return {
        'status': 'ok',
        'message': 'Successfully removed all items from cart!'
    }


@api.route('/api/posters/<int:poster_id>')
@cross_origin()
def getPoster(poster_id):
    poster = Posters.query.get(poster_id)
    if poster:
        return {
            'status': 'ok',
            'totalResults': 1,
            'poster': 
            poster.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'The post you are looking for does not exist.'
        }



########## CONVERT THIS TO ADDTOCART ROUTE##########

# @api.route('/api/posts/create', methods = ["POST"])
# # @cross_origin()
# @token_auth_required
# def addToCart(user):
    
#     data = request.json ## WHERE IS THIS COMING FROM?

#     print = data['print_id']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     cart = Cart(user.id, print_id, quantity)
#     cart.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly added to Cart!'
#     }

# @api.route('/api/posts/update/<post_id>', methods = ["POST"])
# @basic_auth_required
# def updatePost(user, post_id):
#     data = request.json

#     title = data['title']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     post = Post(title, img_url, user.id)
#     post.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly created post!'
#     }

################# AUTH ROUTES API ####################

@api.route('/api/signup', methods=["POST"])
@cross_origin()
def signUpPageAPI():
    headers = request.headers
    print(headers)

    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']
    


    # add user to database
    user = User(username, email, password)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': "Successfully created an account!"
    }

@api.route('/api/login', methods=["POST"])
@cross_origin()
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'message': 'Login successful!',
        'user': user.to_dict()
    }