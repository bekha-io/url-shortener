from fastapi import FastAPI, Request, status, responses, Body
from utils import CustomJSONResp

from database import ShortUrl, UrlRedirect

app = FastAPI()


@app.get('/{short_url}', status_code=301)
async def get_url(short_url: str, request: Request):

    url_item: ShortUrl = ShortUrl.get_or_none(id=short_url)

    if not url_item:
        return CustomJSONResp(
            status_code=status.HTTP_404_NOT_FOUND
        )

    UrlRedirect.new(url_item, request.client.host)
    return responses.RedirectResponse(
        url_item.url
    )


@app.post("/generate", response_class=CustomJSONResp)
async def shorten_url(url: str, request: Request):

    url_item = ShortUrl.new(url, request.client.host)
    item = {
            'longUrl': url_item.url,
            'shortUrl': request.url_for('get_url', short_url=url_item.id)
    }

    return CustomJSONResp(data=item)