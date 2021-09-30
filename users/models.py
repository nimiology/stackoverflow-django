from django.db import models


class Wallet(models.Model):

    id = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.id


class Company(models.Model):

    wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.pk


class Employee(models.Model):

    wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.pk
