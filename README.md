# Procedura di installazione per Debian bookwork

## Installare la versione di jdk v8:
    
    - aggiungere a sources.list la seguente entry: `deb http://deb.debian.org/debian/ unstable main`
    - installare con `sudo apt install openjdk-8-jdk`

## Scaricare le native library di Hadoop
    
Visitare il sito **https://hadoop.apache.org/releases.html** e scaricare il pacchetto **Binary download**. Successivamente assicurarsi che nel pacchetto sia presente la folder **/lib/native **. In questa cartella sono presenti diverse shared objects.

## Eseguire RumbleDB

Eseguire il runtime di rumbledb eseguendo un webserver locale: `java -jar -Djava.library.path=/home/antonio/Downloads/hadoop-3.3.6/lib/native ./workbench/bin/rumbledb-1.21.0-standalone.jar  serve -p 9090`


## Compile a qrc file

To load an icon from a Qt resource file, you'll first need to compile the resource file, and then you can use the resource path to access and load the icon. Here's a step-by-step guide:

1. **Creating the Resource File**:
   
   If you haven't created a resource file yet, follow these steps:

    - Open Qt Designer.
    - Go to `File` -> `New` and select `Qt Resource File` from the dialog, then click "Create".
    - Save this resource file with a name, for instance, `resources.qrc`.
    - Add a prefix, e.g., `/icons`.
    - With the prefix selected, click "Add Files" and locate your icon, e.g., `icon.png`.
    - Save the `resources.qrc` file.

2. **Compile the Resource File**:
   
   Use the `pyrcc5` tool (for PyQt5) to compile the `.qrc` file into a Python file:

   ```
   pyrcc5 resources.qrc -o resources_rc.py
   ```

3. **Loading the Icon in Python**:
   
   Now in your Python script, you can load the icon from the compiled resource:

   ```python
   from PyQt5.QtGui import QIcon

   # Make sure to import the generated resource module
   import resources_rc

   # Load the icon using the resource path
   icon = QIcon(":/icons/icon.png")
   ```

   The path `:/icons/icon.png` corresponds to the prefix and filename you added to the `.qrc` file. The initial colon `:` indicates that the path refers to a resource path.

4. **Using the Icon**:

   You can now use the loaded icon for any widget or purpose in your PyQt application. For example:

   ```python
   button = QPushButton("Click Me")
   button.setIcon(icon)
   ```

By using Qt's resource system, you embed external files directly into your application, making deployment and distribution easier since you don't need to worry about file paths or missing files.

## Convert evtx files to *.ndjson format

1. Downloads **evtx_dump** from [here](https://github.com/omerbenamram/evtx/releases/);
2. Sets the execution flag with `chmod +x <evtx_dump binary>`
3. Convert the file with `/evtx_dump-v0.8.2-x86_64-unknown-linux-gnu -t 1 -o jsonl -f PowerShell_Operational.ndjson Microsoft-Windows-PowerShell%4Operational.evtx`
   If you need a bulk conversion, use the following inline command: `for file in *.evtx; do ./evtx_dump-v0.8.2-x86_64-unknown-linux-gnu -t 1 -o jsonl -f "${file%.evtx}.ndjson" "$file"; done`

   