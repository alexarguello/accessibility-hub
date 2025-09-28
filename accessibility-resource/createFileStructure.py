import os
import re

# Path to the Markdown file containing the TOC
MARKDOWN_FILE = "/plan.md"

# Root directory where folders will be created (change as needed)
ROOT_DIR = "./generated_structure"

# Regex to match TOC lines with folder/file references
TOC_LINK_REGEX = re.compile(r"\*\(->\s*([^)]+)\)")

def clean_path(path):
    """
    Cleans up the extracted path by removing backticks, stray quotes, and whitespace.
    """
    return path.replace('`', '').replace('"', '').replace("'", '').strip()

def parse_toc_lines(lines):
    """
    Parses lines from the Markdown TOC and extracts folder/file paths.
    Returns a set of folder paths to create.
    """
    folders = set()
    for line in lines:
        match = TOC_LINK_REGEX.search(line)
        if match:
            raw_path = match.group(1)
            path = clean_path(raw_path)
            # Only keep the folder part (ignore .md files for folder creation)
            if path.endswith('/'):
                folders.add(path)
            elif '/' in path:
                folder = os.path.dirname(path)
                if folder:
                    # Ensure trailing slash for folder
                    folders.add(folder + '/')
    # Always add parent folders recursively
    all_folders = set()
    for folder in folders:
        parts = folder.strip('/').split('/')
        for i in range(1, len(parts)+1):
            parent = '/'.join(parts[:i]) + '/'
            all_folders.add(parent)
    return all_folders

def create_folders(folders, root_dir):
    """
    Creates the folders under the specified root directory.
    """
    print("Folders to create:")
    for folder in sorted(folders):
        print(f"  {folder}")
    for folder in sorted(folders):
        folder_path = os.path.join(root_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created: {folder_path}")

def main():
    # Read the Markdown file
    with open(MARKDOWN_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Extract folder paths from TOC
    folders = parse_toc_lines(lines)

    # Always create the root directory
    os.makedirs(ROOT_DIR, exist_ok=True)

    # Create the folders
    create_folders(folders, ROOT_DIR)

    print("Folder structure generation complete.")

if __name__ == "__main__":
    main()
