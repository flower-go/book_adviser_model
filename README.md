# book_adviser_model
Model for suggesting books to read based on previews one.


## How it works?
First, users who likes this book are selected. Then, for every book they read, weighted mean of ratings (by user who read the unput book) is computed. Possile weights are 1,2,3 for input book has 70,80,90 percentile above mean respectively. 

## Used data
Book rating data from following link is used for analysis:
http://www2.informatik.uni-freiburg.de/~cziegler/BX/

## Possible problems & features:
- **Input book** - right now hard-coded book is J.R.R Tolkien: The Fellowship of the Ring (The Lord of the Rings, Part 1) with ISBN 0345339703. It can be changed in variable 'tolkien'.
- **Input book identification** - In the case of Lord of the Rings not only different parts can be selected, but also books in different languages, which has different ISBN. One to deal with this problems is has a better structure of the data and know language mutations of same book. It can be done manually. After that we could select users and weights by multiple ISBNs.
- **Changes in the model** - As the model is based on data from some book rating web page, they could change as users reads new books or changes they ratings. In our model, this can be easily reflected, because every new query computes all means etc newly from the beginnning.
- **Computing cost** - Computing averages newly all the time can be really expensive as the data can grow to be very large. For adressing this issue iterative computing of averages can be used, so with every new entry, only few small operations needs to be done.

