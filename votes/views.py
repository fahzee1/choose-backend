import pdb
import uuid
import json
import base64
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import render
from models import TheVote,Category
from users.models import UserProfile
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware_with_args, decorator_from_middleware
from users.middleware import TokenCheck

check_token = decorator_from_middleware(TokenCheck)

"""
Token authentication must be in the form

Authorization:9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

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

def my_response(data={},success=False,reason='Failed request',status_code=200):
    if status_code == 404:
        reason = 'Object not found'

    if status_code == 200 or status_code == 201:
        reason = ''

    message = {}
    message['success'] = success
    message['reason'] = reason
    if data:
        message['data'] = data



    response = JsonResponse(message)
    response.status_code = status_code
    return response


#@check_token
def votes(request,pk):
    message = {'success':False}

    if request.method == HttpTable.put:
        data = json.loads(request.body)
        vote = TheVote.objects.filter(pk=pk)[0]
        if not vote:
            return my_response(status_code=404)

        update = data.get('update',None)
        value = data.get('value',None)
        if update == 'vote':
            if value == 'yes':
                # update yes count
                vote.total_votes_yes = F('total_votes_yes') + 1
                vote.save()

            elif value == 'no':
                #update no count
                vote.total_votes_no = F('total_votes_no') + 1
                vote.save()

            else:
                pass

            message['success'] = True
            return my_response(success=True)

        if update == 'facebook':
            if value == True:
                vote.facebook_shared = True
                vote.save()
                message['success'] = True
                return my_response(success=True)


    elif request.method == HttpTable.delete:
        try:
            vote = TheVote.objects.get(pk=pk)
            vote.delete()
            return my_response(success=True)

        except TheVote.DoesNotExist:
            return my_response(success=False,reason='')

    elif request.method == HttpTable.get:
        try:
            vote = TheVote.objects.get(pk=pk)
            data = vote.to_dict()
            return my_response(data,success=True)

        except TheVote.DoesNotExist:
            reason = 'Vote with pk %s doesnt exist' % pk
            return my_response(reason=reason,status_code=404)
    else:
        reason = "%s method not allowed at this endpoint" % request.method 
        return my_response(reason=reason,status_code=405)

@check_token
def category(request):
    message = {'success':False}
    http_method = HttpTable.get

    if request.method == http_method:
        categories = Category.list_categories()
        del message['success']
        message['categories'] = categories
        return my_response(message,success=True)

    reason = "%s method not allowed at this endpoint" % request.method 
    return my_response(status_code=405)




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

        message['votes'] = TheVote.queryset_to_dict(votes)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)
        del message['success']

        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)


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

        message['votes'] = TheVote.queryset_to_dict(featured)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        del message['success']
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)


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
            reason = 'fb id:%s user doesnt exist' % facebook_id
            return my_response(reason=reason,status_code=404)

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            reason = 'category id:%s category doesnt exist' % category
            return my_response(reason=reason,status_code=404)

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

    
        return my_response(success=True,status_code=201)



    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)