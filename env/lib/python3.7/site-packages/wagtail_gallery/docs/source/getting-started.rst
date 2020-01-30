***************************
Getting Started
***************************

Installation
===================

To install run ``pip install wagtail_gallery``

It should automatically install all the necessary dependencies.

Remember to add ``wagtail_gallery`` (along with the others mentioned) to your installed apps in settings.py i.e.

    .. code-block:: Python

        INSTALLED_APPS = [
            ...
            'wagtail_gallery',
            'wagtail.contrib.routable_page',
            'wagtail.contrib.modeladmin',
            'django_social_share',
        ]

Requirements:

    .. code-block:: Python

        python3
        wagtail
        django
        django-social-share

I'm not quite sure how far back this app works; however, it should work going back quite far. It's currently tested on Python3 with Wagtail >2 and Django >2 on openSUSE. It should work on all platforms and shouldn't break anytime soon. Let me know if you have a combo that doesn't work and I'll see what I can do to support it.

*Please see the* :ref:`caveats-label` *below*

Usage
===================================

To use the app just add a Gallery Root Page to your page hierarchy and fill in the details as necessary.

It will only serve low-res thumbnails by default; however, it will load a high quality version when clicked on.

To add a gallery itself open the sidebar gallery option and add a gallery page, and in each gallery page, add your images. The image at the top will be the thumbnail for the gallery.



Customising
==========================

Honestly this is really basic. No menus, no title bar, just some bootstrap cards, pagination, and a side bar, all of which is responsive. I highly recommend you edit the templates. I do plan on creating template tags at a later stage that should make customising much easier in the future. This is a rough, ugly framework just to get you on your feet. Go nuts! I recommend cheaking out the beautiful themes (based on Bootstrap) made by `Creative Tim <https://www.creative-tim.com/>`_

For more about customising see: :ref:`customising-label`

.. _caveats-label:

Caveats
============

#.  I haven't implemented sub-categories at all. Its a planned feature.

#. You can only have one Gallery Root Page at this point in time. I really do want to add the ability to have many. I just haven't gotten round to it. It should be quite simple.

#. URLs are not yet fully internationalised as ``/category/`` isn't translated. I'll get to this eventually.

#. All galleries are public. No permissions have been integrated; however, this is a planned feature.

