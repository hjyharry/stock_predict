from django.db import models

# Create your models here.
class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender, default='男')
    c_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class User_info(models.Model):
    id = models.OneToOneField("User",on_delete=models.CASCADE,related_name="user_id",db_column="id",primary_key=True,unique=True)
    name = models.CharField(max_length=256,verbose_name="昵称",null=True,unique=True)
    intro = models.TextField(null=True)
    image = models.FileField(null=True,upload_to='image')

    def __str__(self):
        return self.id