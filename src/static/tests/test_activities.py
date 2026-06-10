"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_success(self, client):
        """
        AAA Test: Verify GET /activities returns 200 status code.
        
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Verify status code is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """
        AAA Test: Verify all 9 activities are returned.
        
        Arrange: Client is ready
        Act: Make GET request to /activities
        Assert: Verify response contains exactly 9 activities
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9

    def test_get_activities_returns_expected_activity_names(self, client):
        """
        AAA Test: Verify returned activities have the expected names.
        
        Arrange: Expected activity names
        Act: Make GET request to /activities and extract activity names
        Assert: Verify expected activities are in the response
        """
        # Arrange
        expected_activities = {
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Swimming Club", "Drama Club", "Art Studio", "Science Club", "Debate Team"
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        actual_activity_names = set(activities.keys())
        
        # Assert
        assert actual_activity_names == expected_activities

    def test_get_activities_returns_proper_structure(self, client, sample_activity):
        """
        AAA Test: Verify each activity has required fields.
        
        Arrange: Define required fields for an activity
        Act: Get activities and check structure of first activity
        Assert: Verify all required fields are present
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities[sample_activity["name"]]
        
        # Assert
        assert set(chess_club.keys()) == required_fields

    def test_get_activities_returns_correct_participant_lists(self, client, sample_activity):
        """
        AAA Test: Verify participant list is correct for a known activity.
        
        Arrange: Sample activity with known participants
        Act: Get activities and extract participants for sample activity
        Assert: Verify participants match expected list
        """
        # Arrange
        expected_participants = sample_activity["initial_participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        actual_participants = activities[sample_activity["name"]]["participants"]
        
        # Assert
        assert actual_participants == expected_participants

    def test_get_activities_returns_correct_max_participants(self, client, sample_activity):
        """
        AAA Test: Verify max_participants value is correct.
        
        Arrange: Sample activity with known max_participants
        Act: Get activities and extract max_participants
        Assert: Verify max_participants matches expected value
        """
        # Arrange
        expected_max = sample_activity["max_participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        actual_max = activities[sample_activity["name"]]["max_participants"]
        
        # Assert
        assert actual_max == expected_max
