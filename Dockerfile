################################################################################
#
# Runs the LCOGT Python Django Mezzanine webapp using nginx + uwsgi
#
# The decision to run both nginx and uwsgi in the same container was made because
# it avoids duplicating all of the Python code and static files in two containers.
# It is convenient to have the whole webapp logically grouped into the same container.
#
# You can choose to expose the nginx and uwsgi ports separately, or you can
# just default to using the nginx port only (recommended). There is no
# requirement to map all exposed container ports onto host ports.
#
# Build with
# docker build -t docker.lcogt.net/mezzanine:latest .
#
# Push to Registry with
# docker push docker.lcogt.net/mezzanine:latest
#
# To run with nginx + uwsgi both exposed:
# docker run -d -p 8100:80 -m="2048m" --restart=always -v /net/mfs/data4/webfiles:/var/www/apps/lcogt_mezzanine/static/media/files --name=website docker.lcogt.net/mezzanine:latest
#
# See the notes in the code below about NFS mounts.
#
################################################################################

FROM centos:centos7
MAINTAINER LCOGT <webmaster@lcogt.net>

# Install packages and update base system
RUN yum -y install epel-release \
        && yum -y install cronie libjpeg-devel nginx python-pip mysql-devel python-devel supervisor \
        && yum -y groupinstall "Development Tools" \
        && yum -y update

# Ensure crond will run on all host operating systems
RUN sed -i -e 's/\(session\s*required\s*pam_loginuid.so\)/#\1/' /etc/pam.d/crond

# Setup the Python Django environment
ENV PYTHONPATH /var/www/apps
ENV DJANGO_SETTINGS_MODULE lcogt_mezzanine.settings
ENV BRANCH ${BRANCH}
#ENV BUILDDATE ${BUILDDATE}

# Copy configuration files
COPY config/uwsgi.ini /etc/uwsgi.ini
COPY config/nginx/* /etc/nginx/
COPY config/processes.ini /etc/supervisord.d/processes.ini
COPY config/crontab.root /var/spool/cron/root

# nginx (http protocol) runs on port 80
# uwsgi (uwsgi protocol) runs on port 9090
EXPOSE 80 9090

# Entry point is the supervisord daemon
ENTRYPOINT [ "/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.conf" ]

# Copy the LCOGT Mezzanine webapp files
COPY lcogt_mezzanine /var/www/apps/lcogt_mezzanine

# Install the LCOGT Mezzanine webapp Python required packages
RUN pip install pip==1.3 \
        && pip install -r /var/www/apps/lcogt_mezzanine/pip-requirements.txt

# It is not possible to access NFS mount points during the docker build
# process. If the chmod cannot be run externally, and must be run every
# time this docker image is started, supervisord can handle it with some
# additional configuration.
#
# Likewise, if the "python manage.py collectstatic" process needs to be
# run every time this node is restarted, supervisord can handle it with
# some additional configuration.
#
# In order to access the NFS mount while this docker image is running,
# you must start the instance with the argument:
#
# -d /path/to/nfs/mount/on/docker/host:/var/www/apps/lcogt_mezzanine/files
#
# These commands are left here for reference:
# RUN chmod 777 /var/www/apps/lcogt_mezzanine/static/media/files/
# RUN mount_nfs -o resvport mfs.lco.gtn:/data4/webfiles /var/www/apps/lcogt_mezzanine/static/media/files

# Setup the LCOGT Mezzanine webapp
RUN python /var/www/apps/lcogt_mezzanine/manage.py collectstatic --noinput

# Upload the latest version of the data for the django_lcogtbiblio (Bibliometrics) app
# RUN python /var/www/apps/lcogt_mezzanine/manage.py loaddata /var/www/apps/lcogt_mezzanine/fixtures/biblio_snapshot.json
