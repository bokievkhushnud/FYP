from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .utils import generate_qr


# signals to generate QR code
@receiver(post_save, sender=Item)
def add_qr_item(sender, instance, **kwargs):
    data = f'items/detail/{instance.id}'
    img_url = generate_qr('asset', data, instance.id)
    Item.objects.filter(id=instance.id).update(qr_code=img_url)
