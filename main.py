from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import sys
import os
import logging
log = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler2 = logging.StreamHandler(sys.stdout)
stream_handler2.setFormatter(formatter)
log.setLevel(logging.DEBUG)
log.addHandler(stream_handler)
log.addHandler(stream_handler2)
from pprint import pformat


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    log.debug("debug")
    log.info("info")
    log.warning(f"Headers: {dict(request.headers)!r}")
    log.warning(f"Env: {dict(os.environ)!r}")
    print(f"Headers: {pformat(dict(request.headers))}")
    print(f"Env: {pformat(dict(os.environ))}")
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

