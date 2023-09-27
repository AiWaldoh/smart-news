from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from tools.google_news_scraper import GoogleNewsScraper

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
scraper = GoogleNewsScraper()


@app.get("/")
async def read_root(request: Request):
    scraper_output = scraper.search("Politics", 10)
    adapted_data = map_and_validate_scraper_data(scraper_output, "Politics")
    return templates.TemplateResponse(
        "index.html", {"request": request, "data": adapted_data}
    )


@app.get("/api/getArticles")
async def get_articles(topic: str):
    scraper_output = scraper.search(topic, 10)
    adapted_data = map_and_validate_scraper_data(scraper_output, topic)
    return {"articles": adapted_data, "topic": topic}


def map_and_validate_scraper_data(scraper_output, topic):
    adapted_articles = []
    for article in scraper_output:
        try:
            mapped_article = {
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
