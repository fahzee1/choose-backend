import pdb
import uuid
import json
import base64
from django.core.files.base import ContentFile
from django.shortcuts import render
from models import TheVote,Category
from users.models import UserProfile
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware_with_args, decorator_from_middleware
from users.middleware import TokenCheck

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
def show_categories(request,pk):
    message = {'success':False}
    http_method = HttpTable.get
    if request.method == http_method:
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            votes = TheVote.objects.filter(category__pk=pk)[int(offset):int(limit)]
            if votes:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) + 1

        else:
            votes = TheVote.objects.filter(category__pk=pk)

        message['success'] = True
        message['data'] = TheVote.queryset_to_dict(votes)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        return JsonResponse(message)

    message['reason'] = "Only '%s' to this endpoint" % http_method
    response = JsonResponse(message)
    response.status_code = 405
    return response
    return JsonResponse(message)


#@check_token
def show_featured(request):
    message = {'success':False}
    http_method = HttpTable.get
    if request.method == http_method:
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            featured = TheVote.objects.filter(featured=True)[int(offset):int(limit)]
            if featured:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) + 1
        else:
            featured = TheVote.objects.filter(featured=True)

        message['success'] = True
        message['data'] = TheVote.queryset_to_dict(featured)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        return JsonResponse(message)

    message['reason'] = "Only '%s' to this endpoint" % http_method
    response = JsonResponse(message)
    response.status_code = 405
    return response


@check_token
def create_vote(request):
    message = {'success':False}
    http_method = HttpTable.post
    if request.method == http_method:
        params = ['facebook_id','category_id','image','left_label','right_label']
        data = json.loads(request.body)
        for name in params:
            if name not in data.keys():
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response


        facebook_id = data['facebook_id']
        category_id = data['category_id']
        imageData = data['image']
        left_label = data['left_label']
        right_label = data['right_label']

        try:
            user = UserProfile.objects.get(facebook_id=facebook_id)

        except UserProfile.DoesNotExist:
            message['reason'] = 'fb id:%s user doesnt exist' % facebook_id
            response = JsonResponse(message)
            response.status_code = 404
            return response

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            message['reason'] = 'category id:%s category doesnt exist' % category
            response = JsonResponse(message)
            response.status_code = 404

        image = base64.b64decode(imageData)
        randomNumbers = str(uuid.uuid4())[:10]
        imagename = '%s-%s.jpg' % (user.username,randomNumbers)
        vote = TheVote()
        vote.user = user
        vote.category = category
        vote.right_label = right_label
        vote.left_label = left_label
        vote.image.save(imagename,ContentFile(image))
        vote.save()

        message['success'] = True
        response = JsonResponse(message)
        response.status_code = 201
        return response





    message['reason'] = "Only '%s' to this endpoint" % http_method
    response = JsonResponse(message)
    response.status_code = 405
    return JsonResponse(message)