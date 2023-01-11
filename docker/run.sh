#!/bin/bash

cd $APP_DIR
ADMIN_PASS=${ADMIN_PASS:-}
mkdir -p db
chown -R app:app $APP_DIR

if [ "$MIGRATE_FROM_SOUTH" = "True" ] ; then
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find . -path "*/migrations/*.pyc"  -delete
  python3 manage.py makemigrations --noinput
  python manage.py migrate --fake-initial
else
  python3 manage.py makemigrations --noinput
  python3 manage.py migrate --noinput
  python3 manage.py collectstatic --noinput
fi

if [ ! -z "$ADMIN_PASS" ] ; then
  python3 manage.py update_admin_user --username=admin --password=$ADMIN_PASS
else
  python3 manage.py update_admin_user --username=admin --password=password
fi

chown -R app:app $APP_DIR
