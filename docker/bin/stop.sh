#!/bin/bash
docker stop lcogt_mezzanine_uwsgi 2>&1 > /dev/null
docker rm lcogt_mezzanine_uwsgi 2>&1 > /dev/null
docker stop lcogt_mezzanine_nginx 2>&1 > /dev/null
docker rm lcogt_mezzanine_nginx 2>&1 > /dev/null