"""
Program for recomendation of books according to one favourite book.
"""
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

"""
Read all data from dataset.
"""


def load_data():
    # TODO: predelat na relativni cestu
    book_ratings = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Book-Ratings.csv',
                               error_bad_lines=False, delimiter=';', encoding='latin-1',
                               dtype={'User-ID': 'category', 'ISBN': 'category', 'Book-Rating': np.int32})
    book_list = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Books.csv', delimiter=';',
                            error_bad_lines=False, encoding='latin-1')
    # users = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Users.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1', )
    return book_ratings, book_list


"""
Preprocessing data, check data quality
"""


def book_ratings_preprocess(books, list):
    print(len(books))
    books = books[books['ISBN'].isin(list)]
    print(len(books))
    books.loc[:, 'Book-Rating'] = books['Book-Rating'].replace(0, np.NaN)
    books = books[books['Book-Rating'].notnull()].copy()
    print(len(books))
    # books = books.iloc[:10]
    return books


"""
vypocet
"""


def calculate_mean(books_input):
    # prumer pro kazdeho uzivatele
    books = books_input
    kukykuky = books.groupby('User-ID')['Book-Rating'].transform('mean')
    books['rating_mean'] = kukykuky
    books = books.drop_duplicates('User-ID')

    # odstranim uzivatele co nic nehodnotili
    books = books[books['rating_mean'].notnull()].copy()
    return books


################################################################


book_ratings, book_list = load_data()
book_ratings = book_ratings_preprocess(book_ratings, book_list['ISBN'])
RATINGS = book_ratings
book_ratings = calculate_mean(book_ratings)

# find user with tolkien above mean
tolkien = '0345339703'

selected_users = RATINGS[RATINGS['ISBN'] == tolkien]
selected_users_above = selected_users[selected_users['Book-Rating'] > selected_users['rating_mean']]

selected_users_above_list = selected_users_above['User-ID']

# ziskam matici: uzivatele a kniha
selected_data = RATINGS[RATINGS['User-ID'].isin(selected_users_above_list)]
selected_data = selected_data[selected_data['ISBN'] != tolkien]
selection_matrix = selected_data.pivot(index='User-ID', columns='ISBN', values='Book-Rating')

# TODO chci percentile

# TODO odchylka
# spočítat průměry pro knížky

grouped_data = selected_data[['ISBN']]
grouped_data['mean_rating'] = selected_data.groupby(['ISBN'])['Book-Rating'].transform("mean")
grouped_data.drop_duplicates('ISBN')
grouped_data = grouped_data.sort_values('mean_rating', ascending=False)

print("Finished.")
print(grouped_data)

# fancy vypis
recommended_isbns = grouped_data.head(10)['ISBN']
book_names = book_list[book_list['ISBN'].isin(recommended_isbns)]
book_names_only = book_names.loc[:, ['Book-Title', 'Book-Author']]
print("I recommend you these books:")

print(book_names_only)
