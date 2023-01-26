#!/bin/bash
for x in {1..10}; do (python3 ./GameManager_3.py 2048 >> ./output.txt ) & done
