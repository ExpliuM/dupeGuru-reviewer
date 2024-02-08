#!/bin/bash

# Creating work dirs
mkdir -p logs

# TODO: To add Windows support
if [[ "$OSTYPE" == *"Ubuntu"* ]]; then
  echo Preparing env for Ubuntu OS

elif [[ "$OSTYPE" == *"darwin"* ]]; then
  echo Preparing env for MacOS
  # TODO: To add validation that we have brew
  # App dependencies
  brew install ffmpeg
  brew install libmagic
  brew install python@3.11
  brew install qt6
  
  # Build tools
  brew install create-dmg

else
  echo "Currently only Ubuntu and OSX"
  exit
fi

# init dupeGuru-result-reviewer env.
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
