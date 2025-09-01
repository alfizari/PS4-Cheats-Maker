import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk, PhotoImage
import os
import json
from quickcodes import QuickCodes
import re
import asyncio
from lupa import LuaRuntime
import helpers 
import sys
import requests
import py7zr
import shutil
import webbrowser




#Checksum
def is_there_checksum(game_name):
    # Will run only of the txt for that game exists 
    try:
        check_dir = get_local_path("checksum")
        txt_path = os.path.join(check_dir, f"{game_name}.txt")
        
        # Check if file exists
        if not os.path.exists(txt_path):
            return
        # Read the code
        with open(txt_path, "r", encoding="utf-8") as f:
            code = f.read()
        
        # Prepare execution environment with helper functions and current context
        globals_dict = {
            "__builtins__": __builtins__,
            "save_data": current_save_data, 
            "current_cusa": cusa_var.get() if 'cusa_var' in globals() else None,
        }
        
        # Add all helper functions automatically
        globals_dict.update(get_helper_globals())
        
        # Execute the checksum code
        exec(code, globals_dict)
        
        return True
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"Error executing checksum code for {game_name}: {e}")
        return False


#dirc

def get_local_path(relative_path):
    """
    Returns a path relative to the script (or exe) location.
    Works in development and after building the .exe.
    """
    if getattr(sys, "frozen", False):
        # Running as .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as .py script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)



##GITHUB stuff

# Path to local JSON
LOCAL_JSON = get_local_path("quickcodes.json")
GITHUB_JSON_URL = "https://raw.githubusercontent.com/alfizari/PS4-Cheats-Maker/main/quickcodes.json"

def download_latest_quickcodes():
    try:
        proceed = messagebox.askyesno(
        "Confirm Update",
        f"This will replace any existing file, Do you wish to continue?",
        )
        if not proceed:
            return
        response = requests.get(GITHUB_JSON_URL)
        response.raise_for_status()  # raise error if request failed

        # Write the downloaded JSON to local file
        with open(LOCAL_JSON, "wb") as f:
            f.write(response.content)

        messagebox.showinfo("Success", "Quick codes updated successfully!")
        

        update_quick_codes()  

    except requests.RequestException as e:
        messagebox.showerror("Download Failed", f"Could not download quick codes:\n{e}")


LOCAL_txt = get_local_path("cusa_list.txt")
GITHUB_txt_URL = "https://raw.githubusercontent.com/alfizari/PS4-Cheats-Maker/main/cusa_list.txt"
def download_latest_CUSA():
    try:
        proceed = messagebox.askyesno(
        "Confirm Update",
        f"This will replace any existing file, Do you wish to continue?",
        )
        if not proceed:
            return
        response = requests.get(GITHUB_txt_URL)
        response.raise_for_status()  # raise error if request failed

   
        with open(LOCAL_txt, "wb") as f:
            f.write(response.content)

        messagebox.showinfo("Success", "CUSA updated successfully!")
        
        # Optional: reload the quick codes in your app
        load_cusa_game_mapping()

    except requests.RequestException as e:
        messagebox.showerror("Download Failed", f"Could not download quick codes:\n{e}")



LOCAL_func_py = get_local_path("helpers.py")
GITHUB_func_py = "https://raw.githubusercontent.com/alfizari/PS4-Cheats-Maker/main/helpers.py"

LOCAL_func_json = get_local_path("built_in_functions.json")
GITHUB_func_json = "https://raw.githubusercontent.com/alfizari/PS4-Cheats-Maker/main/built_in_functions.json"

def download_latest_built_in_functions(GITHUB_FUNC_LINK, LOCAL_PATH):
    try:
        response = requests.get(GITHUB_FUNC_LINK)
        response.raise_for_status()  # raise error if request failed

        # Write the downloaded JSON to local file
        with open(LOCAL_PATH, "wb") as f:
            f.write(response.content)

        messagebox.showinfo("Success", "Built_In_Functions updated successfully!")
        

        load_built_in_functions(jsons)
        run_python_script_auto()

    except requests.RequestException as e:
        messagebox.showerror("Download Failed", f"Could not download quick codes:\n{e}")

def update_func():
    download_latest_built_in_functions(GITHUB_func_py, LOCAL_func_py)
    download_latest_built_in_functions(GITHUB_func_json,LOCAL_func_json)


def download_latest_7z_folder(zip_url, local_folder):
    """
    Alternative version that creates a backup of replaced files
    """
    try:
        proceed = messagebox.askyesno(
            "Confirm Update",
            f"This will update scripts in '{os.path.basename(local_folder)}'.\n"
            f"Files with the same name will be replaced (backup created).\n"
            f"Other existing files will be preserved.\nDo you want to continue?",
        )
        if not proceed:
            return

        response = requests.get(zip_url)
        response.raise_for_status()

        # Create target folder if it doesn't exist
        os.makedirs(local_folder, exist_ok=True)

        # Create backup folder for replaced files
        backup_folder = f"{local_folder}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Write to temporary .7z file
        temp_file = os.path.join(os.path.dirname(__file__), "__temp.7z")
        with open(temp_file, "wb") as f:
            f.write(response.content)

        # Create temporary extraction directory
        temp_extract_dir = os.path.join(os.path.dirname(__file__), "__temp_extract")
        
        # Open the archive
        with py7zr.SevenZipFile(temp_file, mode='r') as archive:
            all_files = archive.getnames()

            # Detect top-level folder
            top_level_folders = set(f.split('/')[0] for f in all_files if f.strip() != "")
            
            if len(top_level_folders) == 1:
                # Extract to temporary folder first
                archive.extractall(path=temp_extract_dir)
                extracted_folder = os.path.join(temp_extract_dir, list(top_level_folders)[0])
                source_folder = extracted_folder
            else:
                # Extract directly to temp folder if no single top-level folder
                archive.extractall(path=temp_extract_dir)
                source_folder = temp_extract_dir

            # Copy files with backup
            copy_files_with_backup(source_folder, local_folder, backup_folder)

        # Clean up temporary files
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
            
        backup_msg = f"\nBackup created: {os.path.basename(backup_folder)}" if os.path.exists(backup_folder) else ""
        messagebox.showinfo("Success", f"{os.path.basename(local_folder)} updated successfully!{backup_msg}")

    except requests.RequestException as e:
        messagebox.showerror("Download Failed", f"Could not download {os.path.basename(local_folder)}:\n{e}")
    except py7zr.exceptions.Bad7zFile as e:
        messagebox.showerror("Extraction Failed", f"Downloaded .7z file is invalid:\n{e}")
    except Exception as e:
        messagebox.showerror("Update Failed", f"Failed to update {os.path.basename(local_folder)}:\n{e}")

