#!/usr/bin/env python3
"""
Test script to validate Haru samples against the JSON schema.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = os.path.join(BASE_DIR, "quiz_schema.json")
SAMPLES_FILE = os.path.join(BASE_DIR, "samples_for_haru.json")

def validate_sample(sample, schema):
    # Required top level
    for req in schema["required"]:
        if req not in sample:
            return False, f"Missing required top-level property: {req}"
    
    # Check format_type enum
    if sample["format_type"] not in schema["properties"]["format_type"]["enum"]:
        return False, f"Invalid format_type: {sample['format_type']}"
        
    # Check quiz_web_data
    q_data = sample["quiz_web_data"]
    for req in schema["properties"]["quiz_web_data"]["required"]:
        if req not in q_data:
            return False, f"Missing in quiz_web_data: {req}"
    if not (0 <= q_data["answer_index"] < len(q_data["options"])):
        return False, f"answer_index {q_data['answer_index']} out of options bounds"
        
    # Check shorts_script_data
    s_data = sample["shorts_script_data"]
    for req in schema["properties"]["shorts_script_data"]["required"]:
        if req not in s_data:
            return False, f"Missing in shorts_script_data: {req}"
            
    # Check fact_check
    fc_data = sample["fact_check"]
    for req in schema["properties"]["fact_check"]["required"]:
        if req not in fc_data:
            return False, f"Missing in fact_check: {req}"
    if fc_data["verification_status"] not in ["VERIFIED", "PENDING", "REJECTED"]:
        return False, f"Invalid verification_status: {fc_data['verification_status']}"

    return True, "Valid"

def main():
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    with open(SAMPLES_FILE, "r", encoding="utf-8") as f:
        samples = json.load(f)
        
    print(f"Loaded schema: {schema['title']}")
    print(f"Loaded {len(samples)} samples. Validating each...")
    
    for idx, sample in enumerate(samples):
        valid, msg = validate_sample(sample, schema)
        if not valid:
            print(f"[FAIL] Sample #{idx+1} ({sample.get('id', 'No ID')}): {msg}")
            sys.exit(1)
        else:
            print(f"[PASS] Sample #{idx+1} ({sample['id']}): {sample['topic']} - Format: {sample['format_type']} - Status: {sample['fact_check']['verification_status']}")
            
    print("\n=== All Samples 100% Conforming to quiz_schema.json ===")

if __name__ == "__main__":
    main()
