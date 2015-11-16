import pdb
import json
from django.shortcuts import render
from django.views.generic import View
from votes.views import my_response
from models import UserProfile, Token
from django.shortcuts import get_object_or_404
from django.utils.decorators import decorator_from_middleware_with_args, decorator_from_middleware
from middleware import TokenCheck

check_token = decorator_from_middleware(TokenCheck)
"""
Token authentication must be in the form

Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Status codes
400 = Bad request
404 = Not Found
403 = Forbidden
405 = Not Allowed
"""

@check_token
def get_me(request):
    message = {'success':False}
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION',None)
        if not token:
            reason = 'No token provided'
            return my_response(reason=reason,status_code=403)

        tokenObj = get_object_or_404(Token,key=token)
        message['user'] = tokenObj.user.to_dict(token=True)
        del message['success']
        return my_response(message,success=True)

    reason = "Only 'GET' to this endpoint"
    return my_response(reason=reason,status_code=405)





def login(request):
    """
    Login with Facebook
    """
    message = {'success':False}

    if request.method == 'POST':
        # Check correct params passed in
        params = ['name','email','facebook_id']
        data = json.loads(request.body)
        for name in params:
            if name not in data.keys():
                reason = 'Missing %s param' % name
                return my_response(reason=reason,status_code=400)


        name = data.get('name',None)
        email = data.get('email',None)
        fbID = data.get('facebook_id',None)
        name = name.replace(' ','_')
        user, created = UserProfile.objects.get_or_create(username=name,
                                                          facebook_id=fbID)

        # Return data
        del message['success']
        message['user'] = user.to_dict(token=True) 

        return my_response(message,success=True)

    # Not POST method so return bad response
    reason = "Only 'POST' to this endpoint"
    return my_response(reason=reason,status_code=405)


@check_token
def user_search(request):

    message = {'success':False}

    if request.method == 'POST':
        # Check correct params passed in
        params = ['name']
        data = json.loads(request.body)
        for name in params:
            if name not in data.keys():
                reason = 'Missing %s param' % name
                return my_response(reason=reason,status_code=400)


        name = data['name']
        if ' ' in name:
            name = name.replace(' ','_')

        users = UserProfile.objects.filter(username__icontains=name)
        user_data = {}
        message['success'] = True
        if users:
            user = users[0]
            user_data['name'] = user.name
            user_data['first_name'] = user.first_name
            user_data['last_name'] = user.last_name
            user_data['facebook_id'] = user.facebook_id

        message['data'] = user_data
        return JsonResponse(message)




    reason = "Only 'GET' to this endpoint"
    return my_response(reason=reason,status_code=405)



