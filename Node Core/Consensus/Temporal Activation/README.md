# Temporal Activation

Defines lifecycle transitions governed by deterministic temporal boundaries.

Activation mechanisms:

- Activation Height.
- Activation Timestamp.

Lifecycle:

~~~text
ANNOUNCED
   ↓
PREPARATION
   ↓
SCHEDULED
   ↓
ACTIVATED
   ↓
ENFORCED
   ↓
RETIRED
~~~

The local clock is not automatically an authority of consensus.
