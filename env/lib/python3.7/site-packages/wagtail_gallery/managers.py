from django.db import models


class CategoryManager(models.Manager):

    def with_uses(self, gallery_page):
        entries = gallery_page.get_entries()
        return self.filter(gallerypage__in=entries).distinct()
