from pydantic import BaseModel

class TerroristValid(BaseModel):
    name: str
    location: str
    danger_rate: int