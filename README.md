# Shadows of Doubt | World Name Replacement

This guide will help you change names in the world of "Shadows of Doubt".

## Manual Installation Procedure

1. **Install Python**: Download and install the latest version of Python.
2. **Create a Virtual Environment (Optional)**: You can choose to create a virtual environment to encapsulate your dependencies.
3. **Install Required Packages**: Use `pip install -r requirements.txt` to install all necessary packages.
4. **Check Script Options**: Run `python main.py -h` to see the available script options.

## Usage Instructions

Follow these steps to use the name replacement tool:

1. **Prepare Your World File**: You can either create a new world or use an existing one. The world file should be located in the `cities_path`, typically found here: `C:\Users\...\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Cities`.
2. **Prepare Names File**: Create a text or CSV file with the names you want to see in the game. Example files are available [here](https://github.com/htkg/sod-replace-names/tree/main/input).
3. **Run the Script**: Navigate to the directory where you downloaded the script, then run `python main.py [.cit or .citb file] [your names .csv or .txt]`.
4. **Replace original with edited World**: Navigate to `C:\Users\...\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Cities` and replace old identical world file with the new one that we've got.

> **_Caution:_** Changing the filename of the city results in the city being regenerated upon loading. The city filename must match exactly what's stored in the save file; otherwise, the city will be regenerated. For instance, if your world was named `Kobe.1.3505.U8mdzS4Um6gYj5j7.citb` in the `Shadows of Doubt\Cities` folder, you should replace it with the exact same name to ensure compatibility with older saves.