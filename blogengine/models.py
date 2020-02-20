import time
from django.db import models
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from model_utils import FieldTracker


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True)
    body = models.TextField(db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    class Meta:
        ordering = ['-date_pub']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if Post.objects.filter(slug=self.slug).count() or self.slug == 'create':
            self.slug = slugify(self.title) + str(int(time.time()))
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detailed_post_url', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('edit_post_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_post_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=150, db_index=True, unique=True)
    slug = models.SlugField(max_length=150, blank=True)
    tracker = FieldTracker()

    class Meta:
        ordering = ['tag_name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tag_name)
        if not self.id or self.tracker.has_changed('slug'):
            if Tag.objects.filter(slug=self.slug).count() or self.slug == 'create':
                self.slug = slugify(self.tag_name) + str(int(time.time()))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse('detailed_tag_url', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('edit_tag_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_tag_url', kwargs={'slug': self.slug})
