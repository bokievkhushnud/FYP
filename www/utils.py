from qrcode import make
from django.core.files.storage import default_storage

# Function to generate QR code
def generate_qr(item_type, data, id):
    img = make(data)
    img_name = 'qr_' + item_type + "_" + str(id) + '.png'
    img_path = 'qrcode/' + img_name

    # Save the QR code to media storage
    with default_storage.open(img_path, 'wb') as img_file:
        for chunk in img.iter_chunks(1024):
            img_file.write(chunk)

    return img_name


# Function to generate Unique code for every item
def generate_code(campus, department, category, ID):
    return "{}-{:04d}-{:04d}-{:04d}".format(campus, int(department.dep_code), int(category.cat_code),int(ID))


# Saving new Items
