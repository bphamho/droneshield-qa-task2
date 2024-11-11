### BUG 1: Locked Out User
**Priority:** High

**Severirty:** Major

- **Environment:** Mac OS Sonoma
- **Browser:** Chrome
- **Application Version:** 130.0.6723.117

**Steps to Reproduce:**
1. Create a pet with name None

**Expected Result:**
The pet should not be created

**Actual Result:**
The pet was succesfully created. Create a pet will NULL/None data could cause potential issues.