from fastapi import FastAPI, File, UploadFile, Request
from deta import Drive
from fastapi.responses import StreamingResponse,HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
files = Drive("files")
templates = Jinja2Templates(directory="templates")

@app.get("/web", response_class=HTMLResponse)
async def index(request: Request):
    '''
    This is a HTML Response. Which has the html template to play the stream.
    '''
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/")
def upload(file: UploadFile = File(...)):
    return files.put(file.filename, file.file)


@app.get("/")
def list_files():
    return files.list()



@app.get("/webi")
def webi():
    name="hello.mp4"
    video_file = files.get(name)
    ext = name.split(".")[1]
    return StreamingResponse(video_file.iter_chunks(), media_type=f"video/{ext}")