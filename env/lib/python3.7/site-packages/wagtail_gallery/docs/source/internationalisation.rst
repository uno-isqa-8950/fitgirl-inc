**************************
Internationalisation
**************************

Languages
=============

Currently only these languages are fully supported:

    #. English (Daniel F. Meyer)
    #. Afrikaans (Daniel F. Meyer)


It would be super awesome if you translate it to your locale language and make a pull request so that everybody can enjoy your translations. You'll also get credit on this page.

To translate the app is super easy thanks to gettext and Django's builtin stuff. This will translate the user interface and admin interface.

.. code-block:: shell

    $ cd wagtail_gallery
    $ django-admin makemessages -l <your_locale>


Open the ``wagtail_gallery/locale/<your_locale>LC_MESSAGES/django.po`` file in your favourite text editor. Provide your translations and then run ``django-admin compilemessages``. The translations should now automatically activate on server restart.

The language will default to what is set in ``settings.py`` ;however, if a specific Wagtail user changes it then it will be what they set as their language or what langauge you serve the page in to the client. See the Django and Wagtail internationalisation documentation on this.

Caveats
=================

#. I have not internationalised the urls yet; however, its planned as a feature for soon.