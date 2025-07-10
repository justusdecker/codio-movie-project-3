from random import randint

import matplotlib.pyplot as plt

from bin.constants import *
from bin.modules import *

from os.path import isfile
from json import load, dumps, JSONDecodeError

class Movie:
    """
    Represents a movie with its title, rating, and release year.

    This class acts as a data model for a movie, providing properties to
    access and modify its attributes. It stores the actual movie data
    internally within a dictionary.
    """
    def __init__(self,movie_data: dict):
        self.movie_data = movie_data

    def asdict(self) -> dict:
        """
        Returns a dictionary representation of the movie's core attributes.

        This method is useful for serializing the movie object, e.g., for saving
        to a file or sending over a network, ensuring a consistent structure.
        It explicitly returns the 'title', 'rating', and 'release_year'
        properties.
        """
        return {
            'title': self.title,
            'rating': self.rating,
            'release_year': self.release_year
        }
    
    @property
    def title(self) -> str:
        """ Gets the title of the movie. Defaults to 'n.a.' if not set. """
        return self.movie_data.get('title','n.a.')
    @title.setter
    def title(self, value: str):
        self.movie_data['title'] = value
    @property
    def rating(self) -> int:
        """ Gets the rating of the movie. Defaults to 0 if not set. """
        return self.movie_data.get('rating',0)
    @rating.setter
    def rating(self, value: int):
        self.movie_data['rating'] = value
    @property
    def release_year(self) -> int:
        """ Gets the release year of the movie. Defaults to 0 if not set. """
        return self.movie_data.get('release_year',0)
    @release_year.setter
    def release_year(self, value: int):
        self.movie_data['release_year'] = value
    

