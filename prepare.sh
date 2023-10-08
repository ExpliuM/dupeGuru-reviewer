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
  
  # Build tools
  brew install create-dmg

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
# ./env/bin/pip3 install --global-option=build_ext --global-option="-I$(brew --prefix libheif)/include/" --global-option="-L$(brew --prefix libheif)/lib/" git+https://github.com/carsales/pyheif.git
# ./env/bin/pip3 install git+https://github.com/carsales/pyheif.git

source ./env/bin/activate
