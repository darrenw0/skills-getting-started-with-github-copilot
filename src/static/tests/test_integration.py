"""Integration tests for FastAPI Activities API using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestActivityWorkflows:
    """Integration test suite for multi-step activity workflows."""

    def test_complete_signup_and_removal_workflow(self, client, sample_activity, test_email):
        """
        AAA Test: Verify complete workflow of signup, verify, and removal.
        
        Arrange: Activity and test email
        Act: 1) Signup 2) Verify participant added 3) Remove 4) Verify removed
        Assert: All operations succeed and state changes are correct
        """
        # Arrange
        activity_name = sample_activity["name"]
        
        # Act - Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        activities_after_signup = client.get("/activities").json()
        participants_after_signup = activities_after_signup[activity_name]["participants"]
        
        # Assert signup
        assert signup_response.status_code == 200
        assert test_email in participants_after_signup
        
        # Act - Remove
        delete_response = client.delete(
            f"/activities/{activity_name}/participants/{test_email}"
        )
        activities_after_delete = client.get("/activities").json()
        participants_after_delete = activities_after_delete[activity_name]["participants"]
        
        # Assert removal
        assert delete_response.status_code == 200
        assert test_email not in participants_after_delete

    def test_signup_multiple_activities_then_remove_one(self, client, test_email):
        """
        AAA Test: Signup for multiple activities, then remove from one.
        
        Arrange: Two activities and one email
        Act: 1) Signup both 2) Remove from first 3) Verify state
        Assert: Removed from first, still in second
        """
        # Arrange
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act - Signup for both
        client.post(f"/activities/{activity1}/signup", params={"email": test_email})
        client.post(f"/activities/{activity2}/signup", params={"email": test_email})
        
        # Act - Remove from first activity
        delete_response = client.delete(
            f"/activities/{activity1}/participants/{test_email}"
        )
        
        # Assert
        activities = client.get("/activities").json()
        assert test_email not in activities[activity1]["participants"]
        assert test_email in activities[activity2]["participants"]
        assert delete_response.status_code == 200

    def test_signup_remove_signup_again(self, client, sample_activity, test_email):
        """
        AAA Test: Signup, remove, then signup again for same activity.
        
        Arrange: Activity and test email
        Act: 1) Signup 2) Remove 3) Signup again
        Assert: All operations succeed and participant is back
        """
        # Arrange
        activity_name = sample_activity["name"]
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Act - Remove
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{test_email}"
        )
        
        # Act - Signup again
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        
        activities = client.get("/activities").json()
        assert test_email in activities[activity_name]["participants"]

    def test_two_students_signup_and_removal(self, client, sample_activity):
        """
        AAA Test: Two students signup, remove first, verify second remains.
        
        Arrange: Activity and two emails
        Act: 1) Both signup 2) Remove first 3) Verify state
        Assert: First removed, second remains with original participants
        """
        # Arrange
        activity_name = sample_activity["name"]
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        original_count = len(sample_activity["initial_participants"])
        
        # Act - Both signup
        client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        client.post(f"/activities/{activity_name}/signup", params={"email": email2})
        
        # Act - Remove first student
        client.delete(f"/activities/{activity_name}/participants/{email1}")
        
        # Assert
        activities = client.get("/activities").json()
        participants = activities[activity_name]["participants"]
        
        assert email1 not in participants
        assert email2 in participants
        assert len(participants) == original_count + 1  # original + email2

    def test_activities_list_reflects_signup_changes(self, client, sample_activity, test_email):
        """
        AAA Test: Verify activities endpoint reflects signup changes immediately.
        
        Arrange: Activity and test email
        Act: Signup and immediately fetch activities
        Assert: Activities list shows updated participant count
        """
        # Arrange
        activity_name = sample_activity["name"]
        initial_participants = sample_activity["initial_participants"].copy()
        
        # Act - Signup
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
        
        # Assert
        activities = client.get("/activities").json()
        current_participants = activities[activity_name]["participants"]
        
        assert len(current_participants) == len(initial_participants) + 1
        assert test_email in current_participants
        # Verify original participants still there
        for email in initial_participants:
            assert email in current_participants

    def test_activities_list_reflects_removal_changes(self, client, sample_activity):
        """
        AAA Test: Verify activities endpoint reflects removal changes immediately.
        
        Arrange: Activity with existing participant
        Act: Remove participant and immediately fetch activities
        Assert: Activities list shows updated participant count
        """
        # Arrange
        activity_name = sample_activity["name"]
        email_to_remove = sample_activity["initial_participants"][0]
        initial_count = len(sample_activity["initial_participants"])
        
        # Act - Remove participant
        client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
        
        # Assert
        activities = client.get("/activities").json()
        current_participants = activities[activity_name]["participants"]
        
        assert len(current_participants) == initial_count - 1
        assert email_to_remove not in current_participants

    def test_get_activities_shows_unchanged_activities(self, client, sample_activity, test_email):
        """
        AAA Test: Verify other activities remain unchanged during signup operations.
        
        Arrange: Multiple activities
        Act: Signup to one activity
        Assert: Other activities' participant lists unchanged
        """
        # Arrange
        activity_to_change = sample_activity["name"]
        activity_to_check = "Programming Class"
        
        # Get original state
        original_activities = client.get("/activities").json()
        original_participants = original_activities[activity_to_check]["participants"].copy()
        
        # Act - Signup to different activity
        client.post(
            f"/activities/{activity_to_change}/signup",
            params={"email": test_email}
        )
        
        # Assert
        updated_activities = client.get("/activities").json()
        updated_participants = updated_activities[activity_to_check]["participants"]
        
        assert updated_participants == original_participants
