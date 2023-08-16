from django.db import models
from applications.users.models import CustomerProfile, ExecutorProfile, Skill


class PaymentMethod(models.TextChoices):
    HOURLY = 'hourly', 'Почасовая оплата'
    FIXED = 'fixed', 'Фиксированная оплата'

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, null=True)
    price = models.IntegerField()
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    skill = models.ManyToManyField(Skill)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.title

class Ordering(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderings')
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='orderings')
    attached = models.BooleanField(default=False)

    def __str__(self):
        return f"Ordering: {self.order} - Executor: {self.executor}"