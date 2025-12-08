import os
import shutil

# ==================================
#          FILE MANAGER
# ==================================

def create_file(path, content=""):
    """
    Create a new file with optional content.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File created: {path}"
    except Exception as e:
        return f"Error creating file: {e}"


def read_file(path):
    """
    Read and return file content.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File does not exist."
    except Exception as e:
        return f"Error reading file: {e}"


def delete_file(path):
    """
    Delete a file from the system.
    """
    try:
        os.remove(path)
        return f"File deleted: {path}"
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error deleting file: {e}"


def rename_file(old_path, new_path):
    """
    Rename a file or folder.
    """
    try:
        os.rename(old_path, new_path)
        return f"Renamed to: {new_path}"
    except FileNotFoundError:
        return "Error: File or folder not found."
    except Exception as e:
        return f"Error renaming: {e}"


def create_folder(path):
    """
    Create a new folder.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder created: {path}"
    except Exception as e:
        return f"Error creating folder: {e}"


def delete_folder(path):
    """
    Delete a folder and its contents.
    """
    try:
        shutil.rmtree(path)
        return f"Folder deleted: {path}"
    except FileNotFoundError:
        return "Error: Folder does not exist."
    except Exception as e:
        return f"Error deleting folder: {e}"


def open_folder(path):
    """
    Open a folder in Windows File Explorer.
    """
    try:
        os.startfile(path)  # Works only on Windows
        return f"Opening folder: {path}"
    except Exception as e:
        return f"Error opening folder: {e}"


def search_file(directory, filename):
    """
    Search for a file recursively inside a directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        return "File not found."
    except Exception as e:
        return f"Error searching: {e}"