def copy_files_with_backup(source_folder, target_folder, backup_folder):
    """
    Copy files from source to target with backup of replaced files.
    """
    backup_created = False
    
    for root, dirs, files in os.walk(source_folder):
        # Calculate relative path from source folder
        rel_path = os.path.relpath(root, source_folder)
        
        # Create corresponding directory structure in target
        if rel_path != '.':
            target_dir = os.path.join(target_folder, rel_path)
        else:
            target_dir = target_folder
            
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy all files from this directory
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)
            
            try:
                # Create backup if file already exists
                if os.path.exists(target_file):
                    if not backup_created:
                        os.makedirs(backup_folder, exist_ok=True)
                        backup_created = True
                    
                    # Create backup directory structure
                    if rel_path != '.':
                        backup_dir = os.path.join(backup_folder, rel_path)
                    else:
                        backup_dir = backup_folder
                    os.makedirs(backup_dir, exist_ok=True)
                    
                    backup_file = os.path.join(backup_dir, file)
                    shutil.copy2(target_file, backup_file)
                    print(f"Backed up: {os.path.relpath(target_file, target_folder)}")
                
                # Copy new file
                shutil.copy2(source_file, target_file)
                print(f"Updated: {os.path.relpath(target_file, target_folder)}")
                
            except Exception as e:
                print(f"Failed to copy {file}: {e}")


LOCAL_PYTHON_DIR = get_local_path("python_scripts")
GITHUB_PYTHON_7Z = "https://github.com/alfizari/PS4-Cheats-Maker/raw/main/python_scripts.7z"

LOCAL_LUA_DIR = get_local_path("lua_scripts")
GITHUB_LUA_ZIP = "https://github.com/alfizari/PS4-Cheats-Maker/raw/main/lua_scripts.7z"

LOCAL_check_DIR = get_local_path("checksum")
GITHUB_check_ZIP = "https://github.com/alfizari/PS4-Cheats-Maker/raw/main/checksum.7z"

def download_latest_python_scripts():
    download_latest_7z_folder(GITHUB_PYTHON_7Z, LOCAL_PYTHON_DIR)
    load_python_scripts()  # reload in GUI

def download_latest_lua_scripts():
    download_latest_7z_folder(GITHUB_LUA_ZIP, LOCAL_LUA_DIR)
    load_cheat_buttons()   # reload lua scripts in GUI

def download_latest_check_scripts():
    download_latest_7z_folder(GITHUB_check_ZIP, LOCAL_check_DIR)

def update_all():
    proceed = messagebox.askyesno(
        "Confirm Update",
        f"This will replace any existing file, Do you wish to continue?",
    )
    if not proceed:
        return
    download_latest_python_scripts()
    download_latest_lua_scripts()
    update_func()
    download_latest_quickcodes()
    download_latest_CUSA()
    download_latest_check_scripts()

################################################33



# Main window
root = tk.Tk()
root.title("Cheat Maker PS4")
root.geometry("800x500")

# ====== Menu Bar ======
menubar = tk.Menu(root)

# Global variables
file_path = tk.StringVar()
cusa_var = tk.StringVar()
game_name_var = tk.StringVar()
quick_code_var = tk.StringVar()
cusa_to_game = {}
data = None  # Will hold the loaded save file data



logo_dir = get_local_path("logo")
ico_path = os.path.join(logo_dir, "logo.ico")
png_path = os.path.join(logo_dir, "logo.png")

# Try ico first
if os.path.exists(ico_path):
    try:
        root.iconbitmap(ico_path)
    except Exception as e:
        print(f"Failed to load ico: {e}")

# Fallback to PNG
if os.path.exists(png_path):
    logo = PhotoImage(file=png_path)
    root.iconphoto(True, logo)



# Ensure folder exists
PYTHON_SCRIPTS_DIR = get_local_path("python_scripts")
if not os.path.exists(PYTHON_SCRIPTS_DIR):
    os.makedirs(PYTHON_SCRIPTS_DIR)



jsons = get_local_path("built_in_functions.json")
def create_new_script():
    """Create a new empty script template and load it into editor"""
    cusa = cusa_var.get()
    if not cusa:
        messagebox.showwarning("Warning", "No CUSA selected!")
        return

    name = simpledialog.askstring("Script Name", "Enter script name:" , parent=root)
    if not name:
        return

    author = simpledialog.askstring("Author", "Enter author name:", parent=root)
    if not author:
        return

    # Create template code in editor
    template_code = f"""# Author: {author}
# CUSA: {cusa}

# Your script code here
# Available variables:
#   save_data - the current save file data (bytearray)
#   current_cusa - the current CUSA ID

# Example usage:
# value = read_int(0x1000, save_data)
# write_int(0x1000, 999999, save_data)
# to print to console: print("Hello from script!"), print(value)
"""
    
    # Load template into editor
    python_text.delete("1.0", "end")
    python_text.insert("1.0", template_code)
    
    messagebox.showinfo("Template Created", f"New script template created for {name}.\nUse 'Save Script' to save it.")

def save_script():
    """Save the current editor content as a script with author info"""
    cusa = cusa_var.get()
    if not cusa:
        messagebox.showwarning("Warning", "No CUSA selected!")
        return

    # Get current content
    current_content = python_text.get("1.0", "end-1c")  # -1c removes extra newline
    if not current_content.strip():
        messagebox.showwarning("Warning", "Editor is empty! Nothing to save.")
        return
    # Get script name
    script_name = simpledialog.askstring("Save Script As", "Enter script name:", parent=root)
    if not script_name:
        return

    # Get author name
    author_name = simpledialog.askstring("Author", "Enter your name for this script:", parent=root)
    if not author_name:
        author_name = "Unknown"


    filename = f"{cusa}_{script_name}.py"
    full_path = os.path.join(PYTHON_SCRIPTS_DIR, filename)
    
    # Check if file exists
    if os.path.exists(full_path):
        result = messagebox.askyesno("File Exists", 
                                   f"Script '{filename}' already exists.\n\nOverwrite it?")
        if not result:
            return

    # Prepend script/author comments
    header = f"# Script: {script_name}\n# Author: {author_name}\n\n"
    content_to_save = header + current_content

    # Save the file
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content_to_save)
        
        messagebox.showinfo("Saved", f"Script saved as {filename}")
        load_python_scripts()  # Refresh script buttons
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save script:\n{str(e)}")


def update_current_script():
    """Update/overwrite the currently loaded script"""
    current_content = python_text.get("1.0", "end-1c")
    if not current_content.strip():
        messagebox.showwarning("Warning", "Editor is empty! Nothing to save.")
        return
    
    # Try to extract filename from current content
    lines = current_content.split('\n')
    cusa = None
    for line in lines[:5]:  # Check first 5 lines for CUSA
        if line.strip().startswith("# CUSA:"):
            cusa = line.split(":")[-1].strip()
            break
    
    if not cusa:
        messagebox.showwarning("Warning", "Cannot determine CUSA from current script.\nUse 'Save Script As' instead.")
        return
    
    # Ask for confirmation
    result = messagebox.askyesno("Update Script", 
                               "This will overwrite the currently loaded script.\n\nContinue?")
    if not result:
        return
    
    # Find the script file (this is a simplified approach)
    # In a more robust implementation, you'd track which file is currently loaded
    name = simpledialog.askstring("Script Name", "Enter the name of the script to update:")
    if not name:
        return
    
    filename = f"{cusa}_{name}.py"
    full_path = os.path.join(PYTHON_SCRIPTS_DIR, filename)
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(current_content)
        
        messagebox.showinfo("Updated", f"Script {filename} updated successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update script:\n{str(e)}")

# ---------- Load buttons for current CUSA scripts ----------
def load_python_scripts():
    """Load script buttons for current CUSA in both Python tab and Quick Codes tab"""
    # Clear existing buttons in python tab
    for widget in python_scripts_frame.winfo_children():
        widget.destroy()
    
    # Clear existing buttons in quick codes tab
    for widget in python_quick_frame.winfo_children():
        widget.destroy()
    
    cusa = cusa_var.get()
    if not cusa:
        return
    
    # Get the current game name
    game_name = get_game_name_from_cusa(cusa)
    
    # Get all CUSAs for this game
    script_cusas = [key for key, name in cusa_to_game.items() if name == game_name]
    if not script_cusas:
        script_cusas = [cusa]  # fallback
    
    # Check if directory exists
    if not os.path.exists(PYTHON_SCRIPTS_DIR):
        return
    
    # Collect all scripts for all relevant CUSAs
    script_files = []
    try:
        for filename in os.listdir(PYTHON_SCRIPTS_DIR):
            for scusa in script_cusas:
                if filename.startswith(scusa) and filename.endswith(".py"):
                    script_files.append(filename)
                    break
    except Exception as e:
        print(f"Error loading scripts: {e}")
        return
    
    if not script_files:
        # Show "No scripts" message in both locations
        ttk.Label(python_scripts_frame, text="No scripts found for this CUSA/game").pack(pady=10)
        ttk.Label(python_quick_frame, text="No Python scripts found").pack(pady=5)
        return
    
    # Create buttons in both locations
    for filename in sorted(script_files):
        full_path = os.path.join(PYTHON_SCRIPTS_DIR, filename)
        
        # Default display
        script_name, author_name = filename, "Unknown"
        for scusa in script_cusas:
            script_name = script_name.replace(f"{scusa}_", "")
        script_name = script_name.replace(".py", "")
        
        # Try reading author from first lines
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[:5]:  # only check first 5 lines
                    if line.lower().startswith("# script:"):
                        script_name = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("# author:"):
                        author_name = line.split(":", 1)[1].strip()
        except Exception:
            pass
        
        display_name = f"{script_name} by {author_name}"
        
        def load_script(p=full_path, fn=filename):
            load_python_script(p, fn)
        
        def run_script(p=full_path):
            run_python_script(p)
        
        # ===== Python Scripts Tab Buttons =====
        script_frame = ttk.Frame(python_scripts_frame)
        script_frame.pack(fill="x", pady=1, padx=5)
        
        btn = ttk.Button(script_frame, text=display_name, command=load_script)
        btn.pack(side="left", fill="x", expand=True)
        
        del_btn = ttk.Button(script_frame, text="×", width=3,
                             command=lambda p=full_path, fn=filename: delete_script(p, fn))
        del_btn.pack(side="right", padx=(2, 0))
        
        def show_context_menu(event, path=full_path, fn=filename):
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Load in Editor",
                                     command=lambda: load_python_script(path, fn))
            context_menu.add_command(label="Run Script",
                                     command=lambda: run_python_script(path))
            context_menu.add_command(label="Delete",
                                     command=lambda: delete_script(path, fn))
            context_menu.post(event.x_root, event.y_root)
        
        btn.bind("<Button-3>", show_context_menu)
        
        # ===== Quick Codes Tab Buttons =====
        quick_script_frame = ttk.Frame(python_quick_frame)
        quick_script_frame.pack(fill="x", pady=1)
        
        quick_btn = ttk.Button(quick_script_frame, text=f"▶ {display_name}", command=run_script)
        quick_btn.pack(side="left", fill="x", expand=True)
        
        edit_btn = ttk.Button(quick_script_frame, text="✏", width=3, command=load_script)
        edit_btn.pack(side="right", padx=(2, 0))
        
        def show_quick_context_menu(event, path=full_path, fn=filename):
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Run Script",
                                     command=lambda: run_python_script(path))
            context_menu.add_command(label="Edit Script",
                                     command=lambda: load_python_script(path, fn))
            context_menu.post(event.x_root, event.y_root)
        
        quick_btn.bind("<Button-3>", show_quick_context_menu)



def load_python_script(path, filename=None):
    """Load script into editor"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            python_text.delete("1.0", "end")
            python_text.insert("1.0", content)
        
        if filename:
            print(f"Loaded script: {filename}")  # Or update a status bar
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load script:\n{str(e)}")

def delete_script(path, filename):
    """Delete a script file"""
    result = messagebox.askyesno("Delete Script", 
                               f"Are you sure you want to delete '{filename}'?\n\nThis cannot be undone!")
    if result:
        try:
            os.remove(path)
            messagebox.showinfo("Deleted", f"Script '{filename}' deleted successfully!")
            load_python_scripts()  # Refresh the list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete script:\n{str(e)}")

def run_python_script(path=None):
    """Run a Python script"""
    try:
        if path:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            code = python_text.get("1.0", "end-1c")

        if not code.strip():
            messagebox.showwarning("Warning", "No code to run!")
            return

        # Create globals dict with all helper functions
        globals_dict = {
            "__builtins__": __builtins__,
            "save_data": current_save_data,
            "current_cusa": cusa_var.get(),
        }
        
        # Add all helper functions automatically
        globals_dict.update(get_helper_globals())

        exec(code, globals_dict)
        messagebox.showinfo("Success", "Script executed successfully!")

    except Exception as e:
        messagebox.showerror("Python Error", f"Script execution failed:\n\n{str(e)}")

# Helper function to get all helper functions (from previous code)
def get_helper_globals():
    """Automatically get all helper functions from helpers module"""
    try:
 
        helper_functions = {}
        
        for name in dir(helpers):
            if not name.startswith('_'):
                attr = getattr(helpers, name)
                if callable(attr):
                    helper_functions[name] = attr
        
        return helper_functions
    except ImportError:
        print("Warning: helpers module not found")
        return {}

# Updated run_python_script using automatic helper detection
def run_python_script_auto(path=None):
    try:
        if path:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            code = python_text.get("1.0", "end")

        # Automatically get all helper functions
        globals_dict = {
            "__builtins__": __builtins__,
            "save_data": current_save_data,
            "current_cusa": cusa_var.get(),
        }
        
        # Add all helper functions automatically
        globals_dict.update(get_helper_globals())

        exec(code, globals_dict)

    except Exception as e:
        messagebox.showerror("Python Error", str(e))

# ---------- Edit script (load into editor) ----------
def edit_python_script(path):
    load_python_script(path)
def load_built_in_functions(jsons):
    try:
        with open(jsons, "r", encoding="utf-8") as f:
            functions = json.load(f)
    except Exception as e:
        print("Failed to load built-in functions:", e)
        functions = []

    # Frame for search + scrollable buttons
    builtins_frame = ttk.Frame(left_python_frame)
    builtins_frame.pack(fill="both", expand=True, pady=5)

    # Search entry
    search_var = tk.StringVar()
    search_entry = ttk.Entry(builtins_frame, textvariable=search_var)
    search_entry.pack(fill="x", padx=5, pady=(0, 5))

    # Scrollable canvas
    canvas = tk.Canvas(builtins_frame)
    scrollbar = ttk.Scrollbar(builtins_frame, orient="vertical", command=canvas.yview)
    buttons_frame = ttk.Frame(canvas)

    buttons_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=buttons_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Populate buttons
    button_refs = []  # keep refs for filtering later

    def populate_buttons():
        # Clear old
        for widget in buttons_frame.winfo_children():
            widget.destroy()

        query = search_var.get().lower()

        for func in functions:
            name = func.get("name", "Unnamed")
            template = func.get("template", "")

            if query and query not in name.lower():
                continue  # filter out non-matching

            btn = ttk.Button(
                buttons_frame,
                text=name,
                command=lambda t=template: insert_helper(t)
            )
            btn.pack(fill="x", pady=2, padx=5)
            button_refs.append(btn)

    # Run initial population
    populate_buttons()

    # Update when typing in search
    search_var.trace_add("write", lambda *_: populate_buttons())

# --- Insert helper function template into editor ---
def insert_helper(template):
    python_text.insert(tk.INSERT, template)
    python_text.focus()  # Optional: focus back to editor

#
## LUA STUFF
# Lua Cheat Starter template as a string
LUA_CHEAT_STARTER = '''-- ============================================
-- Lua Cheat Starter for Save Editor
-- Preloaded Helpers: Byte, UInt16, UInt32, AOB Search
-- ============================================

-- ===== Helper Functions =====

-- Read a single byte
function read_byte(offset)
    return save.data[offset + 1]
end

-- Write a single byte
function write_byte(offset, value)
    save.data[offset + 1] = value
end

-- Read 16-bit little-endian integer
function read_uint16(offset)
    local b1 = save.data[offset + 1]
    local b2 = save.data[offset + 2]
    return b1 + b2 * 256
end

-- Write 16-bit little-endian integer
function write_uint16(offset, value)
    save.data[offset + 1] = value % 256
    save.data[offset + 2] = math.floor(value / 256) % 256
end

-- Read 32-bit little-endian integer
function read_uint32(offset)
    local b1 = save.data[offset + 1]
    local b2 = save.data[offset + 2]
    local b3 = save.data[offset + 3]
    local b4 = save.data[offset + 4]
    return b1 + b2*256 + b3*65536 + b4*16777216
end

-- Write 32-bit little-endian integer
function write_uint32(offset, value)
    save.data[offset + 1] = value % 256
    save.data[offset + 2] = math.floor(value / 256) % 256
    save.data[offset + 3] = math.floor(value / 65536) % 256
    save.data[offset + 4] = math.floor(value / 16777216) % 256
end

-- Search for a single byte value
function find_value(value)
    local offsets = {}
    for i = 1, #save.data do
        if save.data[i] == value then
            table.insert(offsets, i - 1)  -- 0-based
        end
    end
    return offsets
end

-- =============================
-- Array of Bytes (AOB) Search
-- pattern: table of bytes, use nil for wildcard
function find_pattern(pattern)
    local matches = {}
    local plen = #pattern
    local data_len = #save.data

    for i = 1, data_len - plen + 1 do
        local match = true
        for j = 1, plen do
            if pattern[j] ~= nil and save.data[i + j - 1] ~= pattern[j] then
                match = false
                break
            end
        end
        if match then
            table.insert(matches, i - 1)  -- 0-based
        end
    end
    return matches
end

-- Apply all changes back to the save file
function apply()
    write_back(save)
end
exmpl 
we first define a few helper functions to read and write bytes and integers. Then we provide functions to search for values and patterns. Finally, we have an apply function that writes back any changes made to the save data.
-- Write a single byte at a given offset
function write_byte(offset, value)
    save.data[offset] = value
end

function apply()
    -- Example: write 11 at offset 0x1000
    write_byte(0x1000, 1)
    write_back(save)
end

apply()
-- ===== Example Usage =====
-- Modify single byte
-- write_byte(0x102, 22)

-- Modify 16-bit integer
-- write_uint16(0x104, 300)

-- Modify 32-bit integer
-- write_uint32(0x108, 12345678)

-- Search for a value
-- local offsets = find_value(99)
-- for _, off in ipairs(offsets) do
--     print(string.format("Found 99 at 0x%X", off))
-- end

-- Search for a pattern (0x12 0x34 any byte 0x56)
-- local offsets = find_pattern({0x12, 0x34, nil, 0x56})
-- for _, off in ipairs(offsets) do
--     print(string.format("Pattern found at 0x%X", off))
-- end

-- Apply changes
-- apply()
'''
lua = LuaRuntime(unpack_returned_tuples=True)


LUA_SCRIPTS_DIR = get_local_path("lua_scripts")
if not os.path.exists(LUA_SCRIPTS_DIR):
    os.makedirs(LUA_SCRIPTS_DIR)

# Store loaded save file data in a Python bytearray so Lua can manipulate it
current_save_data = None  # Will be updated when opening a file

def create_lua_cheat():
    lua_text.delete("1.0", tk.END)
    lua_text.insert(tk.END, LUA_CHEAT_STARTER)

def save_lua_cheat():
    # Ask user where to save the Lua script
    path = filedialog.asksaveasfilename(defaultextension=".lua",
                                        filetypes=[("Lua files", "*.lua")])
    if not path:
        return
    script_content = lua_text.get("1.0", tk.END)
    with open(path, "w", encoding="utf-8") as f:
        f.write(script_content)
    messagebox.showinfo("Saved", f"Lua script saved to {path}")

def run_lua_script():
    global current_save_data
    if current_save_data is None:
        messagebox.showwarning("No Save", "Load a save file first!")
        return

    # Expose save data to Lua as a table
    lua_table = lua.table_from({"data": bytearray(current_save_data)})

    # Expose a Python helper to write back changes
    def write_back(lua_table):
        global current_save_data
        # Convert Lua table back to Python bytearray
        current_save_data[:] = bytearray(lua_table["data"])  # <-- update in-place
        # Write to disk
        save_path = file_path.get()
        if save_path:
            with open(save_path, "wb") as f:
                f.write(current_save_data)
            messagebox.showinfo("Saved", "Lua modifications applied to save file!")

    lua.globals().write_back = write_back
    lua.globals().save = lua_table

    try:
        script = lua_text.get("1.0", tk.END)
        lua.execute(script)
        # Users are expected to call write_back(save) at the end of their script
    except Exception as e:
        messagebox.showerror("Lua Error", str(e))

def add_cheat_to_list():
    cusa = cusa_var.get()
    if not cusa:
        messagebox.showwarning("No CUSA", "Load a save file first.")
        return

    cheat_name = simpledialog.askstring("Cheat Name", "Enter a name for this cheat:")
    if not cheat_name:
        return

    author_name = simpledialog.askstring("Author", "Enter the author's name:")
    if not author_name:
        author_name = "Unknown"

    # Always prefix with CUSA and optionally author in filename
    # e.g., CUSA07295_max_health_by_ahmed.lua
    safe_cheat_name = cheat_name.strip().replace(" ", "_")
    safe_author = author_name.strip().replace(" ", "_")
    filename = f"{cusa}_{safe_cheat_name}_by_{safe_author}.lua"
    path = os.path.join(LUA_SCRIPTS_DIR, filename)

    # Prepend author comment inside the Lua script
    script_content = lua_text.get("1.0", tk.END).strip()
    script_with_author = f"-- Cheat: {cheat_name}\n-- Author: {author_name}\n\n{script_content}"

    with open(path, "w", encoding="utf-8") as f:
        f.write(script_with_author)

    messagebox.showinfo("Saved", f"Cheat saved as {filename}")
    load_cheat_buttons()


def load_cheat_buttons():
    """Load Lua script buttons for current CUSA in both Lua tab and Quick Codes tab"""
    # Clear existing buttons in lua tab
    for widget in cheats_frame.winfo_children():
        widget.destroy()
    
    # Clear existing buttons in quick codes tab
    for widget in lua_quick_frame.winfo_children():
        widget.destroy()
    
    cusa = cusa_var.get()
    if not cusa:
        return
    
    if not os.path.exists(LUA_SCRIPTS_DIR):
        ttk.Label(lua_quick_frame, text="No Lua scripts found").pack(pady=5)
        return
    
    lua_files = []
    try:
        for filename in os.listdir(LUA_SCRIPTS_DIR):
            if filename.startswith(cusa) and filename.endswith(".lua"):
                lua_files.append(filename)
    except Exception as e:
        print(f"Error loading Lua scripts: {e}")
        return
    
    if not lua_files:
        ttk.Label(lua_quick_frame, text="No Lua scripts found").pack(pady=5)
        return
    
    for filename in sorted(lua_files):
        full_path = os.path.join(LUA_SCRIPTS_DIR, filename)
        
        # Try to read cheat name and author from first lines
        cheat_name, author_name = filename.replace(f"{cusa}_", "").replace(".lua", ""), "Unknown"
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[:5]:  # read only first 5 lines
                    if line.lower().startswith("-- cheat:"):
                        cheat_name = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("-- author:"):
                        author_name = line.split(":", 1)[1].strip()
        except Exception:
            pass
        
        display_name = f"{cheat_name} by {author_name}"
        
        style = ttk.Style()
        style.configure("Left.TButton", anchor="w")
        
        # ===== Lua Scripts Tab Button =====
        btn = ttk.Button(
            cheats_frame,
            text=display_name,
            style="Left.TButton",
            command=lambda p=full_path: run_lua_file(p)
        )
        btn.pack(fill="x", pady=2)
        btn.bind("<Button-3>", lambda e, p=full_path: edit_lua_file(p))
        
        # ===== Quick Codes Tab Button =====
        quick_lua_frame = ttk.Frame(lua_quick_frame)
        quick_lua_frame.pack(fill="x", pady=1)
        
        quick_lua_btn = ttk.Button(
            quick_lua_frame,
            text=f"▶ {display_name}",
            command=lambda p=full_path: run_lua_file(p)
        )
        quick_lua_btn.pack(side="left", fill="x", expand=True)
        
        edit_lua_btn = ttk.Button(
            quick_lua_frame,
            text="✏",
            width=3,
            command=lambda p=full_path: edit_lua_file(p)
        )
        edit_lua_btn.pack(side="right", padx=(2, 0))
        
        def show_lua_quick_context_menu(event, path=full_path):
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Run Script",
                                     command=lambda: run_lua_file(path))
            context_menu.add_command(label="Edit Script",
                                     command=lambda: edit_lua_file(path))
            context_menu.post(event.x_root, event.y_root)
        
        quick_lua_btn.bind("<Button-3>", show_lua_quick_context_menu)
    
    cheats_frame.update_idletasks()
    cheats_canvas.configure(scrollregion=cheats_canvas.bbox("all"))



# Enable mouse wheel scrolling on the canvas
def on_mousewheel(event):
    cheats_canvas.yview_scroll(int(-1*(event.delta/120)), "units")




def edit_lua_file(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        script = f.read()

    # Fill the editor with the cheat content
    lua_text.delete("1.0", tk.END)
    lua_text.insert(tk.END, script)
def run_lua_file(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"File not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        script = f.read()

    try:
        lua.execute(script)
        messagebox.showinfo("Success", f"Cheat applied: {os.path.basename(path)}")
    except Exception as e:
        messagebox.showerror("Lua Error", str(e))




######################################3

def add_id_to_list():
    filename = "cusa_list.txt"
    text_path = get_local_path(filename)

    # Create a temporary root window (hidden)
    root = tk.Tk()
    root.withdraw()

    game_id = simpledialog.askstring("Add Game", "Enter Game ID: No spaces or _")
    if not game_id:
        messagebox.showwarning("Canceled", "No Game ID entered.")
        return

    game_name = simpledialog.askstring("Add Game", "Enter Game Name:")
    if not game_name:
        messagebox.showwarning("Canceled", "No Game Name entered.")
        return

    entry = f"{game_id.strip()}//{game_name.strip()}"

    # Check if already in the file
    try:
        with open(text_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
            if entry in lines:
                messagebox.showinfo("Duplicate", "⚠️ Entry already exists in the list.")
                return
    except FileNotFoundError:
        lines = []

    # Append entry
    with open(text_path, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

    messagebox.showinfo("Success", f"✅ Added:\n{entry}")

#MAIN SCRIPT FUNCTIONS

def load_cusa_game_mapping(filename="cusa_list.txt"):

    global cusa_to_game
    text_path = get_local_path(filename)
    
    if not os.path.exists(text_path):
        print(f"CUSA mapping file not found: {text_path}")
        return

    with open(text_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()


    for line in lines:
        line = line.strip()
        if not line or line.lower().startswith("save ids"):
            continue
        # Split on '//' with optional spaces
        parts = re.split(r'\s*//\s*', line)
        if len(parts) >= 2:
            cusa = parts[0].strip().upper()
            game_name = parts[1].strip()
            cusa_to_game[cusa] = game_name


def get_game_name_from_cusa(cusa):

    if not cusa:
        return "Unknown Game"
    cusa_key = cusa.strip().upper()

    return cusa_to_game.get(cusa_key, "Unknown Game")

def ask_current_cusa():

    cusa = simpledialog.askstring("CUSA Input", "Enter the CUSA of this save file:", initialvalue="CUSA")
    if not cusa:
        messagebox.showwarning("CUSA required", "You must enter a CUSA code to continue.")
        return None
    return cusa

def load_codes(json_file="quickcodes.json"):
    """Load all quick codes from JSON file."""
    json_path = get_local_path(json_file)

    if not os.path.exists(json_path):
        print(f'JSON file not found: {json_path}')
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure each code entry is in the new format: {"code": "...", "author": "..."}
    codes_list = data.get("codes", [])
    for entry in codes_list:
        codes_dict = entry.get("codes", {})
        for k, v in codes_dict.items():
            # If v is still a string (old format), convert to dict
            if isinstance(v, str):
                codes_dict[k] = {"code": v, "author": "Unknown"}

    return codes_list


def get_codes_for_cusa(cusa):
    all_codes = load_codes()
    return [entry for entry in all_codes if entry.get("CUSA") == cusa]

def open_file():
    """Open a save file and load it into memory"""
    selected_file = filedialog.askopenfilename(
        title="Select Save File",
        filetypes=[("All files", "*.*")]
    )
    if not selected_file:
        return None  # user cancelled

    # Store both full path + filename
    file_name = os.path.basename(selected_file)
    save_file_var.set(file_name)     # just the name (for UI display)
    file_path.set(selected_file)     # full path (for saving later)

    # Ask for CUSA
    cusa = ask_current_cusa()
    if not cusa:
        return None

    cusa_var.set(cusa.upper())
    game_name_var.set(get_game_name_from_cusa(cusa))
    update_quick_codes()

    # Load data into memory
    global current_save_data
    with open(selected_file, "rb") as f:
        current_save_data = bytearray(f.read())

    return current_save_data
def save_file_handler():
    global current_save_data
    if current_save_data is None:
        messagebox.showwarning("Warning", "No save data loaded!")
        return

    try:


        path = file_path.get()
        game_name=game_name_var.get()
        is_there_checksum(game_name)
        with open(path, "wb") as f:
            f.write(current_save_data)

        messagebox.showinfo("Saved", f"Changes written to:\n{path}")

    except Exception as e:
        messagebox.showerror("Save Error", str(e))

def save_as_file_handler():
    global current_save_data
    if current_save_data is None:
        messagebox.showwarning("Warning", "No save data loaded!")
        return

    try:

        base_name = os.path.basename(file_path.get())
        output_path = filedialog.asksaveasfilename(
            title="Save As",
            initialfile=base_name,
            filetypes=[("All files", "*.*")]
        )
        game_name=game_name_var.get()
        is_there_checksum(game_name)
        with open(output_path, "wb") as f:
            f.write(current_save_data)

        messagebox.showinfo("Saved", f"Changes written to:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Save Error", str(e))
def apply_manual_code():

    manual_code = manual_code_entry.get("1.0", tk.END).strip()
    if not manual_code:
        messagebox.showwarning("Warning", "Please enter a quick code!")
        return
    apply_quick_codes(manual_code)

def save_quick_code():
    quick_code = manual_code_entry.get("1.0", tk.END).strip()
    if not quick_code:
        messagebox.showwarning("Warning", "Please enter a quick code to save!")
        return

    cusa = cusa_var.get()
    if not cusa:
        messagebox.showwarning("Warning", "No CUSA selected!")
        return

    name = simpledialog.askstring("Save Quick Code", "Enter a name for this quick code:")
    if not name:
        return

    author = simpledialog.askstring("Author", "Enter the author of this code:", initialvalue="Unknown")
    if not author:
        author = "Unknown"

    # Load existing codes
    all_codes = load_codes()

    # Find or create the CUSA entry
    cusa_entry = None
    for entry in all_codes:
        if entry.get("CUSA") == cusa:
            cusa_entry = entry
            break
    if not cusa_entry:
        cusa_entry = {"CUSA": cusa, "codes": {}}
        all_codes.append(cusa_entry)

    # Check for duplicate code name
    codes_dict = cusa_entry.setdefault("codes", {})
    if name in codes_dict:
        result = messagebox.askyesno(
            "Duplicate",
            f"A quick code named '{name}' already exists for CUSA {cusa}.\n\nOverwrite it?"
        )
        if not result:
            return

    # Save code with author
    codes_dict[name] = {"code": quick_code, "author": author}

    # Save back to JSON

    json_path =  get_local_path("quickcodes.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"codes": all_codes}, f, indent=4)

    messagebox.showinfo("Saved", f"Quick code '{name}' saved for CUSA {cusa} by {author}.")
    update_quick_codes()



def apply_quick_codes(quick_codes: str):
    global current_save_data  # Make sure we can modify the global
    
    save_path = file_path.get()
    if not save_path:
        print("No save file selected!")
        messagebox.showwarning("Warning", "No save file selected!")
        return
    
    try:
        # Apply quick codes
        qc = QuickCodes(save_path, quick_codes)
        asyncio.run(qc.apply_code())
        asyncio.run(qc.write_file())
        
        # Read the updated file into global current_save_data
        with open(save_path, 'rb') as f:  
            current_save_data = bytearray(f.read()) 
        
        # Apply checksum if needed
        game_name = game_name_var.get()
        is_there_checksum(game_name)
        
        # Write the final data (with checksum)
        with open(save_path, "wb") as f:
            f.write(current_save_data)
            
        messagebox.showinfo("Success", "Quick code applied successfully to current file. Saving not required!")
        
    except Exception as e:
        print(f"Error applying quick codes: {e}")
        messagebox.showerror("Error", f"Failed to apply quick codes: {str(e)}")

def update_quick_codes():
    # Clear old buttons (except the label)
    for widget in codes_frame.winfo_children():
        if widget != quick_label:
            widget.destroy()
    
    current_cusa = cusa_var.get()
    matching_codes = get_codes_for_cusa(current_cusa)
    
    if matching_codes:
        for entry in matching_codes:
            codes_dict = entry.get("codes", {})
            for code_name, code_data in codes_dict.items():
                if isinstance(code_data, dict):
                    code_value = code_data.get("code", "")
                    author = code_data.get("author", "Unknown")
                else:
                    code_value = code_data
                    author = "Unknown"
                
                btn_text = f"{code_name} (by {author})"
                btn = ttk.Button(
                    codes_frame,
                    text=btn_text,
                    command=lambda c=code_value: apply_quick_codes(c)
                )
                btn.pack(fill="x", pady=2)
    else:
        # Use a style for the gray "no codes" label
        style = ttk.Style()
        style.configure("NoCode.TLabel", foreground="gray")
        
        ttk.Label(
            codes_frame,
            text="No codes available for this CUSA",
            style="NoCode.TLabel"
        ).pack(fill="x", pady=5)


        

##DEBUGG
def print_to_terminal(terminal, text):
    terminal.configure(state="normal")
    terminal.insert("end", text + "\n")
    terminal.see("end")  # scroll to the bottom
    terminal.configure(state="disabled")
##

def exit_app():
    root.quit()

def toggle_codes():
    if codes_frame.winfo_ismapped():
        codes_frame.pack_forget()
        toggle_btn.config(text="+ Available Quick Codes")
    else:
        codes_frame.pack(fill="x", padx=5, pady=(0,10))
        toggle_btn.config(text="- Available Quick Codes")
        update_quick_codes()  # populate buttons when shown

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file_handler)
file_menu.add_command(label="Save As", command=save_as_file_handler)
file_menu.add_command(label="Add ID to game list", command=add_id_to_list)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Background menu (or View)
view_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Background", menu=view_menu)

# ===== Update menu =====
update_menu = tk.Menu(menubar, tearoff=0)
update_menu.add_command(label="Update ALL", command=update_all)
update_menu.add_command(label="Update QuickCodes List", command=download_latest_quickcodes)
update_menu.add_command(label="Update Python Script List", command=download_latest_python_scripts)
update_menu.add_command(label="Update Lua Script List", command=download_latest_lua_scripts)
update_menu.add_command(label="Update Built_in_functions", command=update_func)
update_menu.add_command(label="Update Game ID  list", command=download_latest_CUSA)
update_menu.add_command(label="Update Checksum List", command=download_latest_check_scripts)
menubar.add_cascade(label="Update Cheats", menu=update_menu)

# Help menu
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("350x150")
    about_window.resizable(False, False)

    tk.Label(about_window, text="Save Editor v1.1", font=("Segoe UI", 12, "bold")).pack(pady=(10, 0))
    tk.Label(about_window, text="Developed by Alfazari911").pack(pady=(5, 0))
    tk.Label(about_window, text="Github:", font=("Segoe UI", 10)).pack(pady=(10, 0))

    def open_github():
        webbrowser.open("https://github.com/alfizari/PS4-Cheats-Maker")

    link = tk.Label(about_window, text="https://github.com/alfizari/PS4-Cheats-Maker", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda e: open_github())

def help_decrypt():
    messagebox.showinfo("How to Decrypt Saves", "To decrypt PS4 saves, You Could Use Free Tools Such As PS Bot discord or Apollo tool. Paid tools like Save Wizard also work well.\n\nMake sure to back up your saves before modifying them!")

def show_documentation():
    doc_window = tk.Toplevel(root)
    doc_window.title("About")
    doc_window.geometry("350x150")
    doc_window.resizable(False, False)

    tk.Label(doc_window, text="Built in functions", font=("Segoe UI", 12, "bold")).pack(pady=(10, 0))
    tk.Label(doc_window, text="Github:", font=("Segoe UI", 10)).pack(pady=(10, 0))

    def open_github():
        webbrowser.open("https://github.com/alfizari/PS4-Cheats-Maker/blob/main/helpers.py")

    link = tk.Label(doc_window, text="https://github.com/alfizari/PS4-Cheats-Maker/blob/main/helpers.py", fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda e: open_github())



help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
help_menu.add_command(label="How to Decrypt Saves", command=help_decrypt)
help_menu.add_command(label="Documentation", command=show_documentation)
menubar.add_cascade(label="Help", menu=help_menu)
# Apply the menu
root.config(menu=menubar)


# ====== Paned Window (Left/Right split) ======
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=1)

# ----- Left Frame -----
left_frame = tk.Frame(paned, padx=5, pady=5)  # slightly less padding
paned.add(left_frame, width=150)  # make it narrower (was 300)

save_file_var = tk.StringVar(value="No file selected")

tk.Label(left_frame, text="Save File:", anchor="w").pack(fill="x")
tk.Label(left_frame, textvariable=save_file_var, fg="blue").pack(fill="x")

tk.Label(left_frame, text="Game ID:", anchor="w").pack(fill="x", pady=(10, 0))
tk.Label(left_frame, textvariable=cusa_var, fg="green").pack(fill="x")

tk.Label(left_frame, text="Game:", anchor="w").pack(fill="x", pady=(10, 0))
tk.Label(left_frame, textvariable=game_name_var, fg="purple").pack(fill="x")

# ----- Right Frame with Tabs -----
right_frame = tk.Frame(paned, padx=10, pady=10, bg="#f4f4f4")
paned.add(right_frame)

# Create Notebook (tabs container)
tabs = ttk.Notebook(right_frame)
tabs.pack(fill="both", expand=True)


# Quick Codes Tab
quick_codes_tab = ttk.Frame(tabs)
tabs.add(quick_codes_tab, text="Cheats")

# Scripts Tab (main tab)
scripts_tab = ttk.Frame(tabs)
tabs.add(scripts_tab, text="Script Builder")

# --- Sub-tabs inside Scripts ---
sub_tabs = ttk.Notebook(scripts_tab)
sub_tabs.pack(fill="both", expand=True)

# Sub-tab: Custom Scripts

custom_tab = ttk.Frame(sub_tabs)

sub_tabs.add(custom_tab, text="Custom Lua Scripts")

# Main container with left and right sections
main_container = ttk.Frame(custom_tab)
main_container.pack(fill="both", expand=True, padx=5, pady=5)

# Left frame for cheat buttons and controls
left_frame = ttk.Frame(main_container)
left_frame.pack(side="left", fill="y", padx=(0, 5))

# Button frame for the top row buttons
btn_frame = ttk.Frame(left_frame)
btn_frame.pack(pady=(0, 5), anchor="w")

ttk.Button(btn_frame, text="Load Cheats for Current CUSA", command=load_cheat_buttons).pack(pady=2, anchor="w")
ttk.Button(btn_frame, text="Create Lua Cheat (Helper)", command=create_lua_cheat).pack(pady=2, anchor="w")
ttk.Button(btn_frame, text="Save Lua Cheat externally", command=save_lua_cheat).pack(pady=2, anchor="w")
ttk.Button(btn_frame, text="Run Lua Cheat", command=run_lua_script).pack(pady=2, anchor="w")

# Scrollable frame for the cheats that will be loaded dynamically
cheats_canvas = tk.Canvas(left_frame, bg="SystemButtonFace")
cheats_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=cheats_canvas.yview)
cheats_scrollable_frame = ttk.Frame(cheats_canvas)

cheats_scrollable_frame.bind(
    "<Configure>",
    lambda e: cheats_canvas.configure(scrollregion=cheats_canvas.bbox("all"))
)

cheats_canvas.create_window((0, 0), window=cheats_scrollable_frame, anchor="nw")
cheats_canvas.configure(yscrollcommand=cheats_scrollbar.set)

# Cheats canvas (left side, but smaller width)
cheats_canvas.pack(side="left", fill="y", expand=False, pady=5)   # only vertical fill
cheats_scrollbar.pack(side="right", fill="y", pady=5)

# Bind mouse wheel events to the canvas and scrollable frame
cheats_canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
cheats_canvas.bind("<Button-4>", lambda e: cheats_canvas.yview_scroll(-1, "units"))  # Linux
cheats_canvas.bind("<Button-5>", lambda e: cheats_canvas.yview_scroll(1, "units"))   # Linux

# Also bind to the scrollable frame
cheats_scrollable_frame.bind("<MouseWheel>", on_mousewheel)  # Windows
cheats_scrollable_frame.bind("<Button-4>", lambda e: cheats_canvas.yview_scroll(-1, "units"))  # Linux
cheats_scrollable_frame.bind("<Button-5>", lambda e: cheats_canvas.yview_scroll(1, "units"))   # Linux

# Reference to the scrollable frame for the load function
cheats_frame = cheats_scrollable_frame

# Add Cheat to List button
ttk.Button(btn_frame, text="Add Cheat to List", command=add_cheat_to_list).pack(pady=2, anchor="w")

# Right frame for Lua textbox (takes most of the space)
right_frame = ttk.Frame(main_container)
right_frame.pack(side="right", fill="both", expand=True)

# Textbox for user Lua scripts
lua_text = scrolledtext.ScrolledText(right_frame, height=20, wrap=tk.WORD)
lua_text.pack(fill="both", expand=True)

# ====== Modified Quick Codes Tab ======

# Create the main frame structure
top_frame = ttk.Frame(quick_codes_tab)
top_frame.pack(fill="x", pady=(0, 10))

# Quick Codes toggle button
toggle_btn = ttk.Button(quick_codes_tab, text="+ Available Quick Codes", command=toggle_codes)
toggle_btn.pack(fill="x", pady=(0, 5))

# Codes frame (initially hidden)
codes_frame = ttk.Frame(quick_codes_tab)
quick_label = ttk.Label(codes_frame, text="Quick Codes", font=("Segoe UI", 10, "bold"))
quick_label.pack(fill="x", pady=(0,5))
# Don't pack it initially - toggle_codes() will handle this

# Manual Quick Code Entry Section
manual_frame = ttk.Frame(quick_codes_tab)
manual_frame.pack(fill="x", pady=(0, 10))

tk.Label(manual_frame, text="Manual Quick Code:", bg="#fff5f5", anchor="w").pack(fill="x")

# Text entry for manual code
manual_code_entry = tk.Text(manual_frame, height=3, wrap=tk.WORD)
manual_code_entry.pack(fill="x", pady=(2, 5))

# Apply manual code button
apply_manual_btn = ttk.Button(manual_frame, text="Apply Manual Code",
                           command=lambda: apply_manual_code())
apply_manual_btn.pack(fill="x")

# Save manual code button
save_manual_btn = ttk.Button(manual_frame, text="Save Code To List",
                            command=lambda: save_quick_code())
save_manual_btn.pack(fill="x", pady=(5, 0))
# ====== NEW: Scripts Section in Quick Codes Tab ======

# Scripts section frame
scripts_section = ttk.Frame(quick_codes_tab)
scripts_section.pack(fill="both", expand=True, pady=(10, 0))

# Python Scripts subsection
python_section = ttk.LabelFrame(scripts_section, text="Python Scripts")
python_section.pack(fill="x", pady=(0, 5))

# Python load button and frame container
python_container = ttk.Frame(python_section)
python_container.pack(fill="x", padx=5, pady=5)

# Load Python Scripts button
load_python_btn = ttk.Button(python_container, text="📁 Load Python Scripts", 
                            command=lambda: load_python_scripts())
load_python_btn.pack(fill="x", pady=(0, 5))

# Frame to hold python script buttons in quick codes tab
python_quick_frame = ttk.Frame(python_container)
python_quick_frame.pack(fill="x")

# Lua Scripts subsection
lua_section = ttk.LabelFrame(scripts_section, text="Lua Scripts")
lua_section.pack(fill="x", pady=(5, 0))

# Lua load button and frame container
lua_container = ttk.Frame(lua_section)
lua_container.pack(fill="x", padx=5, pady=5)

# Load Lua Scripts button
load_lua_btn = ttk.Button(lua_container, text="📁 Load Lua Scripts", 
                         command=lambda: load_cheat_buttons())
load_lua_btn.pack(fill="x", pady=(0, 5))

# Frame to hold lua script buttons in quick codes tab
lua_quick_frame = ttk.Frame(lua_container)
lua_quick_frame.pack(fill="x")



# PYTHON BUILT-IN FUNCTIONS
python_tab = ttk.Frame(sub_tabs)
sub_tabs.add(python_tab, text="Python Editor")

# Configure grid (2 columns: left = sidebar, right = editor)
python_tab.columnconfigure(0, weight=0)  # Sidebar stays compact
python_tab.columnconfigure(1, weight=1)  # Editor expands
python_tab.rowconfigure(0, weight=1)     # Make everything stretch vertically

# -------------------------------
# Left sidebar (scripts manager)
# -------------------------------
left_python_frame = ttk.Frame(python_tab)
left_python_frame.grid(row=0, column=0, sticky="ns", padx=(5, 5), pady=5)

# Sidebar buttons
ttk.Button(left_python_frame, text="Load Scripts", command=load_python_scripts).pack(pady=2, anchor="w")
ttk.Button(left_python_frame, text="Create Script (Helper)", command=create_new_script).pack(pady=2, anchor="w")
ttk.Button(left_python_frame, text="Add Script to list", command=save_script).pack(pady=2, anchor="w")
ttk.Button(left_python_frame, text="Run Script", command=lambda: run_python_script()).pack(pady=2, anchor="w")

# Script list frame
python_scripts_frame = ttk.Frame(left_python_frame)
python_scripts_frame.pack(fill="y", expand=True)

# -------------------------------
# Right side (editor + run button)
# -------------------------------
editor_frame = ttk.Frame(python_tab)
editor_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
editor_frame.rowconfigure(0, weight=1)
editor_frame.columnconfigure(0, weight=1)

# Scrollable editor
python_text = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD)
python_text.grid(row=0, column=0, sticky="nsew")

# Run button at bottom
def run_python_code():
    try:
        code = python_text.get("1.0", tk.END)
        globals_dict = {
            "__builtins__": __builtins__,
            "save_data": current_save_data,
            "current_cusa": cusa_var.get(),
        }
        globals_dict.update(get_helper_globals())

        # Redirect stdout/stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = TextRedirector(python_terminal)

        exec(code, globals_dict)

    except Exception as e:
        messagebox.showerror("Python Error", str(e))
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


#debugg terminals
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)
        self.widget.configure(state="disabled")
    def flush(self):
        pass

# Row configuration
right_frame.rowconfigure(0, weight=1)  # any editor or space above
right_frame.rowconfigure(1, weight=0)  # terminal fixed height
right_frame.rowconfigure(2, weight=0)  # button fixed height
right_frame.columnconfigure(0, weight=1)

# Python terminal (output box, read-only)
python_terminal = scrolledtext.ScrolledText(
    editor_frame,
    height=10,
    wrap=tk.WORD,
    state="disabled",
    bg="black",
    fg="lime"
)
python_terminal.grid(row=1, column=0, sticky="nsew", pady=(5, 0))  # <-- row 1

# Run button at bottom
ttk.Button(editor_frame, text="Run Python", command=run_python_code)\
   .grid(row=2, column=0, sticky="ew", pady=5)  # <-- row 2

# Row configuration
editor_frame.rowconfigure(0, weight=1)  # editor expands
editor_frame.rowconfigure(1, weight=0)  # terminal fixed height
editor_frame.rowconfigure(2, weight=0)  # run button fixed height
editor_frame.columnconfigure(0, weight=1)


# Initialize quick codes for the default CUSA
update_quick_codes()
load_cusa_game_mapping()
load_built_in_functions(jsons)
run_python_script_auto()

#DARK MODE
# Dark mode palette
DARK_MODE = {
    "bg": "#2e2e2e",          # general background
    "fg": "#ffffff",          # text color
    "button_bg": "#3e3e3e",   # button background
    "button_fg": "#ffffff",   # button text
    "entry_bg": "#4e4e4e",    # entry/text background
    "entry_fg": "#ffffff",    # entry/text foreground
    "text_bg": "#1e1e1e",     # ScrolledText background
    "text_fg": "#00ff00",     # terminal text
}


def apply_dark_mode(widget):
    try:
        if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button) or isinstance(widget, tk.Entry) or isinstance(widget, tk.Text) or isinstance(widget, scrolledtext.ScrolledText):
            # Apply colors based on type
            if isinstance(widget, tk.Frame):
                widget.configure(bg=DARK_MODE["bg"])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=DARK_MODE["bg"], fg=DARK_MODE["fg"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=DARK_MODE["button_bg"], fg=DARK_MODE["button_fg"])
            elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
                widget.configure(bg=DARK_MODE["entry_bg"], fg=DARK_MODE["entry_fg"], insertbackground=DARK_MODE["entry_fg"])
            elif isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(bg=DARK_MODE["text_bg"], fg=DARK_MODE["text_fg"], insertbackground=DARK_MODE["text_fg"])
    except tk.TclError:
        pass  # ignore widgets that don't support bg/fg

    # Recurse into children
    for child in widget.winfo_children():
        apply_dark_mode(child)

def apply_ttk_dark_style():
    style = ttk.Style()
    style.theme_use('clam')  # safe theme for dark customization
    style.configure("TFrame", background=DARK_MODE["bg"])
    style.configure("TLabel", background=DARK_MODE["bg"], foreground=DARK_MODE["fg"])
    style.configure("TButton", background=DARK_MODE["button_bg"], foreground=DARK_MODE["button_fg"])
    style.configure("TNotebook", background=DARK_MODE["bg"])
    style.configure("TNotebook.Tab", background=DARK_MODE["button_bg"], foreground=DARK_MODE["button_fg"])
def toggle_dark_mode():
    if root.cget("bg") == DARK_MODE["bg"]:
        root.configure(bg="SystemButtonFace")
        # optionally reload default ttk theme
    else:
        apply_ttk_dark_style()
        apply_dark_mode(root)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)



# Run app

root.mainloop()
