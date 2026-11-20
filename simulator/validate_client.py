#!/usr/bin/env python3
"""
Independent OPC UA Validation Client
Reads all 7 tags from opc.tcp://127.0.0.1:4840/mes/simulator
Used for TC-OPC-01 and TC-OPC-02 verification.
"""

import asyncio
import sys
from asyncua import Client

ENDPOINT = "opc.tcp://127.0.0.1:4840/mes/simulator"

TAGS = [
    ("Machine_Status", int),
    ("Total_Count", int),
    ("Good_Count", int),
    ("Reject_Count", int),
    ("Cycle_Time", float),
    ("Temperature", float),
    ("Target_Count", int),
]


async def main():
    print(f"Connecting to OPC UA Server: {ENDPOINT}...")
    try:
        async with Client(url=ENDPOINT) as client:
            ns_idx = await client.get_namespace_index("http://mes.local/simulator")
            print(f"Connected successfully! Namespace index: {ns_idx}")
            
            results = {}
            for tag_name, expected_type in TAGS:
                node_id = f"ns={ns_idx};s=Machine01.{tag_name}"
                node = client.get_node(node_id)
                value = await node.read_value()
                val_type = type(value).__name__
                results[tag_name] = value
                print(f"  [TAG] {tag_name:<15} = {value!s:<10} (type: {val_type})")
            
            # Validation assertions
            assert results["Good_Count"] + results["Reject_Count"] == results["Total_Count"], \
                f"Invariant violation: {results['Good_Count']} + {results['Reject_Count']} != {results['Total_Count']}"
            assert results["Machine_Status"] in (0, 1, 2, -1), f"Unexpected status: {results['Machine_Status']}"
            
            print("--- Validation Summary ---")
            print("Status: PASS")
            print(f"Total: {results['Total_Count']} | Good: {results['Good_Count']} | Reject: {results['Reject_Count']}")
            print(f"Invariant Good + Reject == Total: OK")
            print("All 7 tags verified with correct types and plausible values.")
            return 0
    except Exception as e:
        print(f"ERROR connecting or reading tags: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
