from pydantic import BaseModel

class IMEIInfo(BaseModel):
    status: str
    data: dict