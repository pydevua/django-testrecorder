from django.db import models
from django.utils.translation import ugettext_lazy as _

class News(models.Model):
    name = models.CharField(_(u'Name'), max_length=255)
    content = models.TextField(_(u'Content'))
    image = models.ImageField(_(u'Image'), upload_to='uploads/news/', blank=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('main:news-details', [self.pk])