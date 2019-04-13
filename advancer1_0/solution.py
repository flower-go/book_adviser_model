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
    book_ratings = pd.read_csv('BX-Book-Ratings.csv',
                               error_bad_lines=False, delimiter=';', encoding='latin-1',
                               dtype={'User-ID': 'category', 'ISBN': 'category', 'Book-Rating': np.int32})
    book_list = pd.read_csv('BX-Books.csv', delimiter=';',
                            error_bad_lines=False, encoding='latin-1')
    # users = pd.read_csv('C:\\Users\\pdoubravova\\Documents\\work\\advancer1_0\\BX-Users.csv', delimiter = ';', error_bad_lines = False, encoding = 'latin-1', )
    return book_ratings, book_list


"""
Preprocessing data, check data quality
"""


def book_ratings_preprocess(books, list):
    books = books[books['ISBN'].isin(list)]
    books.loc[:, 'Book-Rating'] = books['Book-Rating'].replace(0, np.NaN)  # TODO je to potřeba?
    books = books[books['Book-Rating'].notnull()].copy()
    # books = books.iloc[:10]
    return books


def calculate_mean(books_input):
    # prumer pro kazdeho uzivatele
    books = books_input
    kukykuky = books.groupby('User-ID')['Book-Rating'].transform('mean')
    books['usr_rat_mean'] = kukykuky
    # books = books.drop_duplicates('User-ID')

    # odstranim uzivatele co nic nehodnotili
    books = books[books['usr_rat_mean'].notnull()].copy()
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


def vypis(data, list, pocet):
    recommended_isbns = data.head(pocet)
    book_names = list[list['ISBN'].isin(recommended_isbns.index)]
    book_names_only = book_names.loc[:, ['Book-Title', 'Book-Author']]
    print("I recommend you these books:")
    print(book_names_only)


def get_groups(data, percentile90, percentile80, percentile70):
    data = data.reset_index(drop=True)
    weights = []
    print(len(percentile80))
    for index, row in data.iterrows():
        weight = get_weights(row['Book-Rating'], percentile90[index], percentile80[index], percentile70[index])
        weights.append(weight)
    return pd.Series(data=weights, index=data['User-ID'])


def main():
    book_ratings, book_list = load_data()
    book_ratings = book_ratings_preprocess(book_ratings, book_list['ISBN'])
    book_ratings = calculate_mean(book_ratings)  # TODO tady se to meni na unique user, to nechceme

    # find user with tolkien above mean
    tolkien = '0345339703'  # TODO je to nerozumnejsi kniha?

    selected_tolkien_only = book_ratings[book_ratings['ISBN'] == tolkien]

    # selected_users_above = selected_tolkien_only[selected_tolkien_only['Book-Rating'] / selected_tolkien_only['usr_rat_mean'] > 1]
    tolkien_users_list = selected_tolkien_only['User-ID']

    # ziskam matici: uzivatele a kniha
    tolkien_usrs_ratings = book_ratings[book_ratings['User-ID'].isin(tolkien_users_list)]  # TODO tohle je nějak špatně
    selection_matrix = tolkien_usrs_ratings.pivot(index='User-ID', columns='ISBN', values='Book-Rating')

    percentile_90 = selection_matrix.apply(lambda x: np.nanpercentile(x, 90), axis=1)
    percentile_80 = selection_matrix.apply(lambda x: np.nanpercentile(x, 80), axis=1)
    percentile_70 = selection_matrix.apply(lambda x: np.nanpercentile(x, 70), axis=1)

    weights = get_groups(selected_tolkien_only, percentile_90, percentile_80, percentile_70)
    selection_matrix = selection_matrix[selection_matrix.index.isin(weights[weights != 0].index)]

    weights = weights[weights!=0]
    book_means = selection_matrix.mul(weights, axis=0)
    book_means = book_means.sum().sort_values(ascending=False)

    # fancy vypis
    vypis(book_means, book_list, 40)


if __name__ == "__main__":
    main()
