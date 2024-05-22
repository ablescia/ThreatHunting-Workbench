# Compiling Notes

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
