from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=120)
    image_src = models.URLField(blank=True)
    description = models.CharField(max_length=200, blank=True)
    # duration = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)


class University(models.Model):
    title = models.CharField(max_length=120)
    courses = models.ManyToManyField(Subject)
    # location = models.Field

    def __str__(self):
        return self.title
