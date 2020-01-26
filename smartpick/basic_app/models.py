from django.db import models

# Create your models here.

class Compare(models.Model):
    item1 = models.CharField(max_length=1000,null=True)
    item1_img = models.CharField(max_length=1000,null=True)
    item1_link = models.CharField(max_length=1000,null=True)
    item2 = models.CharField(max_length=1000,null=True)
    item2_img = models.CharField(max_length=1000,null=True)
    item2_link = models.CharField(max_length=1000,null=True)
    item3 = models.CharField(max_length=1000,null=True)
    item3_img = models.CharField(max_length=1000,null=True)
    item3_link = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.item1
