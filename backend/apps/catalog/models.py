from django.db import models

# Create your models here.
class AuthorModel(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CategoryModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BookModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    total_copies = models.IntegerField(default=0)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title