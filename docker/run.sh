#!/bin/bash

cd $APP_DIR
ADMIN_PASS=${ADMIN_PASS:-}
mkdir -p db
chown -R app:app $APP_DIR

if [ ! ${DB_HOST} ] && [ $(echo ".tables" | python3 manage.py dbshell | tr " " "\n" | grep south) ] ; then
  echo "Old Macnamer DB detected - need tp do a bit of work"
  echo ".tables" | python3 manage.py dbshell | tr " " "\n" | grep south | sed 's/^/DROP TABLE /g' | sed 's/$/;/g' | python3 manage.py dbshell
  python3 manage.py migrate --fake-initial
fi

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

if [ ! -z "$ADMIN_PASS" ] ; then
  python3 manage.py update_admin_user --username=admin --password=$ADMIN_PASS
else
  python3 manage.py update_admin_user --username=admin --password=password
fi

chown -R app:app $APP_DIR
