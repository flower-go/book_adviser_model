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
    # books = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Books.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1')
    # users = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Users.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1', )
    return book_ratings


"""
Preprocessing data, check data quality
"""


def book_ratings_preprocess(books):
    books.loc[:, 'Book-Rating'] = books['Book-Rating'].replace(0, np.NaN)
    books = books.iloc[:10]
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


book_ratings = load_data()
RATINGS = book_ratings
book_ratings = book_ratings_preprocess(book_ratings)
book_ratings = calculate_mean(book_ratings)
print(book_ratings)

# print(book_ratings)
print("Finished.")
