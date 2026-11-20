#!/usr/bin/env python3
"""
Test Counter Invariant: Total = Good + Reject (TC-CNT-01)
Polls the OPC UA server continuously across multiple cycles.
"""

import asyncio
import sys
from asyncua import Client

ENDPOINT = "opc.tcp://127.0.0.1:4840/mes/simulator"

async def test_invariant(num_samples=30, interval_sec=0.5):
    print(f"Connecting to {ENDPOINT} to verify counter invariant over {num_samples} samples...")
    async with Client(url=ENDPOINT) as client:
        ns = await client.get_namespace_index("http://mes.local/simulator")
        node_total = client.get_node(f"ns={ns};s=Machine01.Total_Count")
        node_good = client.get_node(f"ns={ns};s=Machine01.Good_Count")
        node_reject = client.get_node(f"ns={ns};s=Machine01.Reject_Count")
        node_status = client.get_node(f"ns={ns};s=Machine01.Machine_Status")
        
        violations = 0
        samples = []
        for i in range(num_samples):
            total = await node_total.read_value()
            good = await node_good.read_value()
            reject = await node_reject.read_value()
            status = await node_status.read_value()
            
            is_valid = (good + reject == total)
            if not is_valid:
                violations += 1
                print(f"  [VIOLATION] Sample {i+1}: Total={total}, Good={good}, Reject={reject}")
            else:
                samples.append((total, good, reject, status))
            
            await asyncio.sleep(interval_sec)
        
        print("\n=== TC-CNT-01 Counter Invariant Test Results ===")
        print(f"Samples evaluated: {num_samples}")
        print(f"Violations detected: {violations}")
        print(f"First reading: Total={samples[0][0]}, Good={samples[0][1]}, Reject={samples[0][2]}")
        print(f"Latest reading: Total={samples[-1][0]}, Good={samples[-1][1]}, Reject={samples[-1][2]}")
        print(f"Delta units produced during test: {samples[-1][0] - samples[0][0]}")
        
        if violations == 0:
            print("Test Result: PASS (Zero invariant violations across all samples)")
            return 0
        else:
            print(f"Test Result: FAIL ({violations} violations)")
            return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(test_invariant()))
