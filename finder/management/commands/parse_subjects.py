from django.core.management.base import BaseCommand
from finder.models import Subject
import requests
import re


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        response = requests.get("https://www.ucas.com/explore/subjects").content.decode("utf-8")
        course_cards = re.findall("<div class=\"card card--cta link-container transition-trigger\">(.+?)/h3>",
                                  response)
        for course in course_cards:
            title = re.findall("<h3>(.+?)<", course)[0]
            image_source = re.findall("data-background-url=\"(.+?)\"", course)[0]
            print(title, image_source)
            Subject.objects.create(title=title, image_src=image_source)
        self.stdout.write(self.style.SUCCESS('Subjects parsed successfully'))



