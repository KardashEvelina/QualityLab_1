#!/bin/bash
set -e

echo "Checking Python syntax..."
python -m compileall -q main.py task_service.py user_service.py report_service.py

echo "Running SonarQube analysis..."
sonar-scanner \
  -Dsonar.token="$SONAR_TOKEN" \
  -Dsonar.qualitygate.wait=true