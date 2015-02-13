#!/bin/bash
BRANCH=`git name-rev --name-only HEAD`
docker stop lcogt_mezzanine_uwsgi 2>&1 > /dev/null
docker rm lcogt_mezzanine_uwsgi 2>&1 > /dev/null
docker stop lcogt_mezzanine_nginx 2>&1 > /dev/null
docker rm lcogt_mezzanine_nginx 2>&1 > /dev/null
docker login --username="lcogtwebmaster" --password="lc0GT!" --email="webmaster@lcogt.net"
if [ "$DEBUG" != "" ]; then
    DEBUGENV="-e DEBUG=True"
fi
docker run -d --name=lcogt_mezzanine_uwsgi -e PREFIX=$PREFIX $DEBUGENV lcogtwebmaster/lcogt:lcogt_mezzanine_$BRANCH /var/www/apps/lcogt_mezzanine/docker/bin/uwsgi.sh
docker run -d --name=lcogt_mezzanine_nginx -p 8000:8000 -e PREFIX=$PREFIX $DEBUGENV --link lcogt_mezzanine_uwsgi:lcogt_mezzanine_uwsgi lcogtwebmaster/lcogt:lcogt_mezzanine_$BRANCH /var/www/apps/lcogt_mezzanine/docker/bin/nginx.sh
if [ "$DEBUG" != "" ]; then
    docker logs -f lcogt_mezzanine_nginx &
    docker logs -f lcogt_mezzanine_uwsgi &
fi