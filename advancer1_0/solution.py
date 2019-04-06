"""
Program for recomendation of books according to one favourite book.
"""
import pandas as pd
import numpy as np

"""
Read all data from dataset.
"""
# TODO: predelat na relativni cestu
book_ratings = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Book-Ratings.csv',
                           error_bad_lines = False, delimiter = ';', encoding = 'latin-1',
                           dtype={'User-ID': 'category', 'ISBN': 'category', 'Book-Rating': np.int32})
#books = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Books.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1')
#users = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Users.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1', )


"""
Preprocessing data, check data quality
"""
book_ratings['Book-Rating'] = book_ratings['Book-Rating'].replace(0, np.NaN)
book_ratings = book_ratings.iloc[:10]

"""
vypocet
"""
#prumer pro kazdeho uzivatele
book_ratings['rating_mean'] = book_ratings.groupby('User-ID')['Book-Rating'].transform('mean')
book_ratings = book_ratings.drop_duplicates(['User-ID'])

#odstranim uzivatele co nic nehodnotili
book_ratings = book_ratings[book_ratings['rating_mean'].notnull()]

print(book_ratings)


#print(book_ratings)
print("Finished.")
