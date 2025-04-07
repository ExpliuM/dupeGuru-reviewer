#!/bin/bash

# Creating work dirs
mkdir -p logs

# TODO: To add Windows support
if [[ "$OSTYPE" == *"Ubuntu"* ]]; then
  echo Preparing env for Ubuntu OS

elif [[ "$OSTYPE" == *"darwin"* ]]; then
  echo Preparing env for MacOS

  # Install brew
  if ! command -v brew &>/dev/null; then
    echo "Installing brew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi

  echo "Installing brew packages"
  # Declare an array of string with type
  declare -a packages=(
    # App dependencies
    "ffmpeg"
    "libmagic"
    # "python@3.11"
    "python"
    "qt6"

    # Build tools
    "create-dmg"
  )

  for package in "${packages[@]}"; do
    isPackageInstalled=$(brew list "$package" 2>/dev/null)
    if [[ ! -z "$isPackageInstalled" ]]; then
      echo -e "\t${package} is already installed"
      continue
    fi
    echo -e "\tinstalling ${package}"
    brew install "$package" >/dev/null
  done

else
  echo "Currently only Ubuntu and OSX"
  exit
fi

# init dupeGuru-result-reviewer env.
./set-env.sh
