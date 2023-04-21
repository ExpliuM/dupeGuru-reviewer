#!/bin/bash

FILENAME=dupeGuru-reviewer
LOG_FILE_NAME=build

# Target architecture (macOS only; valid values: x86_64, arm64, universal2).
architectureArray=("arm64" "x86_64" "universal")

./prepare.sh
./clean.sh
./env/bin/pip3 uninstall pathlib

for architecture in "${architectureArray[@]}"; do
  rm -rf build
  rm setup.py
  # Building app
  ./env/bin/pyinstaller --windowed --log-level DEBUG --target-arch "${architecture}" "${FILENAME}.py" 2>&1 | tee -a "logs/${LOG_FILE_NAME}-${architecture}.log"

  # Building dmg installer
  mkdir -p dist/dmg-${architecture}
  cp -r "dist/${FILENAME}.app" dist/dmg-${architecture}
  test -f "dist/${FILENAME}-${architecture}.dmg" && rm "dist/${FILENAME}.dmg"

  #   --volicon "${FILENAME}.icns" \
  create-dmg \
    --app-drop-link 425 120 \
    --hdiutil-verbose \
    --hide-extension "${FILENAME}.app" \
    --icon "${FILENAME}.app" 175 120 \
    --icon-size 100 \
    --no-internet-enable \
    --volname "${FILENAME}" \
    --window-pos 200 120 \
    --window-size 600 300 \
    "dist/${FILENAME}-${architecture}.dmg" \
    "dist/dmg-${architecture}/"
done

