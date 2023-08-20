from applications.profiles.models import ExecutorProfile, CustomerProfile
from django.db import models


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
        return self.customer


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
