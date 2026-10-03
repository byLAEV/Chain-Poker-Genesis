# Node Core Identity — Design Consolidation Draft

**Project:** Chain Poker Genesis by LAEV  
**Component:** Node Core / Identity  
**Document status:** Design draft — non-normative  
**Version:** 0.1  
**Purpose:** Consolidation of the identity concepts currently defined by LAEV during the design phase.

> This document records the current design conversation. It is not yet an implementation specification and MUST NOT be interpreted as authorization to implement the mechanisms described here.

## 1. Purpose

The Identity system of Node Core is intended to establish a verifiable relationship between:

- the life of a Node created by the installer;
- the cryptographic identity that approaches that Node;
- the evidence requested by the protocol;
- the verification results produced from that evidence;
- the reputation information relevant to consensus;
- and the minimal references that can be propagated through the network.

The design follows the principle:

**No confiamos; verificamos.**

When something cannot yet be verified, the system does not automatically treat it as trusted. Instead, the unresolved state becomes part of the process by which verifiable reputation can be established.

## 2. Design status

The concepts in this document are being defined before implementation.

The intended order is:

1. LAEV design concept
2. Design documentation
3. Formal specification
4. Review and correction
5. Architecture
6. Implementation plan
7. Implementation
8. Test vectors
9. Reference implementation
10. Audit

Therefore, names, directory structures, schemas, algorithms, lifecycle states, and interfaces mentioned here remain subject to formal review unless explicitly marked as already established elsewhere.

## 3. Core principles

### 3.1 Verification before trust

Node Core does not need to trust an identity merely because it presents a claim.

The system should determine what can be cryptographically verified, what can be proven through protocol-controlled requests, and what remains unverified.

### 3.2 Minimum necessary disclosure

The identity process should expose only the information required by the current protocol request.

Zero-knowledge techniques may be used to prove a required property without unnecessarily revealing the underlying information.

### 3.3 Cryptographic approach

The mechanism by which an external identity approaches Node Core is based on cryptographic control and signatures.

The current concept contemplates:

- PGP;
- GPG;
- cryptographic signatures;
- hardware USB wallet signatures.

Private keys belonging to an external credential or hardware wallet remain external to Node Core. Node Core verifies signatures or cryptographic results rather than requiring custody of those private keys.

### 3.4 Identity is not reputation

Identity establishes a cryptographically verifiable subject and its relationship with a Node.

Reputation is separate.

Reputation represents verifiable information about prior participation, behavior, completed verification, and other evidence that consensus may use when determining participation conditions, preferences, and proof-of-function requirements.

Reputation is not a generic trust score and does not replace verification.

## 4. Node life

A Node is understood as a concrete life created by installation.

The installer gives life to the Node.

The design goal is deterministic lifecycle observability: it should be possible to establish, from verifiable events and records:

- how many Node lives have been created;
- when each life was created;
- which life is active;
- when a life was lost, terminated, or otherwise ended;
- when such an event occurred;
- and the relevant lifecycle metrics.

This use of “deterministic” refers primarily to the ability to establish and reproduce the Node lifecycle state from verifiable events. It does not yet define a specific cryptographic derivation algorithm.

## 5. Installer and Node identity

A default installer may provide the mechanism that generates the Node identity when a Node life is created.

The current concept is:

~~~
DEFAULT INSTALLER
      ↓
NODE LIFE CREATION
      ↓
NODE IDENTITY / NODE ID
      ↓
NODE ACTIVE
~~~

The exact Node ID generation mechanism remains an open design decision.

The relationship between installer provenance and Node identity must not be assumed to mean that the installer owns the external identity that later approaches the Node.

## 6. External identity approach

After a Node life exists, an external identity can approach the Node.

The current conceptual path is:

~~~
IDENTITY APPROACH
(PGP / GPG / cryptographic signature / hardware wallet)
      ↓
CRYPTOGRAPHIC VERIFICATION
      ↓
IDENTITY BINDING
~~~

The approach mechanism establishes cryptographic control or authorship of the presented credential.

This mechanism is distinct from zero-knowledge verification.

## 7. Identity binding

The design includes a binding between the Node life and the external identity that approaches it.

The resulting relationship may be represented as a united identity representation.

Conceptually:

~~~
NODE LIFE / NODE ID
        +
EXTERNAL CRYPTOGRAPHIC IDENTITY
        ↓
IDENTITY BINDING
        ↓
UNITED IDENTITY REPRESENTATION
~~~

Binding does not destroy, replace, or merge the original identities into an indistinguishable object.

The purpose is to establish a verifiable relationship between them.

The exact binding record, identifiers, signatures, timestamps, manifests, hashes, and authorization rules remain to be formally specified.

## 8. Protocol request sequence

Identity information is not intended to be exposed indiscriminately.

The protocol should request the information, property, proof, or evidence that is required at a particular stage.

The conceptual sequence is:

~~~
UNITED IDENTITY
      ↓
PROTOCOL REQUEST
      ↓
REQUIRED EVIDENCE / PROPERTY
      ↓
PROOF OR SELECTIVE DISCLOSURE
      ↓
VERIFICATION
~~~

The sequence of requests should itself be controlled by protocol rules.

The exact request format, issuer, ordering, authorization, chaining, expiration, and verification semantics remain open.

## 9. Zero-knowledge verification

Zero-knowledge mechanisms are intended to minimize disclosure.

The system may receive a proof that a requested property is true without receiving the complete underlying information.

This is complementary to cryptographic identity approach:

- signatures establish control or authorship of a credential;
- zero-knowledge proofs establish requested properties with minimized disclosure.

Neither mechanism should automatically be treated as a substitute for the other.

## 10. Verification states

The design requires a distinction between:

- information presented;
- information processed;
- information cryptographically verified;
- information insufficient for verification;
- and information rejected under protocol rules.

An unresolved or insufficient verification result should not be silently converted into trust.

It may instead become part of the evidence history from which reputation can later be established.

Exact state names and transitions remain subject to formal specification.

## 11. Reputation

Reputation is a verification-support mechanism used by consensus.

It may provide verifiable information that helps consensus determine:

- which participation conditions apply;
- which preferences may be configured;
- which proof-of-function tests are required;
- what prior verified behavior is relevant;
- and what additional verification may be necessary.

Reputation must remain evidence-based and auditable.

**Reputation does not replace proof.**

A positive reputation state cannot, by itself, establish that a required proof-of-function test was successfully performed.

## 12. Consensus interaction

The conceptual relationship is:

~~~
VERIFIED IDENTITY / EVIDENCE
            +
       REPUTATION
            ↓
        CONSENSUS
       ↙         ↘
PREFERENCES   PROOF-OF-FUNCTION
CONDITIONS       REQUIREMENTS
~~~

Consensus determines protocol conditions according to its own rules.

The exact consensus interfaces and decision rules remain to be specified.

## 13. Proof of function

Proof-of-function tests demonstrate that a required function was actually performed according to the applicable rules.

Identity and reputation can determine which tests or conditions are required, but neither identity nor reputation is itself proof that the function was executed.

The relationship between reputation and proof-of-function selection requires a formal specification.

## 14. Propagation

Identity-related information should propagate through verifiable references rather than indiscriminately distributing private identity material.

Potential propagated references include:

- Node ID;
- installer identifier or provenance reference, where applicable;
- united identity reference;
- binding reference;
- manifest hashes;
- verification state;
- consensus-relevant state;
- CIDs;
- references to encrypted objects.

The exact propagation set is not yet normative.

## 15. Storage and CID references

Identity-related material may be represented through encrypted objects and content-addressed references.

The current design includes:

- local Node storage;
- Kubo/IPFS;
- local Gateway access;
- external or cloud backups where authorized;
- encrypted stored objects;
- CID-based references.

A CID may propagate without revealing the plaintext represented by the object.

Storage and propagation must therefore remain separate concerns:

~~~
IDENTITY DATA
      ↓
ENCRYPTED OBJECT
      ↓
CID / CONTENT REFERENCE
      ↓
PROPAGATION
~~~

The exact encryption, key-management, authorization, retention, and recovery profiles remain open.

## 16. Recovery and continuity

