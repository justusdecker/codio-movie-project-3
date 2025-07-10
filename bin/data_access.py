from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db" # Define the database URL

engine = create_engine(DB_URL, echo=True) # Create the engine echo prints the sql querys

# Create the movies table if it does not exist
def create_database():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT NOT NULL
            )
        """))
        connection.commit()
    

def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(title, year, rating, poster):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"), 
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"), 
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' removed successfully.")
        except Exception as e:
            print(f"Error: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET title = :title, rating = :rating WHERE title = :title;"), 
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")


create_database()
# Test adding a movie
add_movie("Inception", 2010, 8.8,'N/A')

# Test listing movies
movies = list_movies()
print(movies)

# Test updating a movie's rating
update_movie("Inception", 9.0)
print(list_movies())

# Test deleting a movie
delete_movie("Inception")
print(list_movies())  # Should be empty if it was the only movie