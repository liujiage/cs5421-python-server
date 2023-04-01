from .parser import JsonPathXParser
from ..helper import convert

movie_dict = {
    'movie': [
        {'title': 'Reservoir Dogs', 'director': 'Quentin Tarantino', 'year': 1992, 'cast': ['Harvey Keitel', 'Tim Roth', 'Michael Madsen', 'Chris Penn']}, 
        {'title': 'Pulp Fiction', 'director': 'Quentin Tarantino', 'year': 1994, 'cast': ['John Travolta', 'Uma Thurman', 'Samuel L. Jackson', 'Bruce Willis']}, 
        {'title': 'Jackie Brown', 'director': 'Quentin Tarantino', 'year': 1997, 'cast': ['Pam Grier', 'Samuel L. Jackson', 'Robert Forster', 'Bridget Fonda', 'Michael Keaton', 'Robert De Niro']}, 
        {'title': 'Kill Bill: Vol. 1', 'director': 'Quentin Tarantino', 'year': 2003, 'cast': ['Uma Thurman', 'David Carradine', 'Daryl Hannah', 'Michael Madsen', 'Lucy Liu', 'Vivica A. Fox']}, 
        {'title': 'Kill Bill: Vol. 2', 'director': 'Quentin Tarantino', 'year': 2004, 'cast': ['Uma Thurman', 'David Carradine', 'Daryl Hannah', 'Michael Madsen', 'Vivica A. Fox']}, 
        {'title': 'Taxi Driver', 'director': 'Martin Scorsese', 'year': 1976, 'cast': ['Robert De Niro', 'Jodie Foster', 'Cybill Schepherd']}, 
        {'title': 'Goodfellas', 'director': 'Martin Scorsese', 'year': 1990, 'cast': ['Robert De Niro', 'Ray Liotta', 'Joe Pesci']}, 
        {'title': 'The Age of Innocence', 'director': 'Martin Scorsese', 'year': 1993, 'cast': ['Daniel Day-Lewis', 'Michelle Pfeiffer', 'Winona Ryder']}, 
        {'title': 'Mean Streets', 'director': 'Martin Scorsese', 'year': 1973, 'cast': ['Robert De Niro', 'Harvey Keitel', 'David Proval']}
    ]
}

parser = JsonPathXParser()
parser.build()

test_string_1 = '$'                     # pass
test_string_2 = '$.movie'               # pass
test_string_3 = '$[1]'                  # pass
test_string_4 = '$[0:2]'                # pass
test_string_5 = '$.movie[1:3]'          # pass
test_string_6 = '$.movie[1]'            # pass
test_string_7 = '$.movie[1]["title"]'   # pass
test_string_8 = '$.movie[1].title'      # pass
test_string_9 = '$.movie[*]'            # pass
test_string_10 = '$.movie[1:3]..title'  # pass
test_string_11 = '$.movie[1,3,5]'       # pass

test_string_12 = '$.movie[?(@.title=="Goodfellas")]'    # pass
test_string_13 = '$.movie[?(@.year<1997)]'              # pass
test_string_14 = '$.movie[?(@.year<=1997)]'             # pass
test_string_15 = '$.movie[?(@.year>1997)]'              # pass 
test_string_16 = '$.movie[?(@.year>=1997)]'             # pass
test_string_17 = '$.movie[?(@.title!="Goodfellas")]'    # pass
test_string_18 = '$.movie[?(@.year!=1997)]'             # pass
test_string_19 = '$.movie[?(@.title!="Goodfellas")]'    # pass
test_string_20 = '$.movie[?(@.year==1997)]'             # pass

res = parser.parser.parse(test_string_18)
print(res)
print(convert(movie_dict, res))
