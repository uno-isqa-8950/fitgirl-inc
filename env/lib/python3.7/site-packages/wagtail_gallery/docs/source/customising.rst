.. _customising-label:

===================
Customising
===================

Edit the template files. I do plan on doing template tags in the :ref:`future <roadmap-label>` for a better experience but this is just how it is for now.

All that you absolutely need is to load the ``wagtail_gallery/css/lightbox.min.css`` at the top of the page. You will need to load ``wagtail_gallery/js/jquery.min.js`` before ``wagtail_gallery/js/lightbox.min.js`` static files in the ``wagtail_gallery/gallery_page.html`` template.

To actually render the gallery and lightbox script add the following:

.. code-block:: html

    <script>
        lightbox.option({
            'alwaysShowNavOnTouchDevices': true,
            'wrapAround': true
        })
    </script>

    {% for img in page.gallery_image.all %}
        {% image img.image fill-400x300-c100 as header_image %}
            <a class="d-block mb-4 h-100" href="{{ img.image.file.url }}" data-lightbox="{{ page.title }}"
               data-title="{{ img.description }}">
                <img class="img-raised rounded img-fluid" src="{{ header_image.url }}">
            </a>
    {% endfor %}

There is only a small amount of customisation available of both how the lightbox looks and functions, see: `Lightbox JS docs <https://lokeshdhakar.com/projects/lightbox2/#options>`_
