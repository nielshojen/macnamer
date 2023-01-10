#!/bin/bash

cd $APP_DIR
ADMIN_PASS=${ADMIN_PASS:-}
mkdir -p db
chown -R app:app $APP_DIR
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

if [ ! -z "$ADMIN_PASS" ] ; then
  python3 manage.py update_admin_user --username=admin --password=$ADMIN_PASS
else
  python3 manage.py update_admin_user --username=admin --password=password
fi

chown -R app:app $APP_DIR