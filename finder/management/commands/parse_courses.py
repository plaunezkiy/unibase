import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import json
import datetime
from django.core.management.base import BaseCommand
from finder.models import Subject


def get_page_counter(url):
    page = requests.get(url).content.decode("utf-8")
    soup = BeautifulSoup(page, "html.parser")
    pager = soup.find("div", {"class": "explore__pager"})
    try:
        counter = pager.findAll("a", {"class": "button explore__pager-item"})[-1]
    except AttributeError:
        return 1
    return int(counter.get_text())


def parse_page(url, page):
    page = requests.get(url + f"&page={page}").content.decode("utf-8")

    soup = BeautifulSoup(page, "html.parser")

    cards = soup.findAll("div", {"class": "explore-grid__item grid__item"})
    for card in cards:
        uni = card.find("a", {"class": re.compile("^provider transition--hover-stop.*")})
        uni = uni.get_text()

        course_info = card.find("h3", {"class": "course-title"})
        link = course_info.find("a")["href"]
        
        title = course_info.get_text()

        mode_div = card.find("div", {"class": "study-mode icon-inline--left icon--study-mode-darker"})
        mode = mode_div.find("dd").get_text()
        duration_div = card.find("div", {"class": "duration icon-inline--left icon--duration-darker"})
        duration = duration_div.find("dd").get_text()

        requirements = card.find("div", {"class": "ucas-points link-container__escape transition--hover-stop"})
        requirements = requirements.find("dd").get_text()
        if requirements != "N/A":
            requirements = re.match("(.+?)/", requirements)[0]
        print(requirements)

        more = False
        related = card.find("a", {"class": "icon-inline--right icon--chevron-right-light link-container__link"})
        try:
            url = "https://ucas.com" + related["href"]
            more = True
            yield [{
                "university": uni,
                "title": title,
                "mode": mode,
                "duration": duration,
                "requirements": requirements
            }, [more, url]]

        except Exception:
            yield [{
                "university": uni,
                "title": title,
                "mode": mode,
                "duration": duration,
                "requirements": requirements
            }, [more]]


def parse_pages(url):
    data = []
    page_cnt = get_page_counter(url)
    for page in range(page_cnt):
        for primary in parse_page(url, page+1):
            data.append(primary[0])
            if primary[1][0]:
                results = parse_pages(primary[1][1])
                for index, result in enumerate(results):
                    if index == 0:
                        continue
                    data.append(result)
    return data


def retrieve_data(course, year=2021, level="undergraduate"):
    q_course = f"subject={quote(str(course))}"
    filter_by = f"filterBy=all"
    level = f"studyLevel={level}"
    year = f"studyYear={year}"

    query_list = [q_course, filter_by, level, year]
    query = "&".join(query_list)

    query_url = f"https://www.ucas.com/explore/courses?{query}"

    data = parse_pages(query_url)
    with open(f"data/{course}.json", "x") as file:
        json.dump(data, file)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        counter = Subject.objects.count()
        subjects = Subject.objects.all()
        for index, subject in enumerate(subjects):
            retrieve_data(subject)
            self.stdout.write(self.style.SUCCESS(f"{index+1}/{counter} {subject} parsed successfully"))
        self.stdout.write(self.style.SUCCESS("All subjects parsed successfully"))


# print(retrieve_data("Computer science"))
