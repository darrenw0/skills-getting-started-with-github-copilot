"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestRemoveParticipant:
    """Test suite for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_delete_participant_success(self, client, sample_activity):
        """
        AAA Test: Verify successful participant removal returns 200.
        
        Arrange: Valid activity name and existing participant email
        Act: DELETE participant from activity
        Assert: Verify status code is 200
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["initial_participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200

    def test_delete_participant_removes_from_list(self, client, sample_activity):
        """
        AAA Test: Verify participant is actually removed from participant list.
        
        Arrange: Valid activity and participant
        Act: Delete participant, then fetch activities
        Assert: Verify email is no longer in participants list
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["initial_participants"][0]
        
        # Act
        delete_response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        remaining_participants = activities[activity_name]["participants"]
        
        # Assert
        assert email not in remaining_participants

    def test_delete_participant_keeps_other_participants(self, client, sample_activity):
        """
        AAA Test: Verify deleting one participant doesn't affect others.
        
        Arrange: Activity with multiple participants
        Act: Delete one participant
        Assert: Verify other participants remain in list
        """
        # Arrange
        activity_name = sample_activity["name"]
        email_to_delete = sample_activity["initial_participants"][0]
        email_to_keep = sample_activity["initial_participants"][1]
        
        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email_to_delete}"
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        remaining_participants = activities[activity_name]["participants"]
        
        # Assert
        assert email_to_delete not in remaining_participants
        assert email_to_keep in remaining_participants

    def test_delete_nonexistent_activity_returns_404(self, client):
        """
        AAA Test: Verify deletion from non-existent activity returns 404.
        
        Arrange: Invalid activity name and test email
        Act: DELETE from non-existent activity
        Assert: Verify status code is 404
        """
        # Arrange
        invalid_activity = "NonexistentActivity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404

    def test_delete_nonexistent_activity_error_message(self, client):
        """
        AAA Test: Verify error message for non-existent activity.
        
        Arrange: Invalid activity name
        Act: DELETE from non-existent activity
        Assert: Verify error detail mentions activity not found
        """
        # Arrange
        invalid_activity = "NonexistentActivity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/participants/{email}"
        )
        error_detail = response.json().get("detail", "")
        
        # Assert
        assert "not found" in error_detail.lower()

    def test_delete_nonexistent_participant_returns_404(self, client, sample_activity):
        """
        AAA Test: Verify deletion of non-existent participant returns 404.
        
        Arrange: Valid activity but invalid email
        Act: DELETE non-existent participant from activity
        Assert: Verify status code is 404
        """
        # Arrange
        activity_name = sample_activity["name"]
        nonexistent_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{nonexistent_email}"
        )
        
        # Assert
        assert response.status_code == 404

    def test_delete_nonexistent_participant_error_message(self, client, sample_activity):
        """
        AAA Test: Verify error message for non-existent participant.
        
        Arrange: Valid activity but invalid email
        Act: DELETE non-existent participant
        Assert: Verify error detail mentions participant not found
        """
        # Arrange
        activity_name = sample_activity["name"]
        nonexistent_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{nonexistent_email}"
        )
        error_detail = response.json().get("detail", "")
        
        # Assert
        assert "not found" in error_detail.lower()

    def test_delete_already_deleted_participant_returns_404(self, client, sample_activity):
        """
        AAA Test: Verify deleting same participant twice returns 404 second time.
        
        Arrange: Valid activity and participant
        Act: Delete same participant twice
        Assert: First delete succeeds, second returns 404
        """
        # Arrange
        activity_name = sample_activity["name"]
        email = sample_activity["initial_participants"][0]
        
        # Act
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_delete_multiple_participants_sequentially(self, client, sample_activity):
        """
        AAA Test: Verify deleting multiple participants one by one.
        
        Arrange: Activity with multiple participants
        Act: Delete participants sequentially
        Assert: Verify each deletion succeeds and count decreases
        """
        # Arrange
        activity_name = sample_activity["name"]
        initial_count = len(sample_activity["initial_participants"])
        
        # Act - Delete first participant
        email1 = sample_activity["initial_participants"][0]
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email1}"
        )
        activities1 = client.get("/activities").json()
        count_after_first = len(activities1[activity_name]["participants"])
        
        # Act - Delete second participant
        email2 = sample_activity["initial_participants"][1]
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email2}"
        )
        activities2 = client.get("/activities").json()
        count_after_second = len(activities2[activity_name]["participants"])
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert count_after_first == initial_count - 1
        assert count_after_second == initial_count - 2
