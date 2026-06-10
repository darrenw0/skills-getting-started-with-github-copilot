"""Pytest configuration and shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI app.
    Resets the activities database before each test to ensure isolation.
    """
    # Reset activities to initial state before each test
    # Define the original state
    original_activities = {
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
        "Basketball Team": {
            "description": "Competitive basketball practices and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and water safety sessions",
            "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and theater production",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Creative art projects including painting and sculpture",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["amelia@mergington.edu", "elijah@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science exploration",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["harper@mergington.edu", "jack@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking and competitive debate",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["charlotte@mergington.edu", "sebastian@mergington.edu"]
        }
    }
    
    # Clear and repopulate the activities dict
    activities.clear()
    for activity_name, activity_data in original_activities.items():
        # Deep copy participants list to avoid shared references
        activities[activity_name] = {
            "description": activity_data["description"],
            "schedule": activity_data["schedule"],
            "max_participants": activity_data["max_participants"],
            "participants": activity_data["participants"].copy()
        }
    
    return TestClient(app)


@pytest.fixture
def test_email():
    """Fixture that provides a valid test email for signup tests."""
    return "testuser@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture that provides sample activity data for testing."""
    return {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "initial_participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    }
