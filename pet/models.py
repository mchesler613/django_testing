from django.db import models


# An Owner of one or more pets
class Owner(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# A Pet must have an owner
class Pet(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(
        to=Owner,
        on_delete=models.CASCADE  # when an owner is deleted, so is their pet
    )

    def __str__(self):
        return self.name
