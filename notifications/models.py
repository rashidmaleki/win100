from django.db import models
from django.contrib import admin
import jdatetime

# Create your models here.
class Notification(models.Model):
    subject = models.CharField(verbose_name='عنوان' , max_length=50)
    text = models.TextField(verbose_name="متن اطلاعیه")
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    def __str__(self) -> str:
        return self.subject


    class Meta:
        verbose_name_plural = "اطلاعیه ها"
        verbose_name = "اطلاعیه"


class Faq(models.Model):
    question = models.CharField(verbose_name='سوال؟', max_length=200)
    answer = models.TextField(verbose_name='جواب')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "سوالات متداول"
        verbose_name = "سوال"