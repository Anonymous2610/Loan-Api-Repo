from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser
from transactions.models import Loan,transcation


class User(AbstractUser):
    """
        User Model
    """
    USER_TYPES=(
        ('lender','Lender'),
        ('borrower','Borrower'),
    )
    user_type=models.CharField(max_length=10,choices=USER_TYPES,default='borrower')
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    phone_number=models.CharField(max_length=20,unique=True,null=True)
    balance=models.IntegerField(default=0)
    avatar=models.ImageField(upload_to='media/avatar/', default='media/avatar/default.png')
    civil_score=models.IntegerField(default=100)
    username=models.CharField(max_length=100,null=True,unique=True)
    is_online=models.BooleanField(default=False,null=True)
    address=models.TextField(null=True)
    uid=models.CharField(max_length=20,null=True)
    adhar=models.CharField(max_length=16,null=True)
    pan=models.CharField(max_length=10,null=True)

    # verification_status=models.BooleanField(default=False)
    def __str__(self): 
        return self.username
    



class Message(models.Model):
    """
    Message model
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    message = models.TextField(blank=True, null=True)
    linked_conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read=models.BooleanField(default=False,null=True)
    Transcation_id=models.ForeignKey(transcation,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.message




class Conversation(models.Model):
    """
    Conversation model
    """
    name=models.CharField(max_length=1000)
    loan=models.ForeignKey(Loan, on_delete=models.CASCADE)
    lenders = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Lender',null=True)
    borrowers = models.ManyToManyField(User, related_name='Borrower')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Created_by',null=True)
    profile_pic=models.ImageField(upload_to='media/profile_pics', blank=True, default='media/profile_pics/default.png')
    def __str__(self):
        return self.name


class Call(models.Model):
    """
    Call model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name="caller")
    to=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,related_name="reciever")
    created_at = models.CharField(max_length=30,null=True)
    ended_at=models.CharField(max_length=30,null=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_missed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_inprogress = models.BooleanField(default=False)
    duration=models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.user.username+"-"+self.to.username
    

    

