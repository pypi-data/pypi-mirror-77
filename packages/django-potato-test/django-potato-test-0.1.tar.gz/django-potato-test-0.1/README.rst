======
Potato
======

Potato is a Django app for blogging.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "potato" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'potato',
    ]

2. Include the potato URLconf in your project urls.py like this::

    path('potato/', include('potato.urls')),

3. Run ``python manage.py migrate`` to create the potato models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/potato/ to participate in the poll.