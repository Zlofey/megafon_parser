from django.db import models
#автодобавление company_info
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from  django.utils.timezone import now
import time


class Company(models.Model):
    key = models.CharField(primary_key= True, max_length=200)
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=300, blank=True)
    password = models.CharField(max_length=400, blank=True)
    ls = models.CharField(max_length=200, blank=True)
    def publish(self):
        Company_info.objects.create(company=self.key)
        self.save()
    def __str__(self):
        return self.name



class Company_info(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)
    balance = models.FloatField(blank=True, null=True, default=0)
    expenses = models.FloatField(blank=True, null=True, default=0)
    payment = models.FloatField(blank=True, null=True, default=0)
    updated = models.DateTimeField(blank=True, auto_now=True)
    expenses_limit = models.FloatField(blank=True, null=True, default=0)
    credit_limit = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.company.name


# class History(models.Model):
#     company =

#post_init
'''
эта хуйня работает наполовину
@receiver(post_save, sender=Company, dispatch_uid="add_company_info")
def add_company_info(sender, instance, **kwargs):
    print('sender.pk=', sender.pk)
    print('instance.pk=', instance.pk)
    Company_info.objects.create(company=instance)
'''

class History_info(models.Model):
    company_key = models.CharField(blank=True, null=True, max_length=200)
    company_name = models.CharField(blank=True,max_length=200)
    published_date = models.DateTimeField(blank=True, default=now)
    balance = models.FloatField(blank=True, null=True, default=0)
    expenses = models.FloatField(blank=True, null=True, default=0)
    payment = models.FloatField(blank=True, null=True, default=0)
    credit_limit = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.published_date.strftime('%d-%m-%y') + ' ' +  self.company_name

    def publish(self):
        self.published_date = now()
        self.save()
