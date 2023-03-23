# Install
```bash
  python3 -m venv ./env
  ./env/bin/pip3 install -r requirements.txt

  mkdir -p ./module
  cd module
  git clone https://github.com/arsenetar/dupeguru.git
  cd dupeguru
  git checkout 4.3.1
  
  python3 -m venv --system-site-packages ./env
  source ./env/bin/activate
  ./env/bin/pip3 install -r requirements.txt
  ./env/bin/python3 build.py
  chmod +x run.py
  cd ../../
```

# Run
```bash
  ./env/bin/python3 MainWindow.py
```

# Future development
 - Some of the file paths to clipboard
 - Open in finder