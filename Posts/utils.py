import os
import random
import string

from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def PictureAndVideoValidator(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png', '.raw', '.mov', '.wmv', '.avi', '.mp4', '.mvp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('the file is not acceptable')


def upload_file(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    final_name = f"{''.join(random.choice(letters) for _ in range(40))}{ext}"
    return f"{final_name}"


def upload_image_Question(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.slug}{ext}"
    return f"Question/{instance.slug}/{final_name}"


def upload_image_Answer(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.pk}{ext}"
    return f"Question/{instance.question.slug}/Answer/{final_name}"


def slug_generator():
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    slug = "".join(random.choice(letters) for _ in range(50))
    return slug


def upload_profilePic(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.profile.authID}{ext}"
    return f"profiles/{final_name}"


def upload_companyDocument(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    randomSTR = "".join(random.choice(letters) for _ in range(40))
    final_name = f"{randomSTR}{ext}"
    return f"profiles/{instance.company.profile.id}/{final_name}"


class CreateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    pass
