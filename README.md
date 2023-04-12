# About
This is a GUI program that allows you to compare and delete picture and video duplicates.
In oder to use it you need to generate `results.dupeguru` file by using [dupeGuru](https://dupeguru.voltaicideas.net/) app to scan your folders.

** notice that when you press "delete" this moves the content to a TMP folder, in case you regret it you can undo it.

# Usage example
   ![image](./resources/readme/UsageExample.gif)
# How to use?
1. Run dupeGuru
   ![image](./resources/readme/dupeGuru-main.png)
2. Scan the requested folder.
   ![image](./resources/readme/dupeGuru-Scanning.png)
3. Export the results to the `workspaceFolder` of this project.
   ![image](./resources/readme/dupeGuru-Save%20Results.png)
   ![image](./resources/readme/dupeGuru-Save%20as.png)
4. Run dupeGuru-result-reviewer by typing `./run.sh`
   ![image](./resources/readme/dupeGuru-result-reviewer.png)
5. Enjoy

# Prepare
```terminal
./prepare.sh
```

# Run
```terminal
./run.sh
```