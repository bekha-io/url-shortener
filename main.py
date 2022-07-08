from fastapi import FastAPI, Request, status, responses
from fastapi.templating import Jinja2Templates

from utils import CustomJSONResp, TemplateContext
from database import ShortUrl, UrlRedirect

app = FastAPI()


templates = Jinja2Templates(directory="./templates")


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


@app.post("/shorten", response_class=CustomJSONResp)
async def shorten_url(url: str, request: Request):

    url_item = ShortUrl.new(url, request.client.host)
    item = {
            'longUrl': url_item.url,
            'shortUrl': request.url_for('get_url', short_url=url_item.id)
    }

    return CustomJSONResp(data=item)


@app.get('/', response_class=responses.HTMLResponse)
async def index_page(request: Request):

    ctx = TemplateContext()
    ctx.urls = ShortUrl.get_by_ip(request.client.host)
    ctx.total_urls = ShortUrl.select().count()
    ctx.total_users = ShortUrl.select(ShortUrl.ip_requested).distinct().count()
    ctx.total_redirects = UrlRedirect.select().count()

    return templates.TemplateResponse(
        'index.html', {
            'request': request,
            'context': ctx,
        }
    )