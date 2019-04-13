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


def get_weights(selected_book, border1, border2, border3):
    if selected_book >= border1:
        return 3
    elif selected_book >= border2:
        return 2
    elif selected_book >= border1:
        return 1
    else:
        return 0

def get_groups(data, percentile90, percentile80, percentile70):
    data = data.reset_index(drop=True)
    print(len(percentile_80))
    for index, row in data.iterrows():
        print(index)

        weight = get_weights(row['Book-Rating'], percentile90[index], percentile80[index], percentile70[index])

################################################################


book_ratings, book_list = load_data()
book_ratings = book_ratings_preprocess(book_ratings, book_list['ISBN'])
RATINGS = book_ratings
book_ratings = calculate_mean(book_ratings)

# find user with tolkien above mean
tolkien = '0345339703'

selected_users = RATINGS[RATINGS['ISBN'] == tolkien]

selected_users_above = selected_users[selected_users['Book-Rating'] / selected_users['rating_mean'] > 1]

selected_users_above_list = selected_users_above['User-ID']


# ziskam matici: uzivatele a kniha
selected_data = RATINGS[RATINGS['User-ID'].isin(selected_users_above_list)]

selection_matrix = selected_data.pivot(index='User-ID', columns='ISBN', values='Book-Rating')

percentile_90 = selection_matrix.apply(lambda x: np.nanpercentile(x, 90), axis=1)
percentile_80 = selection_matrix.apply(lambda x: np.nanpercentile(x, 80), axis=1)
percentile_70 = selection_matrix.apply(lambda x: np.nanpercentile(x, 70), axis=1)


get_groups(selected_users, percentile_90, percentile_80, percentile_70)
#TODO get user in groups


selected_data = selected_data[selected_data['ISBN'] != tolkien]
grouped_data = selected_data[['ISBN']]
grouped_data['mean_rating'] = selected_data.groupby(['ISBN'])['Book-Rating'].transform("mean")
# grouped_data['10th_percentile'] = selected_data['']
grouped_data.drop_duplicates('ISBN')
grouped_data = grouped_data.sort_values('mean_rating', ascending=False)

print("Finished.")
print(selection_matrix)

# fancy vypis
recommended_isbns = grouped_data.head(10)['ISBN']
book_names = book_list[book_list['ISBN'].isin(recommended_isbns)]
book_names_only = book_names.loc[:, ['Book-Title', 'Book-Author']]
print("I recommend you these books:")

print(book_names_only)
