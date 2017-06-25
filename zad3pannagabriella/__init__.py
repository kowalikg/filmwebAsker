from bs4 import BeautifulSoup
from enum import Enum
import requests
import re  # regular expressions


class ExitStatus(Enum):
    FOUND = 1
    FOUND_ACTOR_WITH_THAT_LAST_NAME = 2
    NOT_FOUND = 3


class WebRequestException(Exception):
    def __init__(self, description):
        self.description = description


class Actor:
    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last

    def __str__(self):
        return self.first_name + " " + self.last_name



class Movie:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __str__(self):
        return self.title


class PatternBox:
    href = "href=\""
    full_alphabet = "[A-ZŻŹĆĄŚĘŁÓŃa-zżźćńółęąś0-9 ]"
    title = ").*)\" title=\"(.*)\"$"
    film_or_serial = "(/(?:film|serial|"
    person1 = "href=\"/person/\S+ \S+ \S+ title=\""
    person2 = "href=\"/person/\S+ title=\""
    star = "*"
    end = "\"$"


class Resolver:
    def __init__(self, first_name, last_name, movie_name):
        self.movie_name = movie_name
        self.actor = Actor(first_name, last_name)
        self.base_address = "http://www.filmweb.pl"

    def resolve(self):
        print(
            "Sprawdzamy czy " + self.actor.__str__() +
            " grał(a) w filmie " + self.movie_name
            )

        lines = self.get_lines(self.base_address + "/search?q=" + self.movie_name)

        movies = []
        pattern = PatternBox.href + PatternBox.film_or_serial +\
            PatternBox.full_alphabet + PatternBox.title

        for line in lines:
            link = re.search(pattern, line)
            if link:
                movies.append(Movie(link.group(2), link.group(1)))

        winner_movies = []
        suspected_actors = []

        for movie in movies:
            result = self.actor_info(movie)

            if result[0] is True:
                winner_movies.append(movie)
            elif not result[0]:
                pass
            else:
                suspected_actors.append((Actor(result[0], result[1]), movie))

        if len(winner_movies):
            # print(self.actor)
            # mozna wywolac bez str kiedy nie uzywamy kontakenancji

            print(self.actor.__str__() + " grał(a) w filmach:")
            print("Oryginalne tytuły: ")
            for movie in winner_movies:
                print(movie)
            print("Znaleziona w Internecie informacja jest raczej pewna")

            return ExitStatus.FOUND

        if not len(winner_movies) and len(suspected_actors):
            print("Prawdopodobnie moze chodzić o aktorów:")

            for actor in suspected_actors:
                print(actor[0].__str__() + " gral(a) w" + actor[1].__str__())

            print("Być może chodzi o któregoś z nich")
            return ExitStatus.FOUND_ACTOR_WITH_THAT_LAST_NAME

        if not len(winner_movies) and not len(suspected_actors):
            print(
                "Solver nie zweryfikował " +
                "czy ten aktor grał w filmie o tym tytule"
                )
            return ExitStatus.NOT_FOUND

    @staticmethod
    def get_content_by_address(address):
        content = requests.get(address)
        content.encoding = 'utf-8'

        if content.status_code == 200:
            # if ok
            return content.text
        else:
            raise WebRequestException("Cannot get http response!")

    def actor_info(self, movie):
        lines = self.get_lines(self.base_address + movie.link)

        pat0_full_name = self.actor.first_name + " " + self.actor.last_name
        pat1_full_name = PatternBox.person1 + self.actor.first_name + \
            PatternBox.full_alphabet + PatternBox.star + \
            self.actor.last_name + PatternBox.end
        pat2_full_name = PatternBox.person2 + self.actor.first_name + \
            PatternBox.full_alphabet + PatternBox.star + \
            self.actor.last_name + PatternBox.end

        pat1_last_name = PatternBox.person1 + "(" +\
            PatternBox.full_alphabet + PatternBox.star + ")" +\
            self.actor.last_name + PatternBox.end
        pat2_last_name = PatternBox.person2 + "(" +\
            PatternBox.full_alphabet + PatternBox.star + ")" +\
            self.actor.last_name + PatternBox.end

        for line in lines:

            if re.search(pat0_full_name, line) or\
                    re.search(pat1_full_name, line) or\
                    re.search(pat2_full_name, line):
                return True, True

            result = re.search(pat1_last_name, line)
            if result:
                return result.group(1), self.actor.last_name

            result = re.search(pat2_last_name, line)
            if result:
                return result.group(1), self.actor.last_name

        return False, False

    def get_lines(self, address):
        web_page = self.get_content_by_address(address)

        html = BeautifulSoup(web_page, 'html.parser')
        divs = html.__str__()

        lines = divs.split(">")
        return lines
