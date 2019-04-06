from urllib.parse import urlparse
from wtforms.validators import ValidationError


class ImportValidator:
    def __init__(self, message=None):
        if not message:
            message = "Not a valid pastebin.com URL or import code."
        self.message = message

    def __call__(self, form, field):
        url = urlparse(field.data)
        if url.netloc != "pastebin.com" and len(field.data) % 4 != 0:
            raise ValidationError(self.message)
