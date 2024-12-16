Feature: Generate Use Case Diagram

  Scenario: User generates a use case diagram successfully
    Given the user navigates to the "Generate Use Case Diagram" page
    And the user enters a valid actor name "Admin"
    And the user enters a valid feature name "Manage Users"
    And the user clicks the "Generate" button
    Then the user should see a success message "Use case diagram generated successfully!"
    And the user should be navigated to the "Output Use Case Diagram" page

  Scenario: User tries to generate a use case diagram without entering an actor
    Given the user navigates to the "Generate Use Case Diagram" page
    And the user leaves the actor name field empty
    And the user enters a valid feature name "Manage Users"
    And the user clicks the "Generate" button
    Then the user should see an error message "Actor name is required."

  Scenario: User tries to generate a use case diagram without entering a feature
    Given the user navigates to the "Generate Use Case Diagram" page
    And the user enters a valid actor name "Admin"
    And the user leaves the feature name field empty
    And the user clicks the "Generate" button
    Then the user should see an error message "Feature name is required."
