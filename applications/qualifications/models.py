from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name


class Language(models.Model):
    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="languages"
    )
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.value


class Education(models.Model):
    graduation_date = models.DateField()
    university = models.CharField(max_length=150)
    faculty = models.CharField(max_length=150)
    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="educations"
    )

    class Meta:
        db_table = "educations"

    def __str__(self):
        return (f"Университет: {self.university} Факультет: {self.faculty} "
                f"Дата окончания: {self.graduation_date}")


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
    executor = models.ForeignKey(
        "profiles.ExecutorProfile",
        on_delete=models.CASCADE,
        related_name="portfolios"
    )
    url = models.URLField()

    class Meta:
        db_table = "portfolios"

    def __str__(self):
        return f"{self.url}"
