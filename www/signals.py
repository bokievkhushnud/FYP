from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .utils import generate_qr, generate_code
from django.core.files import File


# signals to generate QR code
@receiver(post_save, sender=Item)
def add_qr_item(sender, instance, **kwargs):
    data = instance.id
    img_name, img_file = generate_qr(instance.item_type, data, instance.id)
    item_code = generate_code(instance.campus, instance.department, instance.category, instance.id)

    # Temporarily disconnect the post_save signal
    post_save.disconnect(receiver=add_qr_item, sender=Item)

    # Update the item_code and save the QR code
    instance.item_code = item_code
    instance.qr_code.save(img_name, img_file, save=True)
    instance.save()

    # Reconnect the post_save signal
    post_save.connect(receiver=add_qr_item, sender=Item)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_active:
        # Extract data first name and last name from the email
        first_name, last_name = instance.username.split('@')[0].split('.')
        if "_" in last_name:
            last_name = last_name.split("_")[0]
        instance.email = instance.username
        instance.first_name = first_name
        instance.last_name = last_name
        instance.save()

        Profile.objects.create(owner=instance)

        