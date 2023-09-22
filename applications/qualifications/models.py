from django.db import models


class Skill(models.Model):

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name


class Language(models.Model):

    value = models.CharField(max_length=100)

    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="languages"
    )

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.value


class Contact(models.Model):

    value = models.TextField(max_length=200)

    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    class Meta:
        db_table = "contacts"

    def __str__(self):
        return f"{self.value}"


class Portfolio(models.Model):

    url = models.URLField()

    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="portfolios"
    )

    class Meta:
        db_table = "portfolios"

    def __str__(self):

        return f"{self.url}"