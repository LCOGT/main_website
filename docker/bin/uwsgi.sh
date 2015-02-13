#!/bin/bash
touch /var/log/uwsgi.log
tail --pid $$ -f /var/log/uwsgi.log &
/usr/bin/uwsgi --ini /var/www/apps/lcogt_mezzanine/docker/config/uwsgi.ini