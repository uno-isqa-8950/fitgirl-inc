Welcome to Wagtail Gallery's documentation!
===========================================

This is a very basic gallery app that integrates with Wagtail. It allows a person to upload images and order them on a gallery page. Said gallery page then shows the low-res thumbnails, and when clicked it opens up a high res version with captions.

This app is simple, and not feature rich. It does the basics and thats it. I will probably add more features and options to it as time permits, but only if requests are made.

It is also not production ready as there are **no tests currently written** for it. I did put this up on a site and they have been using it extensively and haven't had any reported issues. That said, *apps without tests should always be treated sceptically.*

I hope to write tests in a month or so when I get a bit of free time. I also hope to add a bunch of features in the near future. See: :ref:`roadmap-label`

Please report any errors you encounter. I will try resolve them quickly and then add tests for them as things come up so it doesn't reoccur. Please visit `wagtail_gallery git <https://gitlab.com/dfmeyer/wagtail_gallery>`_ to make pull requests or log issues etc. Documentation is at readthedocs.io: `wagtail_gallery documentation <https://wagtail-gallery.readthedocs.io/en/latest/>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   customising
   internationalisation
   api
   roadmap
   changelog


Thanks
====================

This app wouldn't be possible without the following great projects and people:

   #. `Wagtail CMS <https://wagtail.io/>`_
   #. `Django Web Framework   <https://www.djangoproject.com/>`_
   #. `Lightbox <https://lokeshdhakar.com/projects/lightbox2/>`_
   #. `Bootstrap <http://getbootstrap.com/>`_
   #. `Django Social Share <https://github.com/fcurella/django-social-share>`_
   #. `Font Awesome <https://fontawesome.com/>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
