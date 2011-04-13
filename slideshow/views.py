from models import SlideShowImage
from django.http import HttpResponse
import json

def get_images(request):
    "Get the slideshow images!"
    paths = []
    images = SlideShowImage.objects.all()
    for image in images:
        paths.append(image.image.url)

    content = json.dumps(paths)
    return HttpResponse(content=content, content_type="application/json")
