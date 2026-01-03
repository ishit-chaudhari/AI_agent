#info: in this agent we will be using the tools to add comments and dostrings in my python code. 

from google.adk.agents import Agent
import os
import importlib

def read_code(filepath: str):
    """
    Reads the content of a file from the given filepath.
    
    Args:
        filepath: The absolute path to the file to read.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    else:
        try:
            with open(filepath, "r") as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Failed to read file: {filepath}")
        
def lookup_library(library_name: str):
    """
    Checks if a python library is installed.
    
    Args:
        library_name: The name of the library to check.
    """
    try:
        importlib.import_module(library_name)
        return True
    except ImportError:
        return False


def write_documentation(filepath: str, content: str):
    """
    Writes content to a file.
    
    Args:
        filepath: The absolute path to the file.
        content: The content to write to the file.
    """
    try:
        with open(filepath, "w") as file:
            file.write(content)
        return True
    except Exception as e:
        raise Exception(f"Failed to write documentation: {filepath}")



def find_file(filename: str, search_path: str = ".") -> str:
    """
    Recursively searches for a file with the given name in the specified directory.
    
    Args:
        filename: The name of the file to search for (e.g., "agent2.py").
        search_path: The directory to start searching from. Defaults to current directory.
        
    Returns:
        The absolute path to the file if found, or a message indicating it was not found.
    """
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return "File not found."

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="You are a python developer. Your task is to add comments and docstrings to the python code.",
    instruction="Role: Act like commenting and docstring writer for python developer. Task: your task is to add comments and docstrings to the python code. Rules: 1. Use the tools to add comments and docstrings to the python code. 2. do not change the python code. only add comments and docstrings. 3. If you cannot find a file, use the find_file tool to locate it. 4. When using write_documentation, provide the full updated code as the content.",
    tools=[read_code, lookup_library, write_documentation, find_file],
)

#can you add comments in other files outside this folder if I provide you the location.
#add comment and doctoring foe each and every line. location: /Users/ishitchaudhari/Desktop/agent/multi_tool_agent/agent2.py
