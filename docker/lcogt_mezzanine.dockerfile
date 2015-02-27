#
# lcogt_mezzanine dockerfile
#
FROM lcogtwebmaster/lcogt:webbase
MAINTAINER LCOGT <webmaster@lcogt.net>
RUN yum -y update; yum clean all

ADD . /var/www/apps/lcogt_mezzanine
WORKDIR /var/www/apps/lcogt_mezzanine
RUN cat docker/config/nginx.conf | envsubst '$PREFIX $LCOGT_MEZZANINE_UWSGI_PORT_8101_TCP_ADDR' > /etc/nginx/nginx.conf

RUN pip install -r pip-requirements.txt
RUN python manage.py collectstatic --noinput;
RUN chmod 777 /var/www/apps/lcogt_mezzanine/files/.thumbnails/
# RUN mount_nfs -o resvport mfs.lco.gtn:/data4/webfiles /var/www/apps/lcogt_mezzanine/files

ENV PYTHONPATH /var/www/apps
ENV DJANGO_SETTINGS_MODULE lcogt_mezzanine.settings
ENV BRANCH ${BRANCH}
ENV BUILDDATE ${BUILDDATE}

EXPOSE 8100
EXPOSE 8101
