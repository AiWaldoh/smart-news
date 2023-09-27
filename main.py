from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    data = {
        "columns": [
            {
                "title": "Politics",
                "articles": [
                    {
                        "main_article": {
                            "title": "Political Article Title",
                            "source": "CNN",
                            "description": "Lorem ipsum...",
                            "link": "#",
                            "image_link": "https://lh3.googleusercontent.com/proxy/Xo12q8E8BCGE6KBAU1Zhms_q9DrTw2AlVkkPvN1zw-tV7LSoYGIUoDJKSmbfo4iRJyuHJvtxxV0TWKPCrPr-toqWtlA_aIds9r48_Qjve478QjISRQKhitkDa-CbIwuZ4rFjezKehDCDderBn3_IEzj39OjGES_MoF_D03Y53BtiOV1dkHsOnTyVO8XyYTMT2v5cVR7C_4p8cgV8RT8vEdNn7f09oObXmLK7Xq1RSUQzLB1DzEzR_ip5FcY8TNIgoTvQrhz9nA=s0-w100-h100-dcGQSmi40L"
                        },
                        "additional_articles": [
                            {
                                "title": "Additional Article Title",
                                "source": "Additional Source",
                                "link": "#"
                            }
                        ],
                        "related_links": [
                            {
                                "title": "Related from Fox News",
                                "link": "#"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Sports",
                "articles": [
                    {
                        "main_article": {
                            "title": "Sports Article Title",
                            "source": "ESPN",
                            "description": "Lorem ipsum...",
                            "link": "#",
                            "image_link": "https://lh3.googleusercontent.com/proxy/Xo12q8E8BCGE6KBAU1Zhms_q9DrTw2AlVkkPvN1zw-tV7LSoYGIUoDJKSmbfo4iRJyuHJvtxxV0TWKPCrPr-toqWtlA_aIds9r48_Qjve478QjISRQKhitkDa-CbIwuZ4rFjezKehDCDderBn3_IEzj39OjGES_MoF_D03Y53BtiOV1dkHsOnTyVO8XyYTMT2v5cVR7C_4p8cgV8RT8vEdNn7f09oObXmLK7Xq1RSUQzLB1DzEzR_ip5FcY8TNIgoTvQrhz9nA=s0-w100-h100-dcGQSmi40L"
                        },
                        "additional_articles": [
                            {
                                "title": "Additional Sports Article",
                                "source": "BBC Sports",
                                "link": "#"
                            }
                        ],
                        "related_links": [
                            {
                                "title": "Related from NBC Sports",
                                "link": "#"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})