import os
import random
import string

from django.core.exceptions import ValidationError


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def PictureAndVideoValidator(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png', '.raw', '.mov', '.wmv', '.avi', '.mp4', '.mvp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('the file is not acceptable')


def upload_file_Post(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.slug}{ext}"
    return f"Posts/{final_name}"


def upload_image_Question(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.slug}{ext}"
    return f"Question/{instance.slug}/{final_name}"


def upload_image_Answer(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.pk}{ext}"
    return f"Question/{instance.question.slug}/Answer/{final_name}"


def slug_genrator(cls):
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    while True:
        SLUG = "".join(random.choice(letters) for _ in range(50))
        qs = cls.objects.filter(slug=SLUG)
        if not qs.exists():
            break

    return SLUG


def upload_profilePic(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.profile.authID}{ext}"
    return f"profiles/{final_name}"


def upload_companyDocument(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    randomSTR = "".join(random.choice(letters) for _ in range(50))
    final_name = f"{randomSTR}{ext}"
    return f"profiles/{instance.company.profile.authID}/{final_name}"


def upload_file(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    randomName = "".join(random.choice(letters) for _ in range(100))
    final_name = f"{randomName}{ext}"
    return f"ChatRoom/{instance.chatRoom.pk}/{final_name}"
