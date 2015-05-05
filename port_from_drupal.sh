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

cp *.json fixtures/
cp *.dataset fixtures/users.dataset

# To load all this data use the script in the docker bin
docker/bin/loaddata.sh
