import pickle
import json

movies = pickle.load(open("model/movie_list.pkl", "rb"))
titles = movies['title'].tolist()

with open("../frontend/public/movie_list.json", "w", encoding="utf-8") as f:
    json.dump(titles, f)
