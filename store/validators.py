from django.core.files import File
from django.core.exceptions import ValidationError

def validate_file_size(file: File):
    max_file_size_kb = 50

    if file.size > max_file_size_kb * 1024:
        raise ValidationError(f"File size shouldn't exceed {max_file_size_kb} KB.")