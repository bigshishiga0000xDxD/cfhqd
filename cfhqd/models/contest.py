from pydantic import BaseModel

class RatingChangeModel(BaseModel):
    handle: str
    oldRating: int
    newRating: int

class ContestModel(BaseModel):
    id: int
    name: str
    result: list[RatingChangeModel]
