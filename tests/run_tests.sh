#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "notopened AI ENTERPRISE - Comprehensive Test Suite Runner"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/3] Running Python Unit Tests..."
python3 test_quiz_logic.py

echo "[2/3] Running Haru Content Schema Validation..."
python3 ../../haru_integration/test_schema.py

echo "[3/3] Running Headless Chromium Desktop & Mobile E2E Tests..."
python3 test_browser_flow.py

echo "=========================================================="
echo "[SUCCESS] All unit tests, schema tests, and browser tests PASSED!"
echo "=========================================================="
