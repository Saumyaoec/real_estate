from django.db import models
from authentications.models import User
class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.unit_type} - {self.property.name}"