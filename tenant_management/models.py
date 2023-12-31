from django.db import models
from authentications.models import User
from property_management.models import Unit
class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.name

class TenantAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()
    monthly_rent_date = models.IntegerField()

    def __str__(self):
        return f"{self.tenant.name} - {self.unit.property.name}"