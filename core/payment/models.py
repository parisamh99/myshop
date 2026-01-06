from django.db import models

class PaymentStatusType(models.IntegerChoices):
    pending = 1, "در انتظار"
    success = 2, "پرداخت موفق"
    failed = 3, "پرداخت ناموفق"

class Payment(models.Model):
    authority = models.CharField(max_length=250,null=True,blank=True)
    amount = models.PositiveIntegerField()
    ref_id = models.CharField(max_length=250,null=True,blank=True)
    status = models.IntegerField(choices=PaymentStatusType.choices,default=PaymentStatusType.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.status}"
