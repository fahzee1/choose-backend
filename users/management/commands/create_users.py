import csv
import sys
import pdb
from optparse import make_option
import traceback
from django.core.management.base import BaseCommand, CommandError
from users.models import UserProfile

csv.field_size_limit(sys.maxsize)

class Command(BaseCommand):
    help = 'Script used to extract date, lead id, and disposition from csv and get associated gclid to send to google'
    option_list = BaseCommand.option_list + (
        make_option('--ifile', dest='csv_file',
            help='destination where to find csv'
            ),
        make_option('--count', dest='count',
            help='how many records to create'
            ),
        make_option('--verbose', dest='verbose',
            help='Print to the screen'
            ),
        )

    def handle(self, *args, **options):
        app = lambda : None
        app.options = options
        if not options['csv_file']:
            raise CommandError('Need csv file to feed')

        if not options['count']:
            raise CommandError('Need count to feed')
        
        get_csv_data(app,options['csv_file'],options['count'])
            



def get_csv_data(app,_file,count):
    data = []
    if app.options['verbose']:
        print 'opening csv file...'

    id_start = 5000
    i = 0
    with open(_file,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for info in reader:
            i += 1
            name = info.get('Name','')
            email = info.get('Email','')
            phone = info.get('Phone','')


            name = name.replace(' ','_')

            if i == int(count):
                print 'done.. created %s' % i
                break
                
            try:
                user = UserProfile()
                user.username = name
                user.facebook_user = True
                user.fake_user = True
                user.facebook_id = id_start
                user.save()
            except:
                traceback.print_exc()
                print 'already created %s' % name

            id_start += 1
            

    print 'created %s records' % i



