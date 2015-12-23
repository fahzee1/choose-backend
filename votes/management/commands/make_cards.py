import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from votes.models import CardList


class Command(BaseCommand):
    help = 'Gets cards ready for deployment'
    option_list = BaseCommand.option_list + (
       make_option('--verbose', dest='verbose',
            help='Print to the screen'
            ),
        )

    def handle(self, *args, **options):
        app = lambda : None
        app.options = options
        get_cards(app)
            



def get_cards(app):
    data = []
    if app.options['verbose']:
        print 'fetching cards without image_url...'

    lists = CardList.objects.filter(approved=True,active=True)
    if lists.count():
        print 'lists %s' % lists
        print ' have count %s' % lists.count()
    else:
        print 'no lists to speak of'

    




