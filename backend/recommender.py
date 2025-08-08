import pickle
import pandas as pd
import requests
import sys
import json
import traceback
import time
import requests

# Load data
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

# def fetch_poster(movie_id):
#     api_key = "a64e74cd8ff46204801b27e7f372479b"
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return ""  # Placeholder or blank
#     except Exception as e:
#         print(f"[ERROR] Failed to fetch poster for movie ID {movie_id}: {e}", file=sys.stderr)
#         return ""



def fetch_poster(movie_id, retries=3, delay=1):
    api_key = "a64e74cd8ff46204801b27e7f372479b"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return ""  # No poster available
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Attempt {attempt+1} failed for movie ID {movie_id}: {e}", file=sys.stderr)
            time.sleep(delay)

    return ""


def recommend(movie):
    movie = movie.lower()
    all_titles = movies['title'].str.lower()

    if movie not in all_titles.values:
        return []

    index = all_titles[all_titles == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:7]

    recommendations = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommendations.append({
            "title": title,
            "poster": poster
        })

    return recommendations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps([]))
        sys.exit(0)

    movie = sys.argv[1]
    try:
        result = recommend(movie)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": "Internal Python error", "details": traceback.format_exc()}))
        sys.exit(1)
