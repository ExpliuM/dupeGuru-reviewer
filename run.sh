#!/bin/bash

# if [[ "$OSTYPE" == *"Ubuntu"* ]]; then
#   echo Preparing env for Ubuntu OS

# elif [[ "$OSTYPE" == *"darwin"* ]]; then
#   echo Preparing env for MacOS
#   export PATH="$PATH:/opt/homebrew/Cellar/qt5/bin/"
#   export PATH="$PATH:/usr/local/opt/sphinx-doc/bin"
# else
#   echo "Currently only Ubuntu and OSX"
#   exit
# fi

./env/bin/python3 MainWindow.py
