from django.db import models
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    qr_code_url = models.CharField(max_length=200)
    def __str__(self):
        return self.item_name
