# book_adviser_model
Model for suggesting books to read based on previews one.


How it works?
First, users who likes this book are selected. Then, for every book they read, weighted mean of ratings (by user who read the unput book) is computed. Possile weights are 1,2,3 for input book has 70,80,90 percentile above mean respectively. 

