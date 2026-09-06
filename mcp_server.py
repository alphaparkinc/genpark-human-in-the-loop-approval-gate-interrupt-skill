"""
MCP Server for genpark-human-in-the-loop-approval-gate-interrupt-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import HumanApprovalGateInterruptClient

gate = HumanApprovalGateInterruptClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "create_interrupt",
                        "description": "Trigger a human-in-the-loop interrupt gate for high-risk agent operations.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "thread_id": {"type": "string"},
                                "action": {"type": "object"},
                                "risk_level": {"type": "string"}
                            },
                            "required": ["thread_id", "action"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "create_interrupt":
            res = gate.create_interrupt(args["thread_id"], args["action"], risk_level=args.get("risk_level", "HIGH"))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res)}]
                }
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