Recovery must distinguish between:

1. recovering the same Node life; and
2. creating a new Node life after the previous life has ended.

This distinction is required to preserve meaningful lifecycle metrics.

A recovery mechanism must therefore establish whether continuity of the original Node life has been cryptographically and procedurally demonstrated.

The rules for determining continuity versus new life remain open.

## 17. Conceptual lifecycle

The current consolidated concept can be represented as:

~~~
DEFAULT INSTALLER
      ↓
NODE LIFE CREATION
      ↓
NODE IDENTITY / NODE ID
      ↓
NODE ACTIVE
      ↓
IDENTITY APPROACH
(PGP / GPG / signature / hardware wallet)
      ↓
CRYPTOGRAPHIC VERIFICATION
      ↓
IDENTITY BINDING
      ↓
UNITED IDENTITY REPRESENTATION
      ↓
PROTOCOL REQUEST SEQUENCE
      ↓
ZK PROOFS / SELECTIVE DISCLOSURE
      ↓
VERIFICATION
      ├── VERIFIED
      └── INSUFFICIENT / UNVERIFIED
                  ↓
          REPUTATION BUILDING
                  ↓
              CONSENSUS
              ↙       ↘
      PREFERENCES   PROOF-OF-FUNCTION
                         ↓
                 VERIFIED RESULTS
                         ↓
                    REPUTATION
                         ↓
                    PROPAGATION
~~~

This diagram is conceptual and is not a final state machine.

## 18. Relationship with the existing formal identity profile

The repository already contains a formal Node Core identity profile.

This draft does not silently replace that profile.

Instead, it records the broader identity design currently being developed by LAEV, including concepts that still require reconciliation with the existing formal profile.

In particular, the following require explicit future review:

- Node life versus identity lifecycle;
- installer-generated Node identity;
- external identity approach;
- identity binding / united identity representation;
- PGP/GPG and hardware-wallet signature roles;
- protocol-controlled request sequences;
- zero-knowledge verification;
- reputation as consensus-relevant evidence;
- lifecycle loss and recovery semantics.

Until that review occurs, this document is a design draft rather than a normative replacement.

## 19. Open design decisions

The following questions remain intentionally open:

1. What exactly generates the Node ID?
2. Is the Node ID derived from a generated keypair, another deterministic source, or a separate mechanism?
3. Is installer identity mandatory, optional, or only provenance?
4. What exact event creates a Node life?
5. What exact event terminates or loses a Node life?
6. Can a terminated life be recovered?
7. What evidence proves continuity of the same life after recovery?
8. What exact relation binds external identity to Node identity?
9. Which PGP/GPG mechanisms are required?
10. What exact hardware-wallet signature interface is required?
11. What exact protocol component issues identity requests?
12. How are request sequences authorized and chained?
13. Which properties can be proven using zero-knowledge mechanisms?
14. What is the canonical identity representation?
15. What exact information constitutes reputation?
16. How is reputation independently verified?
17. How does consensus consume reputation?
18. How are proof-of-function requirements selected?
19. What identity references are propagated?
20. Which identity objects are stored locally, through Kubo/IPFS, or externally?
21. How are encryption keys managed without moving private keys into Node Core?
22. What exact conditions distinguish recovery from creation of a new Node life?

## 20. Implementation boundary

No implementation should be derived directly from this document until the unresolved design decisions have been reviewed and the design has been converted into a formal specification.

The intended next phase is:

~~~
DESIGN DRAFT
      ↓
FORMAL SPECIFICATION
      ↓
REVIEW / CORRECTION
      ↓
ARCHITECTURE
      ↓
IMPLEMENTATION PLAN
      ↓
TEST VECTORS
      ↓
REFERENCE IMPLEMENTATION
      ↓
AUDIT
~~~

## 21. Authorship and provenance

This document consolidates the Identity concepts explained by LAEV during the design process of Chain Poker Genesis by LAEV.

Where this document uses organizational language, state names, diagrams, or categories not explicitly fixed by LAEV, those elements are presented as documentation structure or working formulation and remain subject to review.

**Status:** Design consolidation draft.  
**Not normative. Not an implementation specification.**
