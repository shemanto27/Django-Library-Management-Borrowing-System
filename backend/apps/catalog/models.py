from django.db import models

# Create your models here.
class AuthorModel(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BookModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(AuthorModel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title