from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .utils import generate_qr, generate_code


# signals to generate QR code
@receiver(post_save, sender=Item)
def add_qr_item(sender, instance, **kwargs):
    print(kwargs)
    data = f'items/detail/{instance.id}'
    img_url = generate_qr('asset', data, instance.id)
    item_code = generate_code(instance.campus, instance.department, instance.category, instance.id)
    Item.objects.filter(id=instance.id).update(qr_code=img_url, item_code=item_code)