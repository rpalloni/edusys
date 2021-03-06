from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# docker-compose exec envoice_api bash
# use shell: python manage.py shell

class Category(models.Model):
    ct_id = models.AutoField(primary_key=True, db_column='ct_id') # no auto generation of pk
    ct_title = models.CharField('Title', max_length=255) # frontend label
    ct_slug = models.SlugField('Slug', max_length=255)
    ct_short = models.TextField('Short description', blank=True, null=True)
    ct_created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.ct_title


class Course(models.Model):
    cr_id = models.AutoField(primary_key=True, db_column='cr_id')
    cr_categ = models.ManyToManyField(Category,
                            verbose_name='Category',
                            db_column = 'cr_categ',
                            related_name='courses')
    cr_title = models.CharField('Title', max_length=255)
    cr_slug = models.SlugField('Slug', max_length=255)
    cr_short = models.TextField('Short description', blank=True, null=True)
    cr_long = models.TextField('Long description', blank=True, null=True)
    cr_created_at = models.DateTimeField('Created at', auto_now_add=True)
    cr_image = models.ImageField('Image', upload_to='courses/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.cr_title

    def get_image(self):
        if self.cr_image:
            return settings.SERVER_URL + self.cr_image.url
        else:
            return 'http://bulma.io/images/placeholders/1280x960.png'


class Lesson(models.Model):
    
    DRAFT = 'draft'
    PUBLISHED = 'published'

    CHOICES_STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    ARTICLE = 'article'
    QUIZ = 'quiz'

    CHOICES_TYPE = (
        (ARTICLE, 'Article'),
        (QUIZ, 'Quiz')
    )

    ls_id = models.AutoField(primary_key=True, db_column='ls_id')
    ls_course = models.ForeignKey(Course, 
                                verbose_name='Course',
                                related_name='lessons', 
                                on_delete=models.CASCADE)
    ls_title = models.CharField('Title', max_length=255)
    ls_slug = models.SlugField('Slug', max_length=255)
    ls_short = models.TextField('Short description', blank=True, null=True)
    ls_long= models.TextField('Long description', blank=True, null=True)
    ls_status = models.CharField('Status', max_length=20, choices=CHOICES_STATUS, default=PUBLISHED)
    ls_type = models.CharField('Type', max_length=20, choices=CHOICES_TYPE, default=ARTICLE)

    class Meta:
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f'{self.ls_course} - {self.ls_title}'


class Comment(models.Model):
    cm_id = models.AutoField(primary_key=True, db_column='cm_id')
    cm_lesson = models.ForeignKey(Lesson,
                                verbose_name='Lesson',
                                related_name='comments',
                                on_delete=models.CASCADE)
    cm_title = models.CharField('Title', max_length=50)
    cm_content = models.TextField('Content', blank=True, null=True)
    cm_created_at = models.DateTimeField('Created at', auto_now_add=True)
    cm_created_by = models.ForeignKey(User,
                                related_name='comments',
                                on_delete=models.CASCADE)