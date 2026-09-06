"""
Demonstration of genpark-human-in-the-loop-approval-gate-interrupt-skill
"""

from client import HumanApprovalGateInterruptClient

def main():
    gate = HumanApprovalGateInterruptClient()

    # Agent encounters risky action: wire transfer
    action = {
        "action_type": "fund_transfer",
        "amount_usd": 15000.0,
        "recipient": "supplier_logistics_inc"
    }

    ticket = gate.create_interrupt("task_tx_9981", action, required_role="finance_admin", risk_level="CRITICAL")
    print(f"Execution Interrupted! Ticket ID: {ticket['interrupt_id']}")
    print(f"Risk Level: {ticket['risk_level']}")

    # Human reviewer inspects and approves
    decision = gate.approve(
        interrupt_id=ticket["interrupt_id"],
        approval_token=ticket["approval_token"],
        reviewer="finance_director_sarah",
        reviewer_role="finance_admin"
    )

    print("=== HUMAN APPROVAL GRANTED ===")
    print(f"Status: {decision['status']}")
    print(f"Resumed Thread: {decision['resumed_thread_id']}")
    print(f"Action Cleared: {decision['action_payload']['action_type']} of ${decision['action_payload']['amount_usd']}")

if __name__ == "__main__":
    main()
