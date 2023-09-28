from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from tools.google_news_scraper import GoogleNewsScraper
from fastapi.responses import FileResponse
from gpt.GPTQuery import GPTQuery
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

app = FastAPI()

cache_dir = '/tmp/cache'  # specify the path to your cache directory
cache_duration = 60 * 60  # specify the duration for which the cache is valid, in seconds

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

scraper = GoogleNewsScraper("https://www.google.com/search")

@app.get("/service-worker.js")
async def read_service_worker():
    return FileResponse("root_static/service-worker.js", media_type="application/javascript")

@app.get("/")
async def read_root(request: Request):
    scraper_output = scraper.search("Politics", 10)
    adapted_data = map_and_validate_scraper_data(scraper_output, "Politics")
    
    return templates.TemplateResponse(
        "index.html", {"request": request, "data": adapted_data}
    )

gpt = GPTQuery()

@app.get("/api/getArticles")
async def get_articles(topic: str):

    cache_key = topic  # create a unique cache key
    cache_file_path = os.path.join(cache_dir, f"{cache_key}.json")
    
    # check if the cache file exists
    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'r') as f:
            cache_data = json.load(f)
        
        # check if the cache is still valid
        if time.time() - cache_data['timestamp'] < cache_duration:
            print("Returning cached articles")
            return cache_data['articles']
        

    scraper_output = scraper.search_many(topic, pages=4)
    
    adapted_data = map_and_validate_scraper_data(scraper_output, topic)

    result_string = ""
    id_to_article_map = {}

    for article in adapted_data:
        title = article['main_article']['title']
        id = article['main_article']['id']
        
        # Append id and title to the result string
        result_string += f"{id}-{title}\n"
        
        # Map id to article for later retrieval
        id_to_article_map[id] = article
    print("querying gpt")
    grouped_articles_json = gpt.group_articles(result_string)

    # Check if grouped_articles_json is a string and if so, convert it to a dictionary
    if isinstance(grouped_articles_json, str):
        grouped_articles_json = json.loads(grouped_articles_json)  # Convert JSON string to a dictionary

    used_articles_ids = set()

    # Loop through each theme in grouped_articles_json
    for theme_group in grouped_articles_json.get('similar_articles', []):
        theme_articles_ids = theme_group.get('similar_articles', [])
        
        if theme_articles_ids:
            main_article_id = theme_articles_ids[0]
            
            if main_article_id in id_to_article_map:
                main_article = id_to_article_map[main_article_id]
                
                # Get ids for additional and related articles
                additional_articles_ids = theme_articles_ids[1:min(3, len(theme_articles_ids))]
                related_articles_ids = theme_articles_ids[3:7]
                
                if additional_articles_ids:
                    main_article['additional_articles'] = [
                        {"title": id_to_article_map[id]['main_article']['title'],
                        "source": id_to_article_map[id]['main_article']['source'],
                        "link": id_to_article_map[id]['main_article']['link']}
                        for id in additional_articles_ids
                    ]
                    used_articles_ids.update(additional_articles_ids)  # Mark articles as used
                
                if related_articles_ids:
                    main_article['related_links'] = [
                        {"title": id_to_article_map[id]['main_article']['title'],
                         "source": id_to_article_map[id]['main_article']['source'],
                        "link": id_to_article_map[id]['main_article']['link']}
                        for id in related_articles_ids
                    ]
                    used_articles_ids.update(related_articles_ids)  # Mark articles as used

    # Now, remove all used articles from adapted_data
    adapted_data = [article for article in adapted_data if article['main_article']['id'] not in used_articles_ids]

    # And also ensure that the main articles in adapted_data are not in used_articles_ids
    adapted_data = [article for article in adapted_data if article['main_article']['id'] not in used_articles_ids]

    result = {"articles": adapted_data, "topic": topic}
    with open(cache_file_path, 'w') as f:
        json.dump({'timestamp': time.time(), 'articles': result}, f)

    return result




def map_and_validate_scraper_data(scraper_output, topic):
    adapted_articles = []
    counter = 0
    for article in scraper_output:
        counter += 1
        try:
            mapped_article = {
                "id": counter,
                "title": article.get("title", "N/A"),
                "source": article.get("source", "N/A"),
                "description": article.get("description", "N/A"),
                "link": article.get("link", "N/A"),
                "image_link": article.get("image_link", "N/A"),
                "date": article.get("date", "N/A"),
            }

            # Validate - throw an error or fill a default value if a key is missing
            for key in ["title", "source", "description", "link", "image_link"]:
                if not mapped_article[key]:
                    raise ValueError(f"Missing value for {key}")

            adapted_articles.append({"main_article": mapped_article})
        except Exception as e:
            print(f"Error adapting article: {e}")

    return adapted_articles
