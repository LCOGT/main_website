#!/bin/bash
#cd /var/www/apps/lcogt_mezzanine
python manage.py createdb --noinput --nodata
python manage.py createinitialrevisions
python manage.py import_drupal_users --url=fixtures/users.dataset --mezzanine-user='admin'
python manage.py import_drupal_blog --url=fixtures/blog.json --user='lcogt_drupal' --password='aSt3r0!d' --host='db01sba.lco.gtn' --dbname='live_lcogt_drupal7_32' --mezzanine-user='admin'
python manage.py import_drupal_spacebook --url=fixtures/book.json --user='lcogt_drupal' --password='aSt3r0!d' --host='db01sba.lco.gtn' --dbname='live_lcogt_drupal7_32'
python manage.py import_drupal_activities --url=fixtures/activity.json --user='lcogt_drupal' --password='aSt3r0!d' --host='db01sba.lco.gtn' --dbname='live_lcogt_drupal7_32'
python manage.py import_drupal_seminar --url=fixtures/seminar.json --user='lcogt_drupal' --password='aSt3r0!d' --host='db01sba.lco.gtn' --dbname='live_lcogt_drupal7_32'
python manage.py import_misc_content --url=fixtures/misc.json --user='lcogt_drupal' --password='aSt3r0!d' --host='db01sba.lco.gtn' --dbname='live_lcogt_drupal7_32'
python manage.py loaddata fixtures/blocks.json

#lcogt_drupal:aSt3r0!d@127.0.0.1:4040/live_lcogt_drupal7