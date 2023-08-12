from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.db.models import Count, Avg


class User(AbstractBaseUser, PermissionsMixin):
    email_validator = EmailValidator()
    ROLE_CHOICES = (
        ('customer', 'customer'),
        ('executor', 'executor'),
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[email_validator]
    )
    role = models.CharField(max_length=55, choices=ROLE_CHOICES)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name


class BaseProfile(models.Model):
    user = None
    phone_regex_validator = RegexValidator(
        regex=r'^\+(996)(\d{9})$',
        message='Номер телефона должен быть в формате +код страныXXXXXXXXX',
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    avatar = models.ImageField(null=True, blank=True)
    location = models.CharField(unique=True, max_length=150)
    phone = models.CharField(
        unique=True,
        max_length=13,
        validators=[phone_regex_validator])

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
    biography = models.TextField()
    GENDER_CHOICES = (
        ("Женский", "Женский"),
        ("Мужской", "Мужской"),
        ("Не указано", "Не указано"),
    )
    date_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    EDUCATION_CHOICES = (
        ("Среднее", "Среднее"),
        ("Высшее", "Высшее"),
    )
    profession = models.CharField(max_length=150)
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
    def average_rating(self):
        rating_dict = self.ratings.all().aggregate(average_rating=Avg("grade"))
        avg_rating = rating_dict["average_rating"]
        if avg_rating is not None:
            return round(avg_rating)
        else:
            return None

    @property
    def reviews_count(self):
        return self.reviews.all().annotate(reviews_count=Count('id'))["reviews_count"]


class Language(models.Model):
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="languages"
    )
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "languages"

    def __str__(self):
        return f"{self.executor}----{self.value}"


class Education(models.Model):
    graduation_date = models.DateField()
    university = models.CharField(max_length=150)
    faculty = models.CharField(max_length=150)
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="educations"
    )

    class Meta:
        db_table = "educations"

    def __str__(self):
        return f"{self.executor} окончил {self.university}"


class Contact(models.Model):
    value = models.CharField(max_length=100)
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    class Meta:
        db_table = "contacts"

    def __str__(self):
        return f"Контактная информация {self.executor}"


class Portfolio(models.Model):
    url_validator = URLValidator()
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="portfolios"
    )
    url = models.URLField(validators=[url_validator])

    class Meta:
        db_table = "portfolios"

    def __str__(self):
        return f"{self.executor}---{self.url}"


class Review(models.Model):
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField(max_length=500)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Заказчик: {self.customer} оставил отзыв {self.executor}"


class Rating(models.Model):
    RATING_CHOICES = ((i, i * '*') for i in range(1, 6))
    grade = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    class Meta:
        unique_together = ('customer', 'executor')
        db_table = "ratings"

    def __str__(self):
        return f"Заказчик: {self.customer} оценил {self.executor}"