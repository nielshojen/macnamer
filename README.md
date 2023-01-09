# Macnamer

Macnamer is a combination of a Django web app and a script to run on your client Macs with the goal of setting the name of your Macs.

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
* ``DOCKER_MACNAMER_TZ``: The desired [timezone](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Defaults to ``Europe/London``.
* ``DOCKER_MACNAMER_ADMINS``: The admin user's details. Defaults to ``Docker User, docker@localhost``.

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

### Running the Macnamer Container

```docker run -d --name="macnamer" \
  -p 80:8000 \
  -v /usr/local/macnamer_data/db:/home/app/macnamer/db \
  -e ADMIN_PASS=pass \
  nielshojen/macnamer
  ```

## Acknowledgements

Thanks to Graham Gilbert who originally built this. I just changed a few things that i needed in my env

## ToDo

* SAML or OAuth2 authentication
* Add support for MySQL
