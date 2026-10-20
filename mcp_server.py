"""MCP Server for Entropy Hallucination Detector.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import EntropyHallucinationDetector

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "audit_text",
                                "description": "Audit text for vocabulary collapse and degenerative hallucination loops",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string", "description": "LLM output text"},
                                        "min_entropy": {"type": "number", "default": 2.5},
                                        "max_repeat_ratio": {"type": "number", "default": 0.35}
                                    },
                                    "required": ["text"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                res = EntropyHallucinationDetector.audit_text(
                    text=args.get("text", ""),
                    min_entropy=args.get("min_entropy", 2.5),
                    max_repeat_ratio=args.get("max_repeat_ratio", 0.35)
                )
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
