#-----------------------------------------------------------------------------------------------------------------------
# lcogt_mezzanine docker image makefile
#
# 'make' will create the docker image needed to run the lcogt_mezzanine app:
#    lcogtwebmaster/lcogt:lcogt_mezzanine_$BRANCH
#
# where $BRANCH is the git branch name presently in use.
#
# Once built, this image can be pushed up the docker hub repository via 'make install',
# and can then be run via something like:
#
# docker run -d --name=lcogt_mezzanine_wsgi -e PREFIX='' lcogtwebmaster/lcogt:lcogt_mezzanine_$BRANCH /var/www/apps/lcogt_mezzanine/docker/bin/uwsgi.sh
# docker run -d --name=lcogt_mezzanine_nginx -p 8000:8000 -e PREFIX='' --link lcogt_mezzanine_wsgi:lcogt_mezzanine_wsgi lcogtwebmaster/lcogt:lcogt_mezzanine_$BRANCH /var/www/apps/lcogt_mezzanine/docker/bin/nginx.sh
#
# at which point the app will be exposed on the target host at port 8000
#
# Doug Thomas
# LCOGT
#
#-----------------------------------------------------------------------------------------------------------------------
NAME := lcogtwebmaster/lcogt
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
BUILDDATE := $(shell date +%Y%m%d%H%M)
TAG0 := webbase
TAG1 := lcogt_mezzanine_${BRANCH}
PREFIX := ''

.PHONY: all lcogt_mezzanine test login install

all: webbase lcogt_mezzanine test

sudo:
	@if ! sudo -n whoami | grep -q -F root; then echo "  You must be able to sudo without a password; run visudo as root," && echo "  such that you have a line like 'ADMINS ALL = NOPASSWD:ALL'"; false; fi;

login:
	docker login --username="lcogtwebmaster" --password="lc0GT!" --email="webmaster@lcogt.net"

webbase:
	cat docker/webbase.dockerfile | /usr/local/opt/gettext/bin/envsubst > Dockerfile && \
	docker build -t $(NAME):$(TAG0) --rm . && rm -f Dockerfile

lcogt_mezzanine:
	export BUILDDATE=${BUILDDATE} && \
	export BRANCH=${BRANCH} && \
	export PREFIX=${PREFIX} && \
	cat docker/lcogt_mezzanine.dockerfile | /usr/local/opt/gettext/bin/envsubst > Dockerfile && \
	docker build -t $(NAME):$(TAG1) --rm . && rm -f Dockerfile

test:
	env NAME=${NAME} VERSION=${TAG1} ./test/runtests.sh

install: test login
	@if ! docker images ${NAME} | awk '{ print $$2 }' | grep -q -F ${TAG1}; then echo "${NAME}:${TAG1} is not yet built. Please run 'make'"; false; fi
	docker push ${NAME}:${TAG1}
