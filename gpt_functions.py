import os
import shutil
import subprocess

from helpers import yesno, safepath

# Implementation of the functions given to ChatGPT

def write_file(filename, content):
    filename = safepath(filename)

    print(f"FUNCTION: Writing to file code/{filename}...")

    # force newline in the end
    if content[-1] != "\n":
        content = content + "\n"

    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(f"code/{filename}")
    os.makedirs(parent_dir, exist_ok=True)

    with open(f"code/{filename}", "w") as f:
        f.write(content)
    return f"File {filename} written successfully"

def append_file(filename, content):
    filename = safepath(filename)

    print(f"FUNCTION: Appending to file code/{filename}...")

    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(f"code/{filename}")
    os.makedirs(parent_dir, exist_ok=True)

    with open(f"code/{filename}", "a") as f:
        f.write(content)
    return f"File {filename} appended successfully"

def read_file(filename):
    filename = safepath(filename)

    print(f"FUNCTION: Reading file code/{filename}...")
    if not os.path.exists(f"code/{filename}"):
        print(f"File {filename} does not exist")
        return f"File {filename} does not exist"
    with open(f"code/{filename}", "r") as f:
        content = f.read()
    return f"The contents of '{filename}':\n{content}"

def create_dir(directory):
    directory = safepath(directory)

    print(f"FUNCTION: Creating directory code/{directory}")
    if os.path.exists(f"code/{directory}/"):
        return "ERROR: Directory exists"
    os.mkdir(f"code/{directory}")
    return f"Directory {directory} created!"

def move_file(source, destination):
    source = safepath(source)
    destination = safepath(destination)

    print(f"FUNCTION: Move code/{source} to code/{destination}...")

    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(f"code/{destination}")
    os.makedirs(parent_dir, exist_ok=True)

    try:
        shutil.move(f"code/{source}", f"code/{destination}")
    except:
        if os.path.isdir(f"code/{source}") and os.path.isdir(f"code/{destination}"):
            return "ERROR: Destination folder already exists."
        return "Unable to move file."

    return f"Moved {source} to {destination}"

def copy_file(source, destination):
    source = safepath(source)
    destination = safepath(destination)

    print(f"FUNCTION: Copy code/{source} to code/{destination}...")

    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(f"code/{destination}")
    os.makedirs(parent_dir, exist_ok=True)

    try:
        shutil.copy(f"code/{source}", f"code/{destination}")
    except:
        if os.path.isdir(f"code/{source}") and os.path.isdir(f"code/{destination}"):
            return "ERROR: Destination folder already exists."
        return "Unable to copy file."

    return f"File {source} copied to {destination}"

def delete_file(filename):
    filename = safepath(filename)

    print(f"FUNCTION: Deleting file code/{filename}")
    path = f"code/{filename}"

    if not os.path.exists(path):
        print(f"File {filename} does not exist")
        return f"ERROR: File {filename} does not exist"

    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except:
        return "ERROR: Unable to remove file."

    return f"File {filename} successfully deleted"

def list_files(list = "", print_output = True):
    files_by_depth = {}
    directory = "code/"

    for root, _, filenames in os.walk(directory):
        depth = str(root[len(directory):].count(os.sep))

        for filename in filenames:
            file_path = os.path.join(root, filename)
            if depth not in files_by_depth:
                files_by_depth[depth] = []
            files_by_depth[depth].append(file_path)

    files = []
    counter = 0
    max_files = 20
    for level in files_by_depth.values():
        for filename in level:
            counter += 1
            if counter > max_files:
                break
            files.append(filename)

    # Remove "code/" from the beginning of file paths
    files = [file_path.replace("code/", "", 1) for file_path in files]

    if print_output: print(f"FUNCTION: Files in code/ directory:\n{files}")
    return f"List of files in the project:\n{files}"

def ask_clarification(question):
    return input(f"## ChatGPT Asks a Question ##\n```{question}```\nAnswer: ")

def run_cmd(base_dir, command, reason):
    base_dir = safepath(base_dir)
    print("FUNCTION: Run a command")
    print("## ChatGPT wants to run a command! ##")

    command = "cd code/" + base_dir.strip("/") + "; " + command
    print(f"Command: `{command}`")
    print(f"Reason: `{reason}`")

    answer = yesno(
        "Do you want to run this command?",
        ["YES", "NO"]
    )

    if answer != "YES":
        return "I don't want you to run that command"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr

    return_value = "Result from command (last 245 chars):\n" + output[-245:]

    print(return_value)

    return return_value

def project_finished(finished):
    return "PROJECT_FINISHED"

# Function definitions for ChatGPT

definitions = [
    {
        "name": "list_files",
        "description": "List the files in the current project",
        "parameters": {
            "type": "object",
            "properties": {
                "list": {
                    "type": "string",
                    "description": "Set always to 'list'",
                },
            },
            "required": ["list"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file with given name. Returns the file contents as string.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to read",
                },
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file with given name. Existing files will be overwritten. Parent directories will be created if they don't exist",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file",
                },
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "append_file",
        "description": "Write content to the end of a file with given name",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write into the file",
                },
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "move_file",
        "description": "Move a file from one place to another. Parent directories will be created if they don't exist",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "The source file to move",
                },
                "destination": {
                    "type": "string",
                    "description": "The new filename / filepath",
                },
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "create_dir",
        "description": "Create a directory with given name",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Name of the directory to create",
                },
            },
            "required": ["directory"],
        },
    },
    {
        "name": "copy_file",
        "description": "Copy a file from one place to another. Parent directories will be created if they don't exist",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "The source file to copy",
                },
                "destination": {
                    "type": "string",
                    "description": "The new filename / filepath",
                },
            },
            "required": ["source", "destination"],
        },
    },
    {
        "name": "delete_file",
        "description": "Deletes a file with given name",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The filename to delete",
                },
            },
            "required": ["filename"],
        },
    },
    {
        "name": "ask_clarification",
        "description": "Ask the user a clarifying question about the project. Returns the answer by the user as string",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user",
                },
            },
            "required": ["question"],
        },
    },
    {
        "name": "project_finished",
        "description": "Call this function when the project is finished",
        "parameters": {
            "type": "object",
            "properties": {
                "finished": {
                    "type": "string",
                    "description": "Set this to 'finished' always",
                },
            },
            "required": ["finished"],
        },
    },
    {
        "name": "run_cmd",
        "description": "Run a terminal command. Returns the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "base_dir": {
                    "type": "string",
                    "description": "The directory to change into before running command",
                },
                "command": {
                    "type": "string",
                    "description": "The command to run",
                },
                "reason": {
                    "type": "string",
                    "description": "A reason for why the command should be run",
                },
            },
            "required": ["base_dir", "command", "reason"],
        },
    },
]
