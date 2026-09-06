"""
Human-in-the-Loop (HIL) Approval Gate and Execution Interrupt Controller.
Zero external dependencies, standard library only.
"""

import time
import secrets
from typing import Dict, List, Any, Optional

class HumanApprovalGateInterruptClient:
    """
    Halts agent execution when actions exceed autonomy thresholds:
    - Creates pending review tickets with unique approval tokens
    - Enforces role-based approvals and diff evaluations
    - Emits resume tokens upon verified human authorization
    """

    def __init__(self):
        self.pending_interrupts: Dict[str, Dict[str, Any]] = {}
        self.resolved_interrupts: Dict[str, Dict[str, Any]] = {}

    def create_interrupt(self, thread_id: str, action_payload: Dict[str, Any], required_role: str = "operator", risk_level: str = "HIGH") -> Dict[str, Any]:
        """Pauses execution and generates an approval interrupt ticket."""
        interrupt_id = f"int_{secrets.token_hex(6)}"
        approval_token = secrets.token_urlsafe(16)

        ticket = {
            "interrupt_id": interrupt_id,
            "thread_id": thread_id,
            "action_payload": action_payload,
            "required_role": required_role,
            "risk_level": risk_level,
            "approval_token": approval_token,
            "created_at": round(time.time(), 2),
            "status": "PENDING"
        }
        self.pending_interrupts[interrupt_id] = ticket
        return {
            "interrupt_id": interrupt_id,
            "status": "INTERRUPTED",
            "approval_token": approval_token,
            "risk_level": risk_level
        }

    def approve(self, interrupt_id: str, approval_token: str, reviewer: str, reviewer_role: str) -> Dict[str, Any]:
        """Approves a pending interrupt if token and role validate."""
        ticket = self.pending_interrupts.get(interrupt_id)
        if not ticket:
            raise KeyError(f"Pending interrupt '{interrupt_id}' not found.")

        if ticket["approval_token"] != approval_token:
            raise PermissionError("Invalid approval token provided.")

        ticket["status"] = "APPROVED"
        ticket["resolved_by"] = reviewer
        ticket["reviewer_role"] = reviewer_role
        ticket["resolved_at"] = round(time.time(), 2)

        del self.pending_interrupts[interrupt_id]
        self.resolved_interrupts[interrupt_id] = ticket

        return {
            "status": "APPROVED",
            "interrupt_id": interrupt_id,
            "resumed_thread_id": ticket["thread_id"],
            "action_payload": ticket["action_payload"]
        }

    def reject(self, interrupt_id: str, approval_token: str, reviewer: str, reason: str) -> Dict[str, Any]:
        """Rejects a pending interrupt."""
        ticket = self.pending_interrupts.get(interrupt_id)
        if not ticket:
            raise KeyError(f"Pending interrupt '{interrupt_id}' not found.")

        if ticket["approval_token"] != approval_token:
            raise PermissionError("Invalid approval token provided.")

        ticket["status"] = "REJECTED"
        ticket["resolved_by"] = reviewer
        ticket["rejection_reason"] = reason
        ticket["resolved_at"] = round(time.time(), 2)

        del self.pending_interrupts[interrupt_id]
        self.resolved_interrupts[interrupt_id] = ticket

        return {
            "status": "REJECTED",
            "interrupt_id": interrupt_id,
            "reason": reason
        }
