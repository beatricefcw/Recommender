import pandas as pd

# load metadata
metadata = pd.read_csv('movies_metadata.csv', low_memory=False)
print(metadata.head(3))

# calculate mean vote across the whole report
C = metadata['vote_average'].mean()
print(C)

# calculate minimum no of votes required to be in chart
# 90th percentile, top 10%
m = metadata['vote_count'].quantile(0.90)
print(m)

# filtered qualified movies based on m 
q_movies = metadata.copy().loc[metadata['vote_count'] >= m]
print(q_movies.shape)
print(metadata.shape)

# calculate weighted rating of EACH movie
def weighted_rating(dataset, m=m, C=C):
    v = dataset['vote_count']
    R = dataset['vote_average']
    return (v/(v+m)*R) + (m/(m+v)*C)

# create new column, applied function weighted rating to each row
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

# sort to get top results
q_movies = q_movies.sort_values('score', ascending=False)
print(q_movies[['title', 'vote_count', 'vote_average', 'score']].head(20))