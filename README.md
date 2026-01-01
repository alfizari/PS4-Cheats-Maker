# 🎮 PS4-Cheats-Maker  

An easy-to-use app for working with **Save Wizard quick codes** and **custom scripts** for PS4/PS3/PS2/PS or any game saves.  
It accepts decrypted saves, knowing the CUSA is required. It will treat different CUSA's for the same game as one.
My Discord: alfazari911
If you want to share your scripts, make a pull request.

---
## Current Cheats
* Click Update all on the tool to install the latest cheats
  
| CUSA Code             | Game                             | Cheat Type       |
|------------------------|----------------------------------|------------------|
| CUSA13285 / CUSA13632 | Hollow Knight - Voidheart Edition | Python scripts   |
| CUSA39420             | Hollow Knight: Silksong          | Python scripts   |


## ✨ Features  

1. **Accepts Save Wizard quick codes format**  
   <img width="997" height="660" alt="1" src="https://github.com/user-attachments/assets/c9537f92-8e01-4285-93f5-20a284a52e7e" />

2. **Create your own custom Lua scripts**  
   <img width="1321" height="657" alt="2" src="https://github.com/user-attachments/assets/f9c389f0-5819-4b0e-a549-4f37378505bb" />

3. **Built-in helper functions for scripting (Python tab)**  
   Writing scripts is much easier with the ready-to-use functions.  
   <img width="1439" height="763" alt="3" src="https://github.com/user-attachments/assets/e3e01d36-abdf-40d8-a008-6f90d7048db3" />

---

## ⚠️ Important Note  

Clicking **Update Scripts** will replace any existing scripts you have with those downloaded from GitHub if they already exist, it will also create a backup.  
👉 Please **make a backup** before updating.  

---

## 📖 Help  

- Documentation for built-in functions can be found here:  
  [helpers.py](https://github.com/alfizari/PS4-Cheats-Maker/blob/main/helpers.py)  
- Example
  <img width="1889" height="1004" alt="image" src="https://github.com/user-attachments/assets/62ece646-04fb-4b1d-bf42-e7920e2431a3" />

---

## ➕ Adding Quick Codes  

You can add Quick Codes in two ways:  

1. **Directly via JSON**  
   Add them to the JSON file following the same structure:  
   <img width="1195" height="695" alt="6" src="https://github.com/user-attachments/assets/09c984ac-dcab-4622-ae25-9d14d50c6df5" />

2. **Using the App UI**  
   <img width="978" height="505" alt="5" src="https://github.com/user-attachments/assets/6a4a32b9-3e06-43bc-bd71-9234a60af4f5" />

---

## ⬆️ Uploading Scripts  

- **Lua** and **Python** scripts must be **zipped with 7z** and uploaded to GitHub following the correct naming format.  
- Quick codes are stored in the **JSON file**.  

---

## ⚙️ Built-In Functions  

- Do **not** delete or modify existing functions.  
- To add new ones:  
  - Add the function logic here → [helpers.py](https://github.com/alfizari/PS4-Cheats-Maker/blob/main/helpers.py)  
  - Add the function name here → [built_in_functions.json](https://github.com/alfizari/PS4-Cheats-Maker/blob/main/built_in_functions.json)  

💡 You can debug directly in the app terminal with:  
```python
print("your message here")
```

---

## 🐍 Running the Script Natively  

You need **Python 3** installed.  

**Dependencies:**  
- aiofiles
- lupa  
- requests  
- py7zr  

Install them via pip:  
```bash
pip install aiofiles lupa py7zr requests
```

---

## 📦 Building an Executable  

Use **PyInstaller**:  
```bash
pyinstaller --noconsole --onefile --icon=logo/logo.ico --collect-all lupa main.py
```

---

## 🙌 Credits  

- Quick code script by [@HZH](https://github.com/hzhreal)  
  Found at: [HTOS/quickcodes.py](https://github.com/hzhreal/HTOS/blob/bbf9df3c38bbcc84464d71213d38ce29471001db/app_core/quickcodes.py)
- CUSA list from: https://discord.gg/save-wizard
