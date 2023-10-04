# Shadows of Doubt | World Name Replacement: A Comprehensive Guide

This utility changes citizens name according to the text (each new name on newline) or csv file (delimited by ;).
Supports both .citb and .cit files.

## Manual Installation Procedure

To run the name replacement script manually, follow these steps:

1. **Install Python**: Ensure that you have downloaded and installed the latest version of Python on your device.
2. **Create a Virtual Environment (Optional)**: This step is optional but highly recommended. Creating a virtual environment helps encapsulate your dependencies.
3. **Install Required Packages**: Execute the command `pip install -r requirements.txt` in your command prompt or terminal to install all required packages.
4. **Check Script Options**: To view the available script options, run the command `python main.py -h`.

## Binaries

Pre-compiled binaries can be located [here](https://github.com/htkg/sod-replace-names/releases/tag/v1.0.0). The Python to Binary conversion has been performed via Nuitka. For reasons of trust and integrity, feel free to build it from the sources if necessary.

## Usage Instructions

The following steps will guide you on how to use the name replacement tool:

1. **Prepare Your World File**: You have two options here: (a) create a new world, or (b) use an existing one. The world file should be placed in the `cities_path`. Typically, this path would look something like this: `C:\Users\...\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Cities`.
2. **Prepare Names File**: Create a .txt or .csv file containing the names you wish to incorporate into the game. Sample files can be found [here](https://github.com/htkg/sod-replace-names/tree/main/input).
3. **Run the Script**: Navigate to the directory where you've downloaded the script and run either `python main.py [.cit or .citb file] [your names .csv or .txt]` OR `main.exe [.cit or .citb file] [your names .csv or .txt]`, depending on whether you downloaded the binary from the releases.
4. **Replace Original with Edited World**: Traverse to the path `C:\Users\...\AppData\LocalLow\ColePowered Games\Shadows of Doubt\Cities` and replace the old world file with the newly edited one.

> **_Important Note:_** Modifying the filename of the city results in the city being regenerated upon loading. In order to circumvent this, ensure that the city filename matches exactly what's stored in the save file; otherwise, the city will be regenerated. For instance, if your world was named `Kobe.1.3505.U8mdzS4Um6gYj5j7.citb` under the `Shadows of Doubt\Cities` folder, you should use the exact same name for replacement to maintain compatibility with older saves.
