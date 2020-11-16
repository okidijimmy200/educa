from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    # owner: The instructor who created this course.
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    # subject: The subject that this course belongs to. It is a ForeignKey field that points to the Subject model.
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    # title: The title of the course.
    title = models.CharField(max_length=200)
    # slug: The slug of the course. This will be used in URLs later.
    slug = models.SlugField(max_length=200, unique=True)
    # overview: A TextField column to store an overview of the course.
    overview = models.TextField()
# created: The date and time when the course was created. It will beautomatically set by Django when creating new objects because of auto_now_ add=True.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    # class Meta:
    #     ordering = ['order']


# class Content(models.Model):
#     module = models.ForeignKey(Module,
#                                related_name='contents',
#                                on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType,
#                                      on_delete=models.CASCADE,
#                                      limit_choices_to={'model__in':(
#                                      'text',
#                                      'video',
#                                      'image',
#                                      'file')})
#     object_id = models.PositiveIntegerField()
#     item = GenericForeignKey('content_type', 'object_id')
#     order = OrderField(blank=True, for_fields=['module'])

#     class Meta:
#         ordering = ['order']



# class ItemBase(models.Model):
#     owner = models.ForeignKey(User,
#                               related_name='%(class)s_related',
#                               on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.title

# class Text(ItemBase):
#     content = models.TextField()

# class File(ItemBase):
#     file = models.FileField(upload_to='files')

# class Image(ItemBase):
#        file = models.FileField(upload_to='images')

# class Video(ItemBase):
#     url = models.URLField()
