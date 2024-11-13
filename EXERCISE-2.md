# TEST-STRATEGY

## 1. Test Objective
The objective of this task is to verify the functionality, performance and reliability of the https://petstore.swagger.io/v2 REST API.

## 2. Test Approach and Types of Testing
The testing approach and the types of testing for this API is:
**Functional Testing:**
- To test the basic functionality of this API: POST, GET, PUT and DELETE
- Verify the required fields and data types

**Error Handling:**
- To test error conditions and the HTTP responses.

**Concurrency Testing:**
- To test the API's ability to handle concurrent requests and data creation.

## 3. Testing Tools:
- Pytest: As the test framework to automate testing.

# TEST-PLAN

## Test Cases

Based on the test approach and types of testing, the test cases would be:
1. Pet Functionality Tests:
- The functional, error and concurrency tests and performed against the /pet functionality
- The functionality includes:
  - Creating a new pet
  - Updating a pet
  - Finding pets by status
  - Finding a pet by ID
  - Updating a pet with form data
  - Deleting a pet

2. User Functionality Tests:
- The functional, error and concurrency tests and performed against the /user functionality
- The functionality includes:
  - Creating a new user
    - By itself
    - In a list
    - In an array
  - Getting a user by username
  - Updating a user
  - Deleting a user
  - Logging in a user
  - Logging out a user

3. Store Functionality Tests:
- The functional, error and concurrency tests and performed against the /store functionality
- The functionality includes:
- Placing an order for a pet
- Finding the purchase order by order ID
- Deleting an order
- Getting the pet inventory

## Risks
- Since this is a public API, public data is also available which may affect testing due to data potentially changing during testing while also allowing other users to modify data
- Excessive requests may result in rate limiting from the API, hindering ability to test the API.

# DECISIONS AND REASONS
1. Automated Testing with Pytest
- Decision: Use of automated testing with the Pytest framework.
- Reasons: Allows for automated testing of repetitive actions and concurrent tests as well as being widely supported.

2. Concurrency Testing:
- Decision: To simulate multiple concurrent API requests
- Reason: This allows for load testing to better simulate real world loads in order to ensure the API is able to manage multiple simultaneous requests.

3. Boundary and Edge Case Testing
- Decision: Include boundary and edge case testing for each endpoint
- Reason: In the real world this may not occur as frequent but they help to identify potential issues with the input validation and error handling. Unwanted inputs should be caught to ensure robustness and security.