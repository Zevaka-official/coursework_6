import hashlib
import os.path
from django.core.files import File
from django.core.files.utils import validate_file_name
from django.core.files.storage import FileSystemStorage


class HashStorage(FileSystemStorage):

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)

        if not self.exists(name):
            name = self._save(name, content)

        validate_file_name(name, allow_relative_path=True)
        return name


def _get_file_hash_path(root, instance, filename):
    instance.preview_image.open()
    context = instance.preview_image.read()
    _, ext = os.path.splitext(filename)

    file_path = os.path.join(root, hashlib.md5(context).hexdigest() + ext)

    return file_path


def product_preview_images(instance, filename):
    return _get_file_hash_path('product_preview_images', instance, filename)


def article_preview_images(instance, filename):
    return _get_file_hash_path('article_preview_images', instance, filename)


def user_logo_images(instance, filename):
    return _get_file_hash_path('user_logo_images', instance, filename)
