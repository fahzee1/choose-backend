import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from votes.models import Choose
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
    
    count = choose.lists.count()
    if count > 0:
        choose.send_notification()
        cache.clear()
    if verbose:
        print 'done'

    




