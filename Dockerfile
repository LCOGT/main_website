FROM python:3.6-alpine
MAINTAINER Edward Gomez <egomez@lco.global>

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# install depedencies
COPY lco_global/requirements.pip /var/www/apps/lco_global/
RUN apk --no-cache add mariadb-client-libs \
        && apk --no-cache add --virtual .build-deps gcc mariadb-dev musl-dev git \
        && apk --no-cache add libjpeg-turbo jpeg-dev libjpeg libjpeg-turbo-dev \
        && pip --no-cache-dir --trusted-host=buildsba.lco.gtn install -r /var/www/apps/lco_global/requirements.pip \
        && apk --no-cache del .build-deps

# install entrypoint
COPY docker/init /

# install web application
COPY lco_global /var/www/apps/lco_global/
ENTRYPOINT [ "/init" ]
