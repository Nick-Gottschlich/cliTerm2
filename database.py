# The Database object is a container for all the supported anime.

import os
import random

class Anime:
    __id = ""  # ID is stored as a string because it must maintain "003" format, not "3".
    __name = ""
    __path = ""  # The location of the image.

    def __init__(self, identifier, name, path):
        self.__id = identifier
        self.__name = name
        self.__path = path

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_path(self):
        return self.__path

    def __str__(self):
        return self.get_id() + " " + self.get_name().capitalize() + " at " + self.get_path()


class Database:
    __anime_list = []
    __anime_dictionary = {}
    __directory = ""  # The global location of the code.

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(__file__))
        self.__load_data()

    def __str__(self):
        string = ""
        for element in self.__anime_list:
            string += str(element) + "\n"
        return string[:-1]  # Remove the final new line ("\n").

    def __contains__(self, anime):
        # Check for a anime by ID or name.
        if type(anime) is int or str(anime).isdigit():
            return self.anime_id_exists(anime)
        else:
            return self.anime_name_exists(anime)

    def __len__(self):
        return len(self.__anime_list)

    def get_all(self):
        # Get all the anime.
        result = []
        for anime in self.__anime_list:
            result.append(anime)
        return result

    def get_random(self):
        # Select a random anime from the database.
        random_int = random.randint(0, len(self.__anime_list) - 1)
        return self.__anime_list[random_int]

    def anime_id_exists(self, identifier):
        # Check for anime by ID.
        identifier = int(identifier)
        # will need to change this to have a proper max
        if identifier < 1 or identifier > 1:
            return False
        else:
            return True

    def anime_name_exists(self, name):
        # Check for anime by Name.
        return name.lower() in self.__anime_dictionary

    def get_anime(self, anime):
        # Get a anime by name or ID.
        if type(anime) is not int and type(anime) is not str:
            raise Exception("The parameter anime must be of type integer or string.")
        if not self.__contains__(anime):
            raise Exception("No such anime in the database.")
        if type(anime) is int or str(anime).isdigit():
            return self.get_anime_by_id(anime)
        else:
            return self.get_anime_by_name(anime)

    def get_anime_by_name(self, name):
        # Get a anime by its name.
        if type(name) is not str:
            raise TypeError("The type of name must be a string.")
        if not self.anime_name_exists(name):
            raise Exception("No such anime in the database.")
        return self.__anime_dictionary[name]

    def get_anime_by_id(self, identifier):
        # Get a anime by its ID.
        if type(identifier) is not int and not str(identifier).isdigit():
            raise TypeError("The anime ID must be a number.")
        if not self.anime_id_exists(identifier):
            raise Exception("The anime ID must be between 1 and " + str(self.__MAX_ID) + " inclusive.")
        return self.__anime_list[int(identifier) - 1]  # Subtract 1 to convert to 0 base indexing.

    def names_with_prefix(self, prefix):
        # Return anime who's names begin with the specified prefix.
        result = []
        for anime in self.__anime_list:
            if str(anime.get_name()).startswith(prefix):
                result.append(anime)
        return result

    def names_with_infix(self, infix):
        # Return anime who's names contains the specified infix.
        result = []
        for anime in self.__anime_list:
            if infix in str(anime.get_name()):
                result.append(anime)
        return result

    def __load_data(self):
        # Load all the anime data.
        path = "/./Data/anime.txt"
        data_file = open(self.directory + path, 'r')
        for line in data_file:  # Load everything
            identifier = line.split(' ')[0]  # First part of the line is the id.
            name = line[len(identifier)+1:-1].lower()  # The rest is the name (minus the new line at the end).
            identifier = self.__add_zeroes(identifier)  # This statement cannot occur before name has been created.
            path = self.directory + "/./Images/Main" + "/" + identifier + ".png"
            anime = Anime(identifier, name, path)
            self.__anime_list.append(anime)
            self.__anime_dictionary[anime.get_name()] = anime

    @staticmethod
    def __add_zeroes(number):
        # Add zeroes to the front so that it begins with 3 digits. Example: "2" -> "002".
        zeroes = ""
        if int(number) < 10:
            zeroes = "00"
        elif int(number) < 100:
            zeroes = "0"
        return zeroes + str(number)
