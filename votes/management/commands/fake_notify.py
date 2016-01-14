import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from votes.models import CardList
from django.utils import timezone


TIMES = {
    'early_morning':[0,1,2,3,4,5,6],
    'morning':[7,8,9,10,11],
    'afternoon':[12,13,14,15,16,17],
    'evening':[18,19,20],
    'night':[21,22,23]
}

class Command(BaseCommand):
    help = 'Notify users that cards are ready'
    option_list = BaseCommand.option_list + (
       make_option('--verbose', dest='verbose',
            help='Print to the screen'
            ),
        )

    def handle(self, *args, **options):
        notify(options)
            



def notify(options):
    verbose = options['verbose']
    
    now = timezone.localtime(timezone.now())
    if now.hour in TIMES['early_morning'] or now.hour in TIMES['night']:
        if verbose:
            print 'time is either too late or too early to run'
        return

    if verbose:
        print 'Grabbing cards that need to send out notifications'

    lists = CardList.objects.filter(active=True,approved=True).prefetch_related('cards')
    if verbose:
        print 'Grabbed %s cards lists that are fake active' % lists.count()
    
    if verbose:
        print ' preparing to loop through cards'
    for i in lists:
        cards = i.cards.all()
        for c in cards:
            if c.fake_notification_count > 9:
                if verbose:
                    print '%s has been faked more then 9 times' % c
                    print 'marking false'
                c.fake_active = False
                c.save()
                return
            if verbose:
                print 'faking %s' % c
            c.fake_votes()
            c.fake_notification_count = c.fake_notification_count + 1
            c.save()

    if verbose:
        print 'done'
