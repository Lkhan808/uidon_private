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
        ('почасовая', 'почасовая'),
        ('оклад', 'оклад'),
    )

    title = models.CharField(max_length=400)
    description = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    price = models.IntegerField()
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    skill = models.ManyToManyField(Skill)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='новый')
    response_count = models.PositiveIntegerField(default=0, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class OrderResponse(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderings')
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE, related_name='orderings', null=True, blank=True)
    attached = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ordering: {self.order} - Executor: {self.executor}"


class FavoriteOrder(models.Model):
    executor = models.ForeignKey(ExecutorProfile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)