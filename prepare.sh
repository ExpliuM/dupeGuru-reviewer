#!/bin/bash

# TODO: To add Windows support
if [[ "$OSTYPE" == *"Ubuntu"* ]]; then
  echo Preparing env for Ubuntu OS

elif [[ "$OSTYPE" == *"darwin"* ]]; then
  echo Preparing env for MacOS
  # TODO: To add validation that we have brew
  brew install libmagic
  brew install ffmpeg
  
else
  echo "Currently only Ubuntu and OSX"
  exit
fi

# init dupeGuru-result-reviewer env.
python3 -m venv ./env
./env/bin/python3 -m pip install --upgrade pip
./env/bin/pip3 install --upgrade pip

# dupeGuru-result-reviewer install requirements
./env/bin/pip3 install -r requirements.txt

source ./env/bin/activate

mkdir -p logs TMP # TODO: to consider moving this to the python code area

