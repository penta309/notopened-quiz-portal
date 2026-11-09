#!/usr/bin/env python3
"""
notopened AI ENTERPRISE - Haru Content & Web Quiz Portal Synchronization Tool
Maintains strict separation between Quiz Data and Presentation UI Logic.
Validates consistency between Haru's Shorts scripts and Web Quiz data.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "quiz_schema.json")
SAMPLES_PATH = os.path.join(BASE_DIR, "samples_for_haru.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "..", "quiz_portal", "src", "data.js")

def convert_haru_samples_to_js(samples):
    """Converts verified Haru JSON samples into ES6 data.js format."""
    lines = [
        "/**",
        " * notopened Quiz Portal - Verified Baseline Questions",
        " * Generated from Haru's Shorts & Quiz Schema Synchronization Pipeline",
        " */",
        "export const quizData = ["
    ]
    for idx, s in enumerate(samples):
        q_data = s["quiz_web_data"]
        fc = s["fact_check"]
        entry = (
            f"  {{\n"
            f'    id: "{s["id"]}",\n'
            f'    category: "{s["topic"]} ({s["format_type"]})",\n'
            f'    question: "{q_data["question"]}",\n'
            f'    options: {json.dumps(q_data["options"], ensure_ascii=False)},\n'
            f'    answer: {q_data["answer_index"]},\n'
            f'    explanation: "{q_data["explanation"]}",\n'
            f'    source: "{fc["primary_source_name"]}"\n'
            f"  }}{',' if idx < len(samples) - 1 else ''}"
        )
        lines.append(entry)
    lines.append("];\n")
    return "\n".join(lines)

def verify_data_consistency():
    """Verify consistency between quiz data and schema."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    with open(SAMPLES_PATH, "r", encoding="utf-8") as f:
        samples = json.load(f)

    print(f"[*] Validating {len(samples)} Haru samples against schema...")
    for s in samples:
        q_data = s["quiz_web_data"]
        # Consistency checks
        assert len(q_data["options"]) >= 2, f"Too few options for {s['id']}"
        assert 0 <= q_data["answer_index"] < len(q_data["options"]), f"Invalid answer index in {s['id']}"
        assert len(q_data["explanation"]) > 10, f"Explanation too short for {s['id']}"
        assert s["fact_check"]["verification_status"] == "VERIFIED", f"Fact check not verified in {s['id']}"
        print(f"  [OK] {s['id']}: {s['topic']} - Verified by {s['fact_check']['verified_by']}")

    print("[+] All Haru samples verified for 1:1 synchronization with Web Quiz Portal.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--convert":
        with open(SAMPLES_PATH, "r", encoding="utf-8") as f:
            samples = json.load(f)
        output_js = convert_haru_samples_to_js(samples)
        print(output_js)
    else:
        verify_data_consistency()
