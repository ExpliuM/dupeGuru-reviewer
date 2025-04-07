#!/bin/bash

# init dupeGuru-result-reviewer env.
# rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
