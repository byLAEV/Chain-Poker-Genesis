# Node Core CSPRNG Failure Contract

**Status:** Normative contract v1.0

## 1. Operation
randomBytes(length, profile) MUST return exactly the requested number of cryptographically secure random bytes for a valid request.

## 2. Source
The implementation MUST use an operating-system or approved cryptographic-library CSPRNG. Predictable PRNGs, timestamps, counters, process identifiers, or deterministic fallbacks are prohibited as entropy substitutes.

## 3. Failure
If the approved source fails, becomes unavailable, returns invalid output, or cannot satisfy the request, the operation MUST fail closed. It MUST NOT fall back to an unapproved source or return partial bytes.

## 4. Error boundary
Failure MUST be represented as a typed randomness failure. Secret or entropy material MUST NOT appear in errors or logs.

## 5. Testing
Tests MUST cover valid and invalid lengths, provider failure, invalid provider output, fail-closed behavior, and absence of insecure fallback.

**Closure criterion:** contract accepted, failure injection defined, and tests prove no insecure fallback.
