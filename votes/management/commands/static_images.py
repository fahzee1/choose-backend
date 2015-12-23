import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from votes.models import Card


class Command(BaseCommand):
    help = 'save each images.url attribute in image url field'
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

    cards = Card.objects.filter(image_url='')
    print 'looping through %s cards' % cards.count()

    for i in cards:
        if i.image:
            i.image_url = i.image.url
            i.save()
            print 'saving %s' % i
            

    print 'Done!'




