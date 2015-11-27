################################################################################
#
# Runs the LCOGT Python Django Mezzanine webapp using nginx + uwsgi
#
# The decision to run both nginx and uwsgi in the same container was made because
# it avoids duplicating all of the Python code and static files in two containers.
# It is convenient to have the whole webapp logically grouped into the same container.
#
# Build with
# docker build -t docker.lcogt.net/mezzanine:bootstrap .
#
# Push to Registry with
# docker push docker.lcogt.net/mezzanine:bootstrap
#
################################################################################

FROM centos:centos7
MAINTAINER LCOGT <webmaster@lcogt.net>

# nginx (http protocol) runs on port 80
EXPOSE 80
ENTRYPOINT [ "/init" ]

# Setup the Python Django environment
ENV PYTHONPATH /var/www/apps
ENV DJANGO_SETTINGS_MODULE lcogt_mezzanine.settings

# Install packages and update base system
RUN yum -y install epel-release \
        && yum -y install cronie libjpeg-devel nginx python-pip mysql-devel python-devel supervisor \
        && yum -y groupinstall "Development Tools" \
        && yum -y update \
        && yum -y clean all

# Install the LCOGT Mezzanine webapp Python required packages
COPY lcogt_mezzanine/pip-requirements.txt /var/www/apps/lcogt_mezzanine/
RUN pip install pip==1.3 \
        && pip install -r /var/www/apps/lcogt_mezzanine/pip-requirements.txt

# Ensure crond will run on all host operating systems
RUN sed -i -e 's/\(session\s*required\s*pam_loginuid.so\)/#\1/' /etc/pam.d/crond

# Copy configuration files
COPY config/init /init
COPY config/uwsgi.ini /etc/uwsgi.ini
COPY config/nginx/* /etc/nginx/
COPY config/processes.ini /etc/supervisord.d/processes.ini
COPY config/crontab.root /var/spool/cron/root

# Copy the LCOGT Mezzanine webapp files
COPY lcogt_mezzanine /var/www/apps/lcogt_mezzanine
