from sqlmodel import SQLModel, Field
from typing import Optional

class Activity(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None
    participants: str = Field(default="[]")

    def to_dict(self):
        import json
        return {
            "description": self.description or "",
            "schedule": self.schedule or "",
            "max_participants": self.max_participants or 0,
            "participants": json.loads(self.participants or "[]")
        }