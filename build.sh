#!/bin/bash

FILENAME=dupeGuru-reviewer
LOG_FILE_NAME=build

# Target architecture (macOS only; valid values: x86_64, arm64, universal2).
# architectureArray=("arm64")
architectureArray=("arm64" "x86_64" "universal2")

./prepare.sh
./clean.sh

./env/bin/pip3 uninstall --yes pathlib

for architecture in "${architectureArray[@]}"; do
  echo "building ${architecture} architecture"

  test -d "dist/${FILENAME}.app" && rm -rf "dist/${FILENAME}.app"
  test -d build && rm -rf build

  test -f "${FILENAME}.spec" && rm "${FILENAME}.spec"
  test -f "dist/${FILENAME}" && rm "dist/${FILENAME}"

  # Building app
  echo "running pyinstaller for ${architecture} architecture"
  ./env/bin/pyinstaller --windowed -F --log-level DEBUG --target-arch "${architecture}" "${FILENAME}.py" >"logs/pyinstaller-${LOG_FILE_NAME}-${architecture}.log" 2>&1
  echo "pyinstaller for ${architecture} architecture finished"

  # Building dmg installer
  if [[ -d "dist/${FILENAME}.app" ]]; then
    tar -zcvf dist/${FILENAME}-${architecture}.tar.gz dist/${FILENAME}.app
    
    mkdir -p dist/dmg-${architecture}
    cp -r "dist/${FILENAME}.app" dist/dmg-${architecture}

    test -f "dist/${FILENAME}-${architecture}.dmg" && rm "dist/${FILENAME}.dmg"

    #   --volicon "${FILENAME}.icns" \
    # --hdiutil-verbose \
    # --sandbox-safe \
    echo "running create-dmg for ${architecture} architecture"
    create-dmg \
      --app-drop-link 425 120 \
      --hdiutil-quiet \
      --hide-extension "${FILENAME}.app" \
      --icon "${FILENAME}.app" 175 120 \
      --icon-size 100 \
      --no-internet-enable \
      --volname "${FILENAME}" \
      --window-pos 200 120 \
      --window-size 600 300 \
      "dist/${FILENAME}-${architecture}.dmg" \
      "dist/dmg-${architecture}/" >"logs/create-dmg-${LOG_FILE_NAME}-${architecture}.log" 2>&1

    echo "create-dmg for ${architecture} architecture finished"
  fi
done
