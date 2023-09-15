from applications.profiles.models import ExecutorProfile, CustomerProfile
from applications.orders.models import Order
from django.db import models

class FeedbackOnExecutor(models.Model):
    RATING_CHOICES = ((i, i * '*') for i in range(1, 6))
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.TextField(max_length=200, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedbacks_on_executor"
    )

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
        unique_together = ('customer', 'executor', 'order_id')
        db_table = "feedbacks_on_executor"


    def __str__(self):
        return f"{self.rating}, {self.description}"


class FeedbackOnCustomer(models.Model):
    RATING_CHOICES = ((i, i * '*') for i in range(1, 6))
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    description = models.TextField(max_length=200, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    order_id = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedbacks_on_customer"
    )

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
        unique_together = ('executor', 'customer', 'order_id')
        db_table = "feedbacks_on_customer"

    def __str__(self):
        return f"{self.rating}, {self.description}"