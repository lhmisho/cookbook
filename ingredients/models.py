from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Feature Name"), max_length=50, unique=True)
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2)
    category = models.ManyToManyField("Category", verbose_name=_("Product categories"), blank=True)
    in_stock = models.BooleanField(_("In Stock?"), default=True)
    date_created = models.DateTimeField(_("Date created"), auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
