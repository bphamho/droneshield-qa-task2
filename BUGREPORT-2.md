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
The pet was succesfully created. Create a pet with name or id with NULL/None data could cause potential issues.