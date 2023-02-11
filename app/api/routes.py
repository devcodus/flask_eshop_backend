from flask import Blueprint, request
from ..models import Post, Likes, User
from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth
from flask_cors import cross_origin, CORS
from flask_login import current_user


api = Blueprint('api', __name__)
CORS(api, origins = ['*'])

@api.route('/api/posts')
@cross_origin()
def getPosts():
    posts = Post.query.all()

    new_posts = []
    for p in posts:
        new_posts.append(p.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(posts),
        'posts': [p.to_dict() for p in posts]
    }

@api.route('/api/posts/<int:post_id>')
# @cross_origin()
def getPost(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'totalResults': 1,
            'post': 
            post.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': 'The post you are looking for does not exist.'
        }



# @api.route('/api/posts/create', methods = ["POST"])
# # @cross_origin()
# @token_auth_required
# def createPost(user):
#     data = request.json

#     title = data['title']
#     caption = data['caption']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     post = Post(title, img_url, caption, user.id)
#     post.saveToDB()
    
#     return {
#         'status': 'ok',
#         'message': 'Succesfullly created post!'
#     }

# @api.route('/api/posts/update/<post_id>', methods = ["POST"])
# @basic_auth_required
# def updatePost(user, post_id):
#     data = request.json

#     title = data['title']
#     caption = data['caption']
#     img_url = data['img_url']

#     ## for now, accept the user_id parameter from the JSON body
#     ### HOWEVER, this is not the correct way, we need to authenticate them somehow
#     #### we will cover this in BASIC/TOKEN auth

#     post = Post(title, img_url, caption, user.id)
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
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'user': user.to_dict()
    }