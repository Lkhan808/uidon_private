from applications.qualifications.models import Skill
from applications.users.models import User
from django.db import models
from django.db.models import Count, Avg


class BaseProfile(models.Model):
    user = None
    full_name = models.CharField(max_length=150)
    avatar = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=150)
    phone = models.CharField(unique=True, max_length=13)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class CustomerProfile(BaseProfile):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    class Meta:
        db_table = 'customers'


class ExecutorProfile(BaseProfile):
    GENDER_CHOICES = (
        ("Женский", "Женский"),
        ("Мужской", "Мужской"),
        ("Не указано", "Не указано"),
    )

    EDUCATION_CHOICES = (
        ("Среднее", "Среднее"),
        ("Высшее", "Высшее"),
    )
    PAYMENT_METHOD_CHOICES = (
        ('почасовая', 'почасовая'),
        ('оклад', 'оклад'),
    )

    biography = models.TextField()
    date_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    profession = models.CharField(max_length=150)
    salary_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    education_level = models.CharField(max_length=15, choices=EDUCATION_CHOICES)
    skills = models.ManyToManyField(Skill)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="executor_profile"
    )

    class Meta:
        db_table = 'executors'

    @property
    def reviews_count(self):
        return self.reviews.all().aggregate(value=Count("id"))["value"]

    @property
    def average_rating(self):
        return self.ratings.all().aggregate(value=Avg("grade"))["value"]