# From inside the drupal directory of a working version of 
# Drupal export content into json files by content type
# The module Data Export Import must be installed first i.e.
#  drush dl data_export_import
#  drush en data_export_import -y

drush dei-ex users
drush node-export --type=blog --format=json --file=blog.json  
drush node-export --type=seminar --format=json --file=seminar.json 
drush node-export --type=glossary --format=json --file=glossary.json 
drush node-export --type=feature --format=json --file=feature.json  
drush node-export --type=book --format=json --file=book.json      
drush node-export --type=earth_image --format=json --file=earth_image.json 
drush node-export --type=space_image --format=json --file=space_image.json 
drush node-export --type=activity --format=json --file=activity.json      
drush node-export --type=article --format=json --file=article.json       
drush node-export --type=user_profile --format=json --file=profile.json
drush node-export --type=telescope_class --format=json --file=telescope_class.json
drush node-export --type=telescope --format=json --file=telescope.json
drush node-export --type=spectrograph --format=json --file=spectrograph.json
drupal  drush node-export --type=camera --format=json --file=camera.json

cp *.json /tmp/
cp *.dataset /tmp/users.dataset

# Start virtualenv of Mezzanine website and cd to the base of that project

python manage.py import_drupal_users --url=/tmp/users.dataset --mezzanine-user='admin'
python manage.py import_drupal_blog --url=/tmp/blog.json --mezzanine-user='admin'
python manage.py import_drupal_spacebook --url=/tmp/book.json --mezzanine-user='admin'