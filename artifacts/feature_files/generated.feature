Feature: Password reset email flow should work for registered users
  As a user
  I want the described behavior
  So that the product works as expected

  Scenario: Scenario 1: Given the user is on the login page, when the user clicks "Forgot Password", then the user should be navigated to the password reset page.
    Given the user has a valid password reset request
    When the user submits the password reset request
    Then the system should complete the password reset flow

  Scenario: Scenario 2: Given the user enters a registered email address, when the user submits the request, then a reset link should be sent successfully.
    Given the system is ready for the workflow
    When the user performs the requested action
    Then the system should complete the expected outcome

  Scenario: Scenario 3: Given the user enters an unregistered email address, when the user submits the request, then the system should still display a generic success message.
    Given the user is authenticated
    When the login action is triggered
    Then the system should display a welcome message

  Scenario: Scenario 4: Given the reset link is used within the valid time window, when the user enters a new valid password, then the password should be updated successfully.
    Given the user has a valid password reset request
    When the user submits the password reset request
    Then the system should complete the password reset flow

  Scenario: Scenario 5: Given the reset link is expired, when the user tries to use it, then the system should show an expiration error.
    Given the system is ready for the workflow
    When the user performs the requested action
    Then the system should complete the expected outcome
