#!/bin/sh

if [ ! -d "/data/books" ]; then
  cp -rf /prebuilt/books /data/
fi

if [ ! -d "/data/books/settings" ]; then
  cp -rf /prebuilt/books/settings /data/books/
fi

if [ ! -s "/data/books/calibre-webserver.db" ]; then
  cp /prebuilt/books/calibre-webserver.db /data/books/
fi

if [ ! -d "/data/log" ]; then
  cp -rf /prebuilt/log /data/
fi

CONF=/etc/nginx/conf.d/calibre-webserver.conf
envsubst '${NGINX_CLIENT_MAX_BODY_SIZE}' < "${CONF}.template" > "${CONF}"
service nginx restart
/usr/bin/supervisord --nodaemon
