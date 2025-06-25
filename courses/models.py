
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  
    price = models.DecimalField(max_digits=8, decimal_places=2)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    cheat_sheet = models.FileField(upload_to='cheat_sheets/', blank=True, null=True)


    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/courses/{self.course.slug}/materials/{self.slug}/"
