from django.db import models
from django.contrib.auth.models import User

class subject(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    sub_name = models.CharField(max_length=100)
    present=models.IntegerField(default=0)
    totalclasses=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.sub_name}:{self.user.username}'
    def absent(self):
        return self.totalclasses-self.present
    def att_perc(self):
        return round(self.present/self.totalclasses*100,2)
    def can_leave(self):
        c=0
        k=self.totalclasses+1
        while self.present/k>=0.75:
            c+=1
            k+=1
        return c