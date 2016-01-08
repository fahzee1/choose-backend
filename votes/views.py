import pdb
import uuid
import json
import base64
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import render
from models import Card, ShareText, CardList
from users.models import UserProfile
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware_with_args, decorator_from_middleware
from users.middleware import TokenCheck
from django.views.decorators.cache import cache_page
from django.core.cache import cache


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
        reason = 'Object not found - %s' % reason

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


def get_cached_cards(request):
    return cache.get(request.path)

def cache_cards_page(request,data,expires=60*60):
    cache.set(request.path,data,expires)




#cache for 1 hour
@check_token
def show_cards(request):
    message = {'success':False}
    status_code = 200
    http_method = HttpTable.get
    query = request.GET.get('q',None)
    uuid = request.GET.get('uuid',None)

    # first check cache
    """
    cached_cards = get_cached_cards(request)
    if cached_cards:
        if str(cached_cards['uuid']) == uuid:
            reason = "No new data for this category"
            return my_response(reason=reason,status_code=222)
        return my_response(cached_cards,success=True)
    """



    # Only get requests
    if request.method == http_method:
        #get limit and offset from client if there
        limit = request.GET.get('limit',None)
        offset = request.GET.get('offset',None)
        newOffset = None
        if limit and offset:
            #if we have limi and offset convert them to ints
            offset = int(offset)
            limit = int(limit)
            temp_limit = offset + limit
            # try getting cards
            try:
                category = CardList.objects.select_related().get(name=query)
                # check for uuid to see if we need to return new data or nothing
                if uuid:
                    if uuid == str(category.uuid):
                        reason = "No new data for this category"
                        return my_response(reason=reason,status_code=222)

                all_cards = category.cards.all()[offset:temp_limit]
                if all_cards:
                    # only return this if we have data so client knows to stop fetching
                    newOffset = int(limit) + int(offset)
            except CardList.DoesNotExist:
                reason = "CardList object does not exist"
                return my_response(reason=reason,status_code=400) 
        else:
            # if no limit or offset just return the last 100 objects max
            try:
                category = CardList.objects.select_related().get(name=query)
                # check for uuid to see if we need to return new data or nothing
                if uuid:
                    if uuid == str(category.uuid):
                        reason = "No new data for this category"
                        return my_response(reason=reason,status_code=222)

                all_cards = category.cards.all()[:100]
            except CardList.DoesNotExist:
                reason = "CardList object does not exist"
                return my_response(reason=reason,status_code=400)

        cards = CardList.queryset_to_dict(all_cards)
        message['cards'] = cards
        message['uuid'] = str(category.uuid)
        cache_cards_page(request,message,60*60)
        if newOffset:
            message['next_offset'] = str(newOffset)
            message['next_limit'] = str(limit)

        del message['success']
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)


@check_token
def update_card(request,id):
    message = {'success':False}
    http_method = HttpTable.put
    if request.method == http_method:
        data = json.loads(request.body,strict=False)
        card = Card.objects.filter(id=id)[0]
        if not card:
            return my_response(status_code=404)

        for key, value in data.iteritems():
            setattr(card,key,value)

        card.save()
        return my_response(success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)

@cache_page(60*10)
@check_token
def view_card(request,id):
    message = {}
    if request.method == HttpTable.get:
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
            return my_response(status_code=404)

        message['card'] = card.to_dict()
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)

@check_token
def card_vote(request,id,vote):
    message = {'success':False}
    http_method = HttpTable.post
    if request.method == http_method:
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
            return my_response(status_code=404)
            
        if int(vote) == 1:
            # update left count
            card.left_votes_count = F('left_votes_count') + 1
            card.save()

        elif int(vote) == 2:
            #update right count
            card.right_votes_count = F('right_votes_count') + 1
            card.save()

        else:
            reason = "'%s' vote either isnt 1 or 2 or isnt in the right format" % vote
            return my_response(reason=reason,status_code=400)

        message['success'] = True
        return my_response(success=True)

    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)


@check_token
def delete_card(request,id):
    message = {'success':False}
    http_method = HttpTable.delete
    if request.method == http_method:
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
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
        creator_name = data.get('creator_name',None)

        if question_type != settings.QUESTION_TYPE_A_B and question_type != settings.QUESTION_TYPE_YES_NO:
            return my_response(reason='Not valid question type. 100 or 101',status_code=400)

        

        #see if we need to get or create fake user first
        if creator_name:
            user, created = UserProfile.objects.get_or_create(username=creator_name)
            if created:
                # get last user's facebook id and increment it to add to fake user
                last_user = UserProfile.objects.last()
                last_id = long(last_user.facebook_id)
                last_id += 1
                user.facebook_id = last_id
                user.fake_user = True
                user.save()

        if not user:
            try:
                user = UserProfile.objects.get(facebook_id=facebook_id)
            except UserProfile.MultipleObjectsReturned:
                user = UserProfile.objects.filter(facebook_id=facebook_id)[0]
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
        message['card'] = card.to_dict();
        return my_response(message,success=True,status_code=201)



    reason = "Only '%s' to this endpoint" % http_method
    return my_response(reason=reason,status_code=405)

def cards(request):
    message = {'success':False}
    if request.method == HttpTable.get:
        # get all cards
        return show_cards(request)

    elif request.method == HttpTable.post:
        # create card
        return create_card(request)
    else:
        reason = "Invalid http method (GET or POST)"
        return my_response(reason=reason,status_code=405)

def cards_object(request,id):
    if request.method == HttpTable.delete:
        # delete card with id
        return delete_card(request,id)

    elif request.method == HttpTable.put:
        # update card with id
        return update_card(request,id)

    elif request.method == HttpTable.get:
        # view card with id
        return view_card(request,id)

    else:
        reason = "Invalid http method (DELETE or PUT, GET)"
        return my_response(reason=reason,status_code=405)


@check_token
def share_text(request):
    message = {}
    if request.method == HttpTable.get:
        message['share_text'] = ShareText.get_lastest_share_text()
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)


@check_token
def lists(request):
    message = {}
    if request.method == HttpTable.get:
        lists = CardList.objects.filter(approved=True)
        message['lists'] = CardList.queryset_to_dict(lists)
        return my_response(message,success=True)

    reason = "Only '%s' to this endpoint" % HttpTable.get
    return my_response(reason=reason,status_code=405)



    

