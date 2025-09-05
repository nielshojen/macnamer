from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random
import string

def GenerateKey():
    key = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(128))
    try:
        ComputerGroup.objects.get(key=key)
        return GenerateKey()
    except ComputerGroup.DoesNotExist:
        return key;

class ComputerGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Computer Group Name")
    prefix = models.CharField(max_length=200, verbose_name="Computer Name Prefix", blank=True, null=True)
    divider = models.CharField(max_length=1, verbose_name="Name Devider", choices=[('', 'None'), (' ', '(Space)'), ('-', '-')], default='', blank=True)
    domain = models.CharField(max_length=200, verbose_name="Computer Domain", blank=True, null=True)
    key = models.CharField(max_length=255, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.pk and not self.key:
            self.key = GenerateKey()
        super(ComputerGroup, self).save(*args, **kwargs)
    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.id
    class Meta:
        ordering = ['id']

class Network(models.Model):
    id = models.AutoField(primary_key=True)
    network = models.CharField(max_length=200, unique=True)
    computergroup = models.ForeignKey(ComputerGroup, on_delete=models.CASCADE)
    def __str__(self):
        return self.network
    class Meta:
        ordering = ['network']

class Computer(models.Model):
    id = models.AutoField(primary_key=True)
    computergroup = models.ForeignKey(ComputerGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Computer Name")
    serial = models.CharField(max_length=200, verbose_name="Serial Number", unique=True)
    last_checkin = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return ('%s%s' % (self.computergroup, self.name))
    class Meta:
        ordering = ['name']
