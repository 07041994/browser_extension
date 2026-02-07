from pydantic import BaseModel

class ScreenshotRequest(BaseModel):
    image: str = None
    filename: str = None
    url:str = None
