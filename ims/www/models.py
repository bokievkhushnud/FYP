from django.db import models


# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name

class GeberatedQRCode(models.Model):
    item = models.OneToOneField(Item, on_delete = models.CASCADE,)
    qr_code_url = models.CharField(max_length=200)


    def __str__(self):
        return self.item.item_name

