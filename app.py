from typing import Annotated
from fastapi import FastAPI, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from logger.logg import log
import asyncio
from datetime import datetime
from processing.processing import save_screenshot_async


app = FastAPI(title="Browser_extension", version="1.0.0")


origins = ["*"]
app.add_middleware(    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

@app.get("/")
async def root():
    return {"message": "Hello Extension"}


@app.post("/screenshot")
def capture_full_pages(request:  Annotated[list[str], Form()], background_tasks: BackgroundTasks):
    
        
    background_tasks.add_task(save_screenshot, request)
    return {"status": "screenshot capture initiated"}

def save_screenshot(request: list[str]):
    time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    asyncio.run(save_screenshot_async(request))
    time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.info(f"Screenshot capture started at: {time1} and ended at: {time2}")
    log.info(f"Total time taken: {datetime.strptime(time2, '%Y-%m-%d %H:%M:%S') - datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')}")


