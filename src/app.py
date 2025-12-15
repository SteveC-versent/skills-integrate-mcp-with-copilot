"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import os
import json

from sqlmodel import Session, select

from .db import init_db, engine
from .models import Activity

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent, "static")), name="static")

# In-memory activity database - used only to bootstrap the DB on first run
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# Initialize DB and ensure activities are present
init_db()
with Session(engine) as session:
    for name, data in activities.items():
        stmt = select(Activity).where(Activity.name == name)
        existing = session.exec(stmt).first()
        if not existing:
            a = Activity(
                name=name,
                description=data.get("description", ""),
                schedule=data.get("schedule", ""),
                max_participants=data.get("max_participants", 0),
                participants=json.dumps(data.get("participants", []))
            )
            session.add(a)
    session.commit()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all activities from the database as a dict"""
    result = {}
    with Session(engine) as session:
        activities_db = session.exec(select(Activity)).all()
        for a in activities_db:
            result[a.name] = {
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": json.loads(a.participants or "[]")
            }
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity (persisted)"""
    with Session(engine) as session:
        stmt = select(Activity).where(Activity.name == activity_name)
        activity = session.exec(stmt).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        participants = json.loads(activity.participants or "[]")
        if email in participants:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        participants.append(email)
        activity.participants = json.dumps(participants)
        session.add(activity)
        session.commit()

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity (persisted)"""
    with Session(engine) as session:
        stmt = select(Activity).where(Activity.name == activity_name)
        activity = session.exec(stmt).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        participants = json.loads(activity.participants or "[]")
        if email not in participants:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        participants.remove(email)
        activity.participants = json.dumps(participants)
        session.add(activity)
        session.commit()

    return {"message": f"Unregistered {email} from {activity_name}"}
