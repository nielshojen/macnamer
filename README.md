# Macnamer

Macnamer is a combination of a Django web app and a script to run on your client Macs with the goal of setting the name of your Macs. This is a drop in replacement for [MacNamer](https://hub.docker.com/r/macadmins/macnamer)

## Why?

To keep computer naming consistent. It's primarily meant for Macs, but could be used by any os.

## Deploying to clients

The Mac client part of this is available [here](https://github.com/nielshojen/macnamer-client)

## Usage

Macnamer is divided into groups, and within each group are computers and networks.

### Computer Numbers

If you set a prefix for the group, Macnamer will auto increment the number - it for example, set ABC as the prefix and your first machine will be ABC1.

### Networks

If you assign a network to a group, any new request that comes from that network will be assigned the next available number (if you're using the auto naming functionality). If you don't wish Macs to be automatically added to Macnamer, don't assign any networks to a group.

You should enter the network as the LAN subnet xxx.xxx.xxx.0 (e.g. 192.168.10.0) - there isn't currently any support for subnets other than /24, although you can enter multiple subnets, nor is there any validation currently of the field, so make sure you're entering your desired subnets correctly.

## Running it

The easiest way of running this is by running it in Docker or Kubernetes.

### Settings

Several options, such as the timezone and admin password are customizable using environment variables.

* ``ADMIN_PASS``: The default admin's password. This is only set if there are no other superusers, so if you choose your own admin username and password later on, this won't be created.
* ``MACNAMER_TZ``: The desired [timezone](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Defaults to ``Europe/London``.
* ``MACNAMER_ADMINS``: The admin user's details. Defaults to ``Docker User, docker@localhost``.
* ``SECRET_KEY``: The Django secret key. This key is mostly used to sign session cookies. In production you should probalby set your own. Defaults to ``2&lakkwf+r78)9u+30&+1=zc3()1^s2oqrbxr5qe8z_@xm2a&4``.
* ``HOST_NAME``: Set the host name of your instance - might berequired if you do not have control over the load balancer or proxy in front of your instance (see [the Django documentation](https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-trusted-origins)).

If you require more advanced settings, for example if you want to hide certain plugins from certain Business Units or if you have a plugin that needs settings, you can override ``settings.py`` with your own. A good starting place can be found on this image's [Github repository](https://github.com/grahamgilbert/macadmins-macnamer/blob/master/settings.py). To use your own ``settings.py`` file, use the ``-v`` option:

``-v /usr/local/macnamer_data/settings/settings.py:/home/app/macnamer/macnamer/settings.py``

### Database

The directory the SQLite database lives in (``/home/app/macnamer/db``) is exposed. To persist your database, you should run your container with ``-v /host/path/somewhere/db:/home/app/macnamer/db``.

There is also the option of using a postgres database instead, which will can be set up with these environment variables:

* ``DB_HOST``: The hostname for your postgresql server. Defaults to ``db``.
* ``DB_PORT``: Port the postgres server runs on. Defaults to ``5432``.
* ``DB_NAME``: Name of the database. Required.
* ``DB_USER``: Username for the database. Required.
* ``DB_PASS``: Password for the database. Required.

### Migrating data from SQLite to Postgres (in Docker)

NB: Remember to back up your data before starting this!

If you are running v1.0 of this image or the original [MacNamer](https://hub.docker.com/r/macadmins/macnamer), I recommend starting with an upgrade to v2+ of this image, as it should take care of all database migrations before the move to postgres.

Once that's done, dump your current DB to a file. This exmaple dumps the file in the same folder as the SQLite DB file:

```python3 manage.py dumpdata --natural-foreign --natural-primary > db/macnamer_export.json```

Next rename the current DB file so it doesn't get loaded on next startup:

```mv db/macnamer.db db/macnamer_old.db```

Stop the docker, set the environment variables for postgres as described above and start the docker again.

Start with a clean postgres by opening a shell:

```python3 manage.py shell```

And cleaning out the content types:

```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```

And then import your data back into the database:

```python3 manage.py loaddata db/macnamer_export.json```

### Running the Macnamer Container

```docker run -d --name="macnamer" \
  -p 80:8000 \
  -v /usr/local/macnamer_data/db:/home/app/macnamer/db \
  -e ADMIN_PASS=pass \
  nielshojen/macnamer
  ```

## Changelog

* v1.0: Close as makes no odds to the original [MacNamer](https://hub.docker.com/r/macadmins/macnamer). Just a few tweaks to make it work on newer kubernetes versions
* v2.0: Updated to Django 4.1.5. Added support for Postgres. Added support for a choise of different dividers between prefix and number.
* v2.1: Changed from [phusion/passenger-customizable](https://hub.docker.com/r/phusion/passenger-customizable) to [python-alpine](https://hub.docker.com/_/python). Image now passes Snyk scanning.

## Acknowledgements

Thanks to Graham Gilbert who originally built this. I just changed a few things that i needed in my env

## ToDo

* SAML or OAuth2 authentication
* Add support for MySQL
