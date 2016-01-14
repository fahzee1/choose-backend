import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from votes.models import Choose, CardList
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Notify users that cards are ready'
    option_list = BaseCommand.option_list + (
       make_option('--verbose', dest='verbose',
            help='Print to the screen'
            ),
        )

    def handle(self, *args, **options):
        grab_choose(options)
            



def grab_choose(options):
    verbose = options['verbose']
    if verbose:
        print 'Grabbing todays cards'

    choose = Choose.objects.first()

    if verbose:
        print 'Grabbed %s now sending notification' % choose
    
    # Get todays push notification message, blase it and clear cache
    cardlists = choose.lists.all()
    if cardlists.count > 0:
        choose.send_notification()
        cache.clear()

        # loop though each card list and create new uuid's so clients purge cache
        if verbose:
            print 'Creating new uuids for lists'
        for s in cardlists:
            if verbose:
                print 'done for %s' % s
            s.new_uuid(save=True)

        if verbose:
            print 'grabbing featured list'
        # grab featured list and notify each creator of a card in the list that their card 
        # is being featured
        featured = cardlists.filter(name='Featured')
        if featured:
            featured = featured[0]
            if verbose:
                print 'preparing to notify all featured'
            for i in featured.cards.all():
                print 'notifying %s' % i
                i.notify_featured()
    if verbose:
        print 'done'

    




