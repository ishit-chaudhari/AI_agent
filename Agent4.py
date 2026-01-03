# Info: This agent extracts budget data from PNG/JPG images of Excel files and saves to CSV.

from google.adk.agents.llm_agent import Agent
import csv
import os
import json
from datetime import datetime


def save_to_csv(data_json: str) -> dict:
    """
    Saves tabular data to a CSV file in the budget folder.
    
    Args:
        data_json: A JSON string representing a 2D array of table data.
                   First row should be headers, subsequent rows are data.
                   Example: '[["Item", "Quantity", "Price"], ["Filet Mignon", "2", "$98.00"]]'
    
    Returns:
        A dictionary with status and the path to the saved file.
    """
    # Parse the JSON string to get the data
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": f"Failed to parse JSON data: {str(e)}"
        }
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "budget")
    os.makedirs(output_dir, exist_ok=True)
    
    # Always generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"budget_{timestamp}.csv"
    
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        
        return {
            "status": "success",
            "message": f"CSV file saved successfully.",
            "filepath": filepath,
            "rows_written": len(data)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save CSV: {str(e)}"
        }


root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Extracts budget data from images of Excel spreadsheets and saves to CSV.",
    instruction="""You are a helpful assistant that extracts budget data from images of Excel spreadsheets or receipts.

When the user uploads an image of a spreadsheet, receipt, or budget table:
1. Carefully analyze the image to identify all rows and columns of data.
2. Extract ALL the data you can see, preserving the table structure.
3. Use the 'save_to_csv' tool to save the extracted data.
   - Pass the data as a JSON string representing a 2D array.
   - First row should be headers.
   - Example: '[["Item", "Quantity", "Price"], ["Filet Mignon", "2", "$98.00"], ["Rib Eye", "1", "$52.00"]]'

Be thorough and accurate. If you cannot read some text clearly, make your best guess.
After saving, tell the user where the file was saved.""",
    tools=[save_to_csv],
)
