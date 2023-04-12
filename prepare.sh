#!/bin/bash

if [[ "$OSTYPE" == *"Ubuntu"* ]]; then
  echo Preparing env for Ubuntu OS

# TODO: To verify that the condition here is good
elif [[ "$OSTYPE" == *"darwin"* ]]; then
  echo Preparing env for MacOS
  # TODO: To add validation that we have brew
  brew install libmagic
  brew install ffmpeg

else
  echo "Currently only Ubuntu and OSX"
  exit
fi

# Modules
mkdir -p ./module
cd module

# Clone dupeguru
git clone https://github.com/arsenetar/dupeguru.git
cd dupeguru
# dupeguru checkout specific version
git checkout 4.3.1

if [[ "$OSTYPE" != *"darwin"* ]]; then
  # # dupeguru install env
  python3 -m venv ./env
  source ./env/bin/activate
  export PATH="$PATH:/opt/homebrew/Cellar/qt@5/5.15.8_2/bin"
  export PATH="$PATH:/usr/local/opt/sphinx-doc/bin"

  # env python and pip upgrade
  ./env/bin/python3 -m pip install --upgrade pip
  ./env/bin/pip3 install --upgrade pip

  # dupeguru requirements, build and run
  ./env/bin/pip3 install -r requirements.txt
  ./env/bin/python3 build.py
  ./env/bin/python3 run.py
  # python package.py
fi

cd ../../

# init dupeGuru-result-reviewer env.
python3 -m venv ./env
./env/bin/python3 -m pip install --upgrade pip
./env/bin/pip3 install --upgrade pip

# dupeGuru-result-reviewer install requirements
./env/bin/pip3 install -r requirements.txt

source ./env/bin/activate
