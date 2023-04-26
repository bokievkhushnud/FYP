from qrcode import make
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Function to generate QR code
def generate_qr(item_type, data, id):
    img = make(data)
    img_name = 'qr_' + item_type + "_" + str(id) + '.png'
    img_path = 'qrcode/' + img_name

    # Save the QR code to media storage
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_file = ContentFile(buffer.read())
    default_storage.save(img_path, img_file)

    img_url = default_storage.url(img_path)


    return img_url


# Function to generate Unique code for every item
def generate_code(campus, department, category, ID):
    return "{}-{:04d}-{:04d}-{:04d}".format(campus, int(department.dep_code), int(category.cat_code),int(ID))