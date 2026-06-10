"""Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestSignupForActivity:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_activity, test_email):
        """
        AAA Test: Verify successful signup adds participant to activity.
        
        Arrange: Valid activity name and test email
        Act: POST to signup endpoint
        Assert: Verify status code is 200 and response contains success message
        """
        # Arrange
        activity_name = sample_activity["name"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()

    def test_signup_adds_participant_to_list(self, client, sample_activity, test_email):
        """
        AAA Test: Verify participant is actually added to activity's participant list.
        
        Arrange: Valid activity and test email
        Act: Signup, then fetch activities
        Assert: Verify test_email is in participants list
        """
        # Arrange
        activity_name = sample_activity["name"]
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity_name]["participants"]
        
        # Assert
        assert test_email in participants

    def test_signup_returns_confirmation_message(self, client, sample_activity, test_email):
        """
        AAA Test: Verify signup returns appropriate confirmation message.
        
        Arrange: Valid activity and email
        Act: POST to signup endpoint
        Assert: Verify response message contains activity name and email
        """
        # Arrange
        activity_name = sample_activity["name"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        message = response.json().get("message", "")
        
        # Assert
        assert test_email in message
        assert activity_name in message

    def test_signup_invalid_activity_returns_404(self, client, test_email):
        """
        AAA Test: Verify signup to non-existent activity returns 404.
        
        Arrange: Invalid activity name and test email
        Act: POST to signup endpoint with invalid activity
        Assert: Verify status code is 404
        """
        # Arrange
        invalid_activity = "NonexistentActivity"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": test_email}
        )
        
        # Assert
        assert response.status_code == 404

    def test_signup_invalid_activity_error_message(self, client, test_email):
        """
        AAA Test: Verify error message for non-existent activity.
        
        Arrange: Invalid activity name
        Act: POST to signup endpoint
        Assert: Verify error detail contains appropriate message
        """
        # Arrange
        invalid_activity = "NonexistentActivity"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": test_email}
        )
        error_detail = response.json().get("detail", "")
        
        # Assert
        assert "not found" in error_detail.lower()

    def test_signup_duplicate_signup_returns_400(self, client, sample_activity):
        """
        AAA Test: Verify duplicate signup attempt returns 400.
        
        Arrange: Use an existing participant in the sample activity
        Act: Try to sign up with an already-enrolled email
        Assert: Verify status code is 400
        """
        # Arrange
        activity_name = sample_activity["name"]
        existing_email = sample_activity["initial_participants"][0]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400

    def test_signup_duplicate_signup_error_message(self, client, sample_activity):
        """
        AAA Test: Verify error message for duplicate signup.
        
        Arrange: Use an existing participant
        Act: Try duplicate signup
        Assert: Verify error detail contains appropriate message
        """
        # Arrange
        activity_name = sample_activity["name"]
        existing_email = sample_activity["initial_participants"][0]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        error_detail = response.json().get("detail", "")
        
        # Assert
        assert "already" in error_detail.lower() or "signed up" in error_detail.lower()

    def test_signup_multiple_students_same_activity(self, client, sample_activity):
        """
        AAA Test: Verify multiple students can sign up for same activity.
        
        Arrange: Two different test emails
        Act: Sign up both emails to same activity
        Assert: Verify both are in participants list
        """
        # Arrange
        activity_name = sample_activity["name"]
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in participants
        assert email2 in participants

    def test_signup_same_student_different_activities(self, client, test_email):
        """
        AAA Test: Verify same student can sign up for multiple activities.
        
        Arrange: One test email, two different activities
        Act: Sign up same email to both activities
        Assert: Verify email appears in both activities' participant lists
        """
        # Arrange
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": test_email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": test_email}
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert test_email in activities[activity1]["participants"]
        assert test_email in activities[activity2]["participants"]
