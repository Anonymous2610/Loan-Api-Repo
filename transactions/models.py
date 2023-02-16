from django.db import models
# from api.models import User as user
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
status_choices = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('paid', 'Paid'),
    ]

class Loan(models.Model):
    """
    Loan model
    """
    id=models.AutoField(primary_key=True)
    provider=models.ForeignKey(User, on_delete=models.CASCADE,related_name='provider',null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=(('open', 'Open'), ('closed', 'Closed'), ('paid', 'Paid')),default='open')
    def __str__(self):
        return str(self.id)



class transcation(models.Model):
    """
    Transaction model
    """
    id=models.AutoField(primary_key=True) 
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    delay_request=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)