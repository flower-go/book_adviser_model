# book_adviser_model
Model for suggesting books to read based on previews one.


## How it works?
First, users who likes this book are selected. Then, for every book they read, weighted mean of ratings (by user who read the unput book) is computed. Possile weights are 1,2,3 for input book has 70,80,90 percentile above mean respectively. 

## Used data
Book rating data from following link is used for analysis:
http://www2.informatik.uni-freiburg.de/~cziegler/BX/

## Possible problems & features:
- Input book - right now hard-coded book is J.R.R Tolkien: The Fellowship of the Ring (The Lord of the Rings, Part 1) with ISBN 0345339703
