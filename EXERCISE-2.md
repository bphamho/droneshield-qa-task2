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
1. Functional Tests:
- Verify creating a pet, getting pet details, updating a pet and deleting a pet.
- Creating a pet with special characters in their name

2. Error Handling Tests:
- Verify if the API accepts an invalid name or id
- Verify different id's
  - large
  - negative
  - non existent pet id
- Verify incorrect HTTP method

3. Concurrency Tests:
- Verify concurrent pet creation
- Verify a high volume of requests

## Risks
- Testing is currently only performed on a desktop environment so no mobile testing is performed.

# DECISIONS AND REASONS
1. Automated Testing
- Decision: Use of automated testing with the Selenium Framework with Python and pytest
- Reasons: Allows for testing of repetitive actions and coverage of the multiple users provided

2. Repeating each test case for all users
- Decision: Run each test case for each individual user provided on the web application
- Reason: Each user (apart from standard_user) has bugs related to them so testing all test cases for each one will allow for bug discovery.

3. Manual Testing
- Decision: Use of manual testing
- Reason: To explore functionality that may not be noticed just through automation