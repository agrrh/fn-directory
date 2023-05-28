from datetime import datetime

from pydantic import BaseModel, Field


class Payload(BaseModel):
    """
    Sample:
    {
        "name": "update deployment",
        "message": "Successfully updated deployment default/wd (karolisr/webhook-demo:0.0.10)",
        "createdAt": "2017-07-08T10:08:45.226565869+01:00"
    }
    """

    name: str
    message: str
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
