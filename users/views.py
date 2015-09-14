import pdb
import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse,HttpResponseBadRequest,JsonResponse
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
            message['reason'] = 'No token provided'
            response = JsonResponse(message)
            response.status_code = 403
            return response

        tokenObj = get_object_or_404(Token,key=token)
        message['user'] = tokenObj.user.to_dict(token=True)
        message['success'] = True
        return JsonResponse(message)

    message['reason'] = "Only 'GET' to this endpoint"
    response = JsonResponse(message)
    response.status_code = 405
    return response





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
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response


        name = data['name']
        email = data['email']
        fbID = data['facebook_id']
        name = name.replace(' ','_')
        user, created = UserProfile.objects.get_or_create(username=name,
                                                          facebook_id=fbID)

        # Return data
        message['success'] = True
        message['user'] = user.to_dict() 

        return JsonResponse(message)

    # Not POST method so return bad response
    message['reason'] = "Only 'POST' to this endpoint"
    response = JsonResponse(message)
    response.status_code = 405 
    return response


@check_token
def user_search(request):

    message = {'success':False}

    if request.method == 'POST':
        # Check correct params passed in
        params = ['name']
        data = json.loads(request.body)
        for name in params:
            if name not in data.keys():
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response


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




    message['reason'] = "Only 'GET' to this endpoint"
    response = JsonResponse(message)
    response.status_code = 405
    return response



@check_token
def user_object(request,pk):
    """
    /users/:pk endpoint
    """
    profile = get_object_or_404(UserProfile,pk=pk)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        pass

    if request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
