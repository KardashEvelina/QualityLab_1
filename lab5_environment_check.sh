#!/bin/bash

echo "=== LAB 5 ENVIRONMENT CHECK ==="

echo
echo "Python:"
python --version

echo
echo "Radon:"
radon --version

echo
echo "Coverage:"
coverage --version

echo
echo "Mutmut:"
mutmut --version

echo
echo "k6:"
k6 version

echo
echo "Pinned Python quality tools:"
cat requirements_lab5.txt

echo
echo "Environment check completed."
