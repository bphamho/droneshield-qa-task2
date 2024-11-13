### BUG 1: Pet can be created with an empty id or empty name
**Priority:** High

**Severirty:** Major

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Create a pet with name None
2. Create a pet with id None

**Expected Result:**
The pet should not be created

**Actual Result:**
The pet was succesfully created. Creating a pet with name or id with NULL/None data could cause potential issues.

### BUG 2: User can be created with empty username
**Priority:** High

**Severirty:** Major

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Create a user with username None

**Expected Result:**
The user should not be created due to the potential errors.

**Actual Result:**
The user was succesfully created. 

### BUG 3: User can be created with a very long username
**Priority:** High

**Severirty:** Major

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Create a user with a very long username

**Expected Result:**
The user should either be:
a. not be created
b. be created with the correct username

**Actual Result:**
The user was succesfully created but when retreiving the username data an exception was raised due to the limits of JSON.

### BUG 4: Order with no quantity field can be made
**Priority:** High

**Severirty:** Minor

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Place an order with no quantity

**Expected Result:**
The order should not be created.

**Actual Result:**
The order was succesfully placed. This can lead to errors in the future.

### BUG 5: Order with a large quantity
**Priority:** Medium

**Severirty:** Low

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Place an order with a large quantity (e.g. 1,000,000)

**Expected Result:**
The order should not be created.

**Actual Result:**
The order was succesfully placed. Limits should be placed on the order quantity to prevent unrealistic orders being placed or orders greater than the inventory.

### BUG 6: Multiple orders of the same id can be placed concurrently
**Priority:** Minor

**Severirty:** Low

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Use a test script to place orders concurrently

**Expected Result:**
Only 1 order should be accepted or all orders should be rejected.

**Actual Result:**
All orders were placed succesfully. If orders were to somehow have identica ids this would cause an issue where the orders are placed but they all have different details (e.g. different quantities)