#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
import os


def validate_file(value):
    ex = os.path.splitext(str(value))[1]
    if ex not in [".jpg", ".png", ".jpeg"]:
        raise ValidationError('Geçersiz dosya formatı. Yüklediğini dosya şu uzantılara sahip olabilir. ["png", "jpg", "jpeg"]')


def validate_file_size(value):
    file_size = 1048576  # 1 Mb
    if value.size > file_size:
        raise ValidationError("Yüklediğiniz resim en fazla 1 mb .")


def validate_thesis_file(value):
    ex = os.path.splitext(str(value))[1]
    if ex not in [".pdf", ".doc", "docx", ".pptx"]:
        raise ValidationError('Geçersiz dosya formatı. Yüklediğiniz dosya şu uzantılara sahip olabilir. ["pdf", "doc", "docx", "pptx"]')


def validate_thesis_file_size(value):
    file_size = 5242880  # 5 Mb
    if value.size > file_size:
        raise ValidationError("Yüklediğiniz dosya en fazla 5 mb olabilir.")


def validate_thesis_image_size(value):
    file_size = 5242880  # 5 Mb
    if value.size > file_size:
        raise ValidationError("Yüklediğiniz dosya en fazla 5 mb olabilir.")


def validate_multi_thesis_file(files):
    for thesis_file in files:
        ex = os.path.splitext(str(thesis_file))[1]
        if ex not in [".pdf", ".doc", "docx", ".pptx"]:
            raise ValidationError('Geçersiz dosya formatı. Yüklediğiniz dosya şu uzantılara sahip olabilir. ["pdf", "doc", "docx", "pptx"] : %s'
                                  % thesis_file, code="invalid_extension")


def validate_multi_image_file(images):
    for thesis_image in images:
        ex = os.path.splitext(str(thesis_image))[1]
        if ex not in [".jpg", ".png", ".jpeg"]:
            raise ValidationError('Geçersiz dosya formatı. Yüklediğiniz dosya şu uzantılara sahip olabilir. ["png", "jpg", "jpeg"] : %s'
                                  % thesis_image, code="invalid_extension")