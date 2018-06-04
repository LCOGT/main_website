FROM python:3.6-alpine
MAINTAINER Edward Gomez <egomez@lco.global>

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /lco_global
RUN mkdir /static
WORKDIR /lco_global
ADD ./lco_global /lco_global

RUN apk --no-cache add mariadb-client-libs \
        && apk --no-cache add --virtual .build-deps gcc mariadb-dev musl-dev git \
        && apk --no-cache add libjpeg-turbo jpeg-dev libjpeg libjpeg-turbo-dev \
        && pip --no-cache-dir --trusted-host=buildsba.lco.gtn install gunicorn[gevent] -r requirements.pip \
        && apk --no-cache del .build-deps

CMD python manage.py collectstatic --no-input;python manage.py migrate; gunicorn lcogt_mezzanine.wsgi -b 0.0.0.0:8000
