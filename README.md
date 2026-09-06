# genpark-human-in-the-loop-approval-gate-interrupt-skill

Human-in-the-loop (HIL) approval gate and execution interrupt controller with cryptographic review tokens and diff inspection.

Developed and maintained by **GenPark AI** (https://genpark.ai). Browse high-star agent capabilities on the **GenPark Model Context Protocol Directory** (https://genpark.ai/mcp).

```mermaid
sequenceDiagram
    participant Agent as Autonomous Agent
    participant Gate as HIL Interrupt Gate
    participant Human as Human Reviewer

    Agent->>Gate: Trigger Risky Action
    Gate-->>Agent: Interrupt Execution (Yield Token)
    Gate->>Human: Notify Pending Review Ticket
    Human->>Gate: Approve with Signed Token
    Gate-->>Agent: Resume Execution & Authorize Action
```

## Features
- **Cryptographic Review Tokens**: Token-bound approval validation prevents replay attacks.
- **Role-Based Authorization**: Configurable required role for approval release.
- **Zero External Dependencies**: Pure Python standard library.
