from django.db import models
from api.models import User

# Create your models here.
class Document(models.Model):
    doc_one=models.CharField(max_length=1000,blank=True,null=True)
    file=models.FileField(upload_to='media/files/',blank=True,null=True)
    doc_two=models.CharField(max_length=1000,blank=True,null=True)
    file_two=models.FileField(upload_to='media/files/',blank=True,null=True)
    uploaded_by=models.ForeignKey(User,on_delete=models.CASCADE)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    starred_by=models.ManyToManyField(User,related_name='starred_by')
    def __str__(self):
        return self.uploaded_by.username
        
