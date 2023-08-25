from django.db import models
from applications.profiles.models import ExecutorProfile, CustomerProfile
from applications.qualifications.models import Skill


class Order(models.Model):
    STATUS_CHOICES = (
        ('новый', 'новый'),
        ('в работе', 'в работе'),
        ('закрыт', 'закрыт'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('наличный', 'наличный'),
        ('оклад', 'оклад'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    price = models.IntegerField()
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    skill = models.ManyToManyField(Skill)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    response_count = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return self.title

class OrderResponse(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderings')
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='orderings')
    attached = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Ordering: {self.order} - Executor: {self.executor}"

