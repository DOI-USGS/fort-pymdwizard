#!/bin/bash
echo "=== REMAINING RUFF ISSUES ==="
echo ""
echo "Running ruff check..."
ruff check . --output-format=concise 2>/dev/null | head -100
