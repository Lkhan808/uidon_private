from applications.profiles.models import ExecutorProfile, CustomerProfile
from django.db import models


# class Review(models.Model):
#     executor = models.ForeignKey(
#         ExecutorProfile,
#         on_delete=models.CASCADE,
#         related_name="reviews"
#     )
#     customer = models.ForeignKey(
#         CustomerProfile,
#         on_delete=models.CASCADE,
#         related_name="reviews"
#     )
#     text = models.TextField(max_length=500)
#
#     class Meta:
#         db_table = 'reviews'
#
#     def __str__(self):
#         return f"{self.text}"


# class Rating(models.Model):
#     RATING_CHOICES = ((i, i * '*') for i in range(1, 6))
#
#     grade = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
#     description = models.TextField(max_length=200, null=True)
#
#     customer = models.ForeignKey(
#         CustomerProfile,
#         on_delete=models.CASCADE,
#         related_name="ratings"
#     )
#     executor = models.ForeignKey(
#         ExecutorProfile,
#         on_delete=models.CASCADE,
#         related_name="ratings"
#     )
#
#     class Meta:
#         unique_together = ('customer', 'executor')
#         db_table = "ratings"
#
#     def __str__(self):
#         return f"{self.grade}, {self.description}"


class FeedbackOnExecutor(models.Model):
    RATING_CHOICES = ((i, i * '*') for i in range(1, 6))

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.TextField(max_length=200, null=True)

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="feedbacks_on_executor"
    )

    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="feedbacks_on_executor"
    )

    class Meta:
        unique_together = ('customer', 'executor')
        db_table = "feedbacks_on_executor"


    def __str__(self):
        return f"{self.rating}"


class FeedbackOnCustomer(models.Model):
    RATING_CHOICES = ((i, i * '*') for i in range(1, 6))

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.TextField(max_length=200, null=True)

    executor = models.ForeignKey(
        ExecutorProfile,
        on_delete=models.CASCADE,
        related_name="feedbacks_on_customer"
    )

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="feedbacks_on_customer"
    )

    class Meta:
        unique_together = ('executor', 'customer')
        db_table = "feedbacks_on_customer"

    def __str__(self):
        return f"{self.rating}, {self.description}"