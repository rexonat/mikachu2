#!/usr/bin/env bash
set -e

echo "📦 Installing Python dependencies"
pip install -r requirements.txt

echo "🌐 Installing Playwright browsers"
python -m playwright install chromium
python -m playwright install --with-deps

