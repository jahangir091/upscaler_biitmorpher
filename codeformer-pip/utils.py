import base64
import os
import uuid
import io
import numpy as np
from PIL import Image
import piexif
import piexif.helper

from pydantic import BaseModel, Field


def get_img_path():
    current_dir = os.path.dirname(__file__)
    img_directory = current_dir + '/.temp/'
    os.makedirs(img_directory, exist_ok=True)
    img_file_name = uuid.uuid4().hex[:20] + '.jpg'
    return img_directory + img_file_name


def save_image(base64_image):
    # Decode Base64 string to bytes
    image_bytes = base64.b64decode(base64_image)

    # Convert image to PIL
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode == "RGBA":
        image = image.convert("RGB")
    img_path = get_img_path()
    image.save(img_path)
    return img_path


def encode_pil_to_base64(image):
    with io.BytesIO() as output_bytes:
        if image.mode == "RGBA":
            image = image.convert("RGB")
        parameters = image.info.get('parameters', None)
        exif_bytes = piexif.dump({
            "Exif": {piexif.ExifIFD.UserComment: piexif.helper.UserComment.dump(parameters or "",
                                                                                encoding="unicode")}
        })
        image.save(output_bytes, format="JPEG", exif=exif_bytes)
        bytes_data = output_bytes.getvalue()
    return base64.b64encode(bytes_data)


class UpscaleImageRequest(BaseModel):
    image: str = Field(default="", title="Image", description="Image to work on, must be a Base64 string containing the image's data.")
