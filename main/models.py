from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from sorl.thumbnail import processors

def select(klass):
    return klass.objects.all()

def select_latest(klass):
    return klass.objects.latest()

def get_about():
    return About.objects.latest()
    
def select_attr(klass, attr):
    "Utility to get unique list of attr on klass (select attr on klass unique)"
    objs = klass.objects.all()
    results = []
    for obj in objs:
        if hasattr(obj, attr):
            a = getattr(obj, attr)
            if a not in results:
                results.append(a)
    results = list(set(results))
    results.sort()
    return results

orientations = (('landscape', 'landscape'), ('portrait', 'portrait'))

class BlogPost(models.Model):    
    posted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_on = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    text = models.TextField()
    items = models.ManyToManyField("Item", blank=True, null=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('main_post_detail', [str(self.slug)])
    
    class Meta:
        ordering = ('published_on',)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
        
    
class Item(models.Model):
    added = models.DateTimeField(auto_now_add=True)    
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, blank=True, null=True)
    desc = models.TextField()
    category = models.CharField(max_length=128)
    price = models.IntegerField()    
    url = models.CharField(max_length=255)
    thumb = models.ImageField(upload_to="item/", blank=True, null=True,
                              help_text="Item should be 150x150 pixels. Larger images will be resized.")
    photos = models.ManyToManyField("Photo", blank=True, null=True)
    
    def __unicode__(self):
        return u"%s" % self.title[:20]
    
    @models.permalink
    def get_absolute_url(self):
        return ('main_item_detail', [str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

def create_item_thumb(sender, **kwargs):
    import os
    obj = kwargs['instance']
    if obj.thumb:
        imgname = obj.thumb.path
        img = create_thumb(imgname, (150, 150), {'crop': 'center'})
        img.save(imgname)
        obj.thumb = os.path.split(imgname)[1]
    
post_save.connect(create_item_thumb, sender=Item, dispatch_uid="main.models")

def create_thumb(imgname, size, opts):
    from PIL import Image
    im = Image.open(imgname)
    im = processors.scale_and_crop(im, size, opts)
    return im

class Photo(models.Model):
    image = models.ImageField(upload_to="photos")
    thumb = models.ImageField(upload_to="photos", blank=True, null=True)
    credit = models.CharField(max_length=128, blank=True, null=True)
    alt = models.CharField(max_length=255, default="")
    
    def __unicode__(self):
        return u"%s" % self.alt
    
def create_photo_thumb(sender, **kwargs):
    import os
    obj = kwargs['instance']
    imgname = obj.image.path
    img = create_thumb(imgname, (128, 128), {}) 
    thmbpath = "%s_thumb_%s" % os.path.splitext(imgname)
    img.save(thmbpath)
    thmbname = "photos/%s" % os.path.split(thmbpath)[1]
    obj.thumb = thmbname
    
#post_save.connect(create_photo_thumb, sender=Photo)

class About(models.Model):
    photo = models.ImageField(upload_to="photos", blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=14, blank=True, null=True)
    alturl = models.CharField(max_length=255, blank=True, null=True)
    alturl_title = models.CharField(max_length=64, blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('main_about', [])
    
    class Meta:
        get_latest_by = 'id'

def resize_about_photo(sender, **kwargs):
    import os
    obj = kwargs['instance']
    if not obj.photo.path: return
    imgname = obj.photo.path
    img = create_thumb(imgname, (120, 180), {})
    img.save(imgname)
    obj.photo = imgname
        
post_save.connect(resize_about_photo, sender=About)
    
class Press(models.Model):
    publication = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    file = models.ForeignKey('File', blank=True, null=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('main_list_press', [])
    
    class Meta:
        ordering = ('date',)
    
class File(models.Model):
    name = models.CharField(max_length=32)
    file = models.FileField(upload_to="press")
    order = models.CharField(max_length=2, default=1)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        ordering = ('order',)
