from pydantic import BaseModel, validator
from typing import List, Optional


class PayloadRow(BaseModel):
    """Sample:

    {
      "Id": 1,
      "url": "https://www.kinopoisk.ru/film/5012/",
      ...
    }
    """

    id: int
    url: str


class Payload(BaseModel):
    """Sample:

    {
      "type": "records.after.insert",
      "id": "...",
      "data": {
        ...
        "rows": [
          {
            "Id": 1,
            "url": "https://www.kinopoisk.ru/film/5012/",
            ...
          }
        ]
      }
    }
    """

    data: dict
    items: Optional[List[PayloadRow]]

    @validator("items", pre=True, always=True)
    def validate_items(cls, value, values):
        return values["data"]["rows"]
