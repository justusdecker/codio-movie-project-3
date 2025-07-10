from random import randint

import matplotlib.pyplot as plt

from bin.constants import *
from bin.modules import *

import bin.data_access as storage

from bin.api_access import get_movie

class MovieRank:
    def __init__(self):
        self.isrunning = True

    @property
    def titles(self) -> list[str]:
        return [i for i in storage.list_movies()]
    
    #TODO Movies
    
    def list_movies(self):
        movies = storage.list_movies()
        print(f"Movies in total: {len(movies)}")
        print(f"{'Movie':<45} {'Rating':<7} {'Release':<7}")
        for movie in movies:
            print(f"{movie:<45} {movies[movie][RATING]:<7} {movies[movie][YEAR]}")
            
    def add_movie(self):
        
        title =  get_user_input_colorized("Movie title: ")

        #! ERRORHANDLING
        if not title:
            error(MSG_NO_TITLE)
        movie_data = get_movie(title)
        
        if movie_data['Response'] == "False":
            error(movie_data['Error'])
            return
        image = movie_data['Poster']
        
        rating = movie_data['imdbRating']
        if rating == 'N/A':
            rating = -1 # Cant get rating
            
        release_date = movie_data['Released']
        if release_date == 'N/A':
            release_date = '01 Jan 1980' # Cant get release_year
        release_year = release_date.split(' ')[2]
        
        if title not in [key for key in storage.list_movies()]:
            storage.add_movie(title, int(release_year),rating,poster=image)
    
    def remove_movie(self):
        """
        Deletes a movie from the movies database and saves the new data to `movies.json`.
        """
        title =  get_user_input_colorized("Movie title: ")
        
        if not title:
            error(MSG_NO_TITLE)
            
        if title in self.titles:
            storage.delete_movie(title)
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
         
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
            storage.update_movie(title,rating)
        else:
            error(MSG_MOVIE_DOESNT_EXIST)
        
    def print_stats(self):
        """ print movie stats like title, rating & release_year in a formatted way """
        movies = storage.list_movies()
        
        ratings = [movies[i][RATING] for i in movies]
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
        
        for movie in movies:
            rating_c = movies[movie][RATING]
            title = movie
            if rating_c > rating_b:
                best.append(title)
                rating_b = rating_c
            if rating_c < rating_w:
                worst.append(title)
                rating_w = rating_c
        
        print(f"Average rating: {round(average,2)}. Median rating: {median}.\n{"-"*15}")
        print(f'Best Rating{"s" if len(best) > 1 else ""}\n{"-"*15}')
        for b in best:
            print(f"Rating: {b} with {rating_b}/10")
        print(f'Worst Rating{"s" if len(worst) > 1 else ""}\n{"-"*15}')
        for w in worst:
            print(f"Rating: {w} with {rating_w}/10. ")
        
    def print_random_movie(self):
        """ get a random movie and print it in a formatted way"""
        movies = storage.list_movies()
        rnd_movie = [i for i in movies][randint(0,len(movies)-1)]
        print(f"{rnd_movie}: {movies[rnd_movie][RATING]} released in: {int(movies[rnd_movie][YEAR])}")
    
    def print_movies_by_rank(self):
        """ get all movies by rank and print it in a formatted way"""
        movies = storage.list_movies()
        listed = [[movies[i][RATING],i] for i in movies]
        listed = sorted(listed,key=lambda x: x[1],reverse=True)
        for n, r in listed:
            print(f"{r:<35} {n}/10")
            
    def print_search(self):
        """ 
        a searching method to get movies
        """
        movies = storage.list_movies()
        value = get_user_input_colorized("Search: ").lower()
        for movie in movies:
            if value.lower() in movie.lower():
                print(f"{movie:<45} {movies[movie][RATING]:<7} {movies[movie][YEAR]}")

    def plot_movies(self):
        """ Generates and displays a histogram of movie ratings. """
        movies = storage.list_movies()
        plt.hist([movies[i][RATING] for i in movies])
        plt.show()
    
    def generate_html(self):
        
        with open('_static\\index_template.html') as file_in:
            html = file_in.read()

        replacer = """

        """
        movies = storage.list_movies()
        
        for movie in movies:
            replacer += f"""
<li>
<div class="movie">
    <img class="movie-poster" src="{movies[movie][POSTER]}">
    <div class="movie-title">{movie}</div>
    <div class="movie-year">{movies[movie][YEAR]}</div>
</div>
</li>
"""
    
        html = html.replace('__TEMPLATE_MOVIE_GRID__',replacer)
        html = html.replace('__TEMPLATE_TITLE__','Movie Project V3')
        with open('index.html', 'w') as file_out:
            file_out.write(html)
            
        with open('_static\\style.css') as file_in:
            with open('style.css', 'w') as file_out:
                file_out.write(file_in.read())
        print("Website was generated successfully.")
        
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
            case "10": self.generate_html()
            case _: error(MSG_INVALID_INPUT)         

def main():
    while MR.isrunning:
        print("""\033[J
********** My Movies Database **********

Menu:
1.  List movies
2.  Add movie
3.  Delete movie
4.  Update movie
5.  Stats
6.  Random movie
7.  Search movie
8.  Movies sorted by rating
9.  Create Rating Histogram
10. Generate Html
        """)

        MR.update(get_user_input_colorized("Enter choice 1-9: "))
    
        get_user_input_colorized("Press Enter to continue")


if __name__ == "__main__":
    MR = MovieRank()
    main()
