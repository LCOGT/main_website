# From inside the drupal directory of a working version of 
# Drupal export content into json files by content type
# The module Data Export Import must be installed first i.e.
#  drush dl data_export_import
#  drush en data_export_import -y

drush dei-ex users
drush node-export --type=blog --format=json --file=blog.json  
drush node-export --type=seminar --format=json --file=seminar.json 
drush node-export --type=book --format=json --file=book.json      
drush node-export --type=activity --format=json --file=activity.json      

cp *.json /tmp/
cp *.dataset /tmp/users.dataset

# Start virtualenv of Mezzanine website and cd to the base of that project
# Database settings need to be added for the Drupal database and database user

python manage.py createdb --noinput --nodata
python manage.py createinitialrevisions
python manage.py import_drupal_users --url=/tmp/users.dataset --mezzanine-user='admin'
python manage.py import_drupal_blog --url=data/blog.json --user='' --password='' --host='' --dbname='' --mezzanine-user='admin'
python manage.py import_drupal_spacebook --url=/tmp/book.json --user='' --password='' --host='' --dbname=''
python manage.py import_drupal_activities --url=/tmp/activity.json --user='' --password='' --host='' --dbname=''
python manage.py import_drupal_seminar --url=/tmp/seminar.json --user='' --password='' --host='' --dbname=''
python manage.py import_misc_content --url=/tmp/misc.json --user='' --password='' --host='' --dbname=''