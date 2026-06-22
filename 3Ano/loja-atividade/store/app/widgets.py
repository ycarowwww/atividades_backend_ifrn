from django.forms.widgets import ClearableFileInput

class ImagePreviewInput(ClearableFileInput):
    template_name = "widgets/image_preview.html"