class MovieRank:
    def __init__(self):
        self.isrunning = True
        self.load_movies()

    @property
    def titles(self) -> list[str]:
        return [i.title for i in self.movies]

    def save_movies(self):
        """
        Gets all your movies as an argument and saves them to the JSON file.
        """
        with open(f'movies.json', 'w') as file_write:
            file_write.write(dumps([movie.asdict() for movie in self.movies],indent=4))
    
    def load_movies(self):
        """
        loads a list of dictionaries that
        contains the movies information in the database into `self.movies`
        """
        self.movies: list[Movie] = []
        file_name = f'movies.json'
        if isfile(file_name):
            try:
                with open(file_name) as file_read:
                    movies_json = load(file_read)
                    if not isinstance(movies_json,list):
                        raise TypeError()
                    self.movies = [Movie(movie) for movie in movies_json]
                    
            except JSONDecodeError:
                print(f'Cant load from file: {file_name} ERROR: JSONDE')
            except TypeError:
                print(f'Cant load from file: {file_name} ERROR: TE')
        
    
    def list_movies(self):

        print(f"Movies in total: {len(self.movies)}")
        print(f"{'Movie':<45} {'Rating':<7} {'Release':<7}")
        for movie in self.movies:
            print(f"{movie.title:<45} {movie.rating:<7} {movie.release_year}")
            
    def add_movie(self):
        """
        Adds a movie to the movies database and saves the new data to `movies.json`.
        """
        title =  get_user_input_colorized("Movie title: ")
        rating = convert_to_float(get_user_input_colorized("Movie rating: "))
        release_year = convert_to_float(get_user_input_colorized("Movie release year: "))
        
        if not title:
            error(MSG_NO_TITLE)
        
        if release_year < 1891:
            error(MSG_KINETOSSCOPE_NOT_INVENTED_YET)
            return
        if not rating: 
            error(MSG_RATING_IS_NOT_NUMERIC)
            return
        if rating > 10:
            error(MSG_WRONG_RATING)
            return
        
        if title not in [i.title for i in self.movies]:
            
            temp_movie = Movie(
                {
                    "title": title,
                    'rating': rating,
                    "release_year": int(release_year)
                }
            )
            self.movies.append(temp_movie)
        self.save_movies() 
    
    def remove_movie(self):
        """
        Deletes a movie from the movies database and saves the new data to `movies.json`.
        """
        title =  get_user_input_colorized("Movie title: ")
        
        if not title:
            error(MSG_NO_TITLE)
            
        if title in self.titles:
            
            self.movies.pop(self.titles.index(title))
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
        self.save_movies()  
         
    def edit_movie(self):
        """
        Updates a movie from the movies database and saves the new data to `movies.json`.
        """
        title =  get_user_input_colorized("Movie title: ")
        
        if not title:
            error(MSG_NO_TITLE)
        
        if title not in self.titles:
            error(MSG_MOVIE_DOESNT_EXIST)
            return
        
        rating = convert_to_float(get_user_input_colorized("Movie rating: "))
        
        if not rating: 
            error(MSG_RATING_IS_NOT_NUMERIC)
            return
        if rating > 10:
            error(MSG_WRONG_RATING)
            return
        if title in self.titles:
            self.movies[self.titles.index(title)].rating = rating
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
        self.save_movies() 
        
    def print_stats(self):
        """ print movie stats like title, rating & release_year in a formatted way """
        ratings = [i.rating for i in self.movies]
        median = ratings.copy()
        median.sort()
        median_hlen = len(median)//2
        if len(median) % 2:
            median = median[median_hlen]
        else:
            
            _median_1 = median[median_hlen]
            median.sort(reverse=True)
            median = round((median[median_hlen] +_median_1) / 2,2)
            print(median)
        average = sum(ratings) / len(ratings)
        worst, rating_w = [],11
        best, rating_b = [],-1
        
        for movie in self.movies:
            if movie.rating > rating_b:
                best.append(movie.title)
                rating_b = movie.rating
            if movie.rating < rating_w:
                worst.append(movie.title)
                rating_w = movie.rating
        
        print(f"Average rating: {round(average,2)}. Median rating: {median}.\n{"-"*15}")
        print(f'Best Rating{"s" if len(best) > 1 else ""}\n{"-"*15}')
        for b in best:
            print(f"Rating: {b} with {rating_b}/10")
        print(f'Worst Rating{"s" if len(worst) > 1 else ""}\n{"-"*15}')
        for w in worst:
            print(f"Rating: {w} with {rating_w}/10. ")
        
    def print_random_movie(self):
        """ get a random movie and print it in a formatted way"""
        rnd_movie = [i for i in self.movies][randint(0,len(self.movies)-1)]
        print(f"{rnd_movie.title}: {rnd_movie.rating} released in: {rnd_movie.release_year}")
    
    def print_movies_by_rank(self):
        """ get all movies by rank and print it in a formatted way"""
        listed = [[i.rating,i.title] for i in self.movies]
        listed = sorted(listed,key=lambda x: x[1],reverse=True)
        for n, r in listed:
            print(f"{r:<35} {n}/10")
    def print_search(self):
        """ 
        a searching method to get movies
        """
        value = get_user_input_colorized("Search: ").lower()
        for movie in self.movies:
            if value.lower() in movie.title.lower():
                print(f"{movie.title:<45} {movie.rating:<7} {movie.release_year}")

    def plot_movies(self):
        """ Generates and displays a histogram of movie ratings. """
        plt.hist([i.rating for i in self.movies])
        plt.show()
    
    def byebye(self):
        """ The last thing the app will do before close """
        
        print('bye!')
    
    def update(self,inp):
        """
        Acts as a dispatcher for various movie management operations based on user input.

        This method takes a string input, typically representing a user's menu choice,
        and calls the corresponding movie-related method within the class.
        """
        match inp:
            case '0': 
                self.isrunning = False
                self.byebye()
            case "1": self.list_movies()
            case "2": self.add_movie()
            case "3": self.remove_movie()
            case "4": self.edit_movie()
            case "5": self.print_stats()
            case "6": self.print_random_movie()
            case "7": self.print_search()
            case "8": self.print_movies_by_rank()
            case "9": self.plot_movies()
            case _: error(MSG_INVALID_INPUT)         

def main():
    while MR.isrunning:
        print("""\033[J
********** My Movies Database **********

Menu:
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram 
        """)

        MR.update(get_user_input_colorized("Enter choice 1-9: "))
    
        get_user_input_colorized("Press Enter to continue")


if __name__ == "__main__":
    MR = MovieRank()
    main()
