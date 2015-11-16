import pdb
import uuid
import json
import base64
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import render
from models import Card
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



@check_token
def show_cards(request):
    message = {'success':False}
    http_method = HttpTable.get
    if request.method == http_method:
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            all_cards = Card.objects.filter(featured=False)[int(offset):int(limit)]
            if all_cards:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) + 1
        else:
            all_cards = Card.objects.filter(featured=False)

        message['cards'] = Card.queryset_to_dict(all_cards)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        del message['success']
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)

@check_token
def show_featured(request):
    message = {'success':False}
    http_method = HttpTable.get
    if request.method == http_method:
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            featured = Card.objects.filter(featured=True)[int(offset):int(limit)]
            if featured:
                # only return this if we have data so client knows to stop fetching
                newOffset = int(limit) + int(offset) + 1
        else:
            featured = Card.objects.filter(featured=True)

        message['votes'] = Card.queryset_to_dict(featured)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        del message['success']
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)

@check_token
def update_card(request):
    message = {'success':False}
    if request.method == HttpTable.put:
        params = ['update_type','value','card_id']
        data = json.loads(request.body,strict=False)
        for name in params:
            if name not in data.keys():
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response


        update_type = data.get('update_type',None)
        value = data.get('value',None)
        card_id = data.get('card_id',None)

        card = Card.objects.filter(id=card_id)[0]
        if not card:
            return my_response(status_code=404)

        if update_type == 'vote':
            if value == 'left':
                # update left count
                card.left_votes_count = F('left_votes_count') + 1
                card.save()

            elif value == 'right':
                #update right count
                card.right_votes_count = F('right_votes_count') + 1
                card.save()


            else:
                pass

            message['success'] = True
            return my_response(success=True)

        if update == 'facebook':
            if value == True:
                card.facebook_shared = True
                card.save()
                message['success'] = True
                return my_response(success=True)


@check_token
def delete_card(request):
    message = {'success':False}
    http_method = HttpTable.delete
    if request.method == http_method:
        params = ['card_id']
        data = json.loads(request.body)
        for name in params:
            if name not in data.keys():
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response

        card_id = data.get('card_id',None)
        card = Card.objects.filter(id=card_id)[0]
        if not card:
            return my_response(status_code=404)
        card.delete()
        return my_response(success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)

@check_token
def create_card(request):
    message = {'success':False}
    http_method = HttpTable.post
    if request.method == http_method:
        params = ['facebook_id','image','question','question_type']
        data = json.loads(request.body,strict=False)
        for name in params:
            if name not in data.keys():
                message['reason'] = 'Missing %s param' % name
                response = JsonResponse(message)
                response.status_code = 400
                return response


        facebook_id = data['facebook_id']
        imageData = data['image']
        question = data['question']
        question_type = data['question_type']
        if question_type != settings.QUESTION_TYPE_A_B and question_type != settings.QUESTION_TYPE_YES_NO:
            return my_response(reason='Not valid question type. 100 or 101',status_code=400)

        try:
            user = UserProfile.objects.get(facebook_id=facebook_id)

        except UserProfile.DoesNotExist:
            reason = 'fb id:%s user doesnt exist' % facebook_id
            return my_response(reason=reason,status_code=404)

        
        image = base64.b64decode(imageData)
        randomNumbers = str(uuid.uuid4())[:10]
        imagename = '%s-%s.jpg' % (user.username,randomNumbers)
        card = Card()
        card.user = user
        card.question = question
        card.question_type = question_type
        card.image.save(imagename,ContentFile(image))
        card.save()
        message['card_id'] = card.id;
        return my_response(message,success=True,status_code=201)



    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)