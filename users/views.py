import pdb
import json
import traceback
from django.shortcuts import render
from django.views.generic import View
from votes.views import my_response
from django.db import IntegrityError
from votes.models import Card
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
class HttpTable(object):
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    delete = 'DELETE'

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
        try:
            user, created = UserProfile.objects.get_or_create(username=name,
                                                          facebook_id=fbID,
                                                          email=email)
        except IntegrityError:
            traceback.print_exc()
            reason = 'There was an IntegrityError creating user -- %s' % traceback.format_exc()
            return my_response(reason=reason,status_code=500)



        # Return data
        message['user'] = user.to_dict(token=True) 

        return my_response(message,success=True)

    # Not POST method so return bad response
    reason = "Only 'POST' to this endpoint"
    return my_response(reason=reason,status_code=405)

@check_token
def users(request):
    message = {}
    if request.method == HttpTable.get:
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            offset = int(offset)
            limit = int(limit)
            temp_limit = offset + limit
            users = UserProfile.objects.all()[offset:temp_limit]
            if users:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) 
        else:
            users = UserProfile.objects.all()

        message['users'] = UserProfile.queryset_to_dict(users)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        return my_response(message,success=True)


    reason = "Invalid http method"
    return my_response(reason=reason,status_code=405)

@check_token
def user_cards(request,facebook_id):
    if request.method == HttpTable.get:

        try:
            user = UserProfile.objects.get(facebook_id=facebook_id)
        except UserProfile.DoesNotExist:
            return my_response(status_code=404)

        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            offset = int(offset)
            limit = int(limit)
            temp_limit = offset + limit
            cards = user.card.all()[offset:temp_limit]
            if cards:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) 
        else:
            cards = user.card.all()

        message = {}
        message['cards'] = Card.queryset_to_dict(cards)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)

@check_token
def view_user(request,facebook_id):
    if request.method == HttpTable.get:
        try:
            user = UserProfile.objects.get(facebook_id=facebook_id)
        except UserProfile.DoesNotExist:
            reason = 'user with id %s doesnt exist' % facebook_id
            return my_response(reason=reason,status_code=404)

        message = {}
        message['user'] = user.to_dict()
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)

@check_token
def update_user(request,facebook_id):
    if request.method == HttpTable.put:
        try:
            user = UserProfile.objects.get(facebook_id=facebook_id)
        except UserProfile.DoesNotExist:
            return my_response(status_code=404)

        data = json.loads(request.body,strict=False)
        for key, value in data.iteritems():
            setattr(user,key,value)
        user.save()
        message = {}
        message['user'] = user.to_dict()
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)

@check_token
def user_object(request,facebook_id):
    if request.method == HttpTable.get:
        return view_user(request,facebook_id)

    elif request.method == HttpTable.put:
        return update_user(request,facebook_id)

    else:
        reason = "Invalid HTTP method"
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



