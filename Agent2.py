# Import the base Agent class from the Google ADK library.
from google.adk.agents import Agent
# Import the ZoneInfo class for handling time zones (though not used in final functions).
from zoneinfo import ZoneInfo
# Import the datetime module for date and time operations (though not used in final functions).
import datetime
# Import the requests library for making HTTP requests to external APIs.
import requests
# Define a function named 'current_time' that returns the current time in a specified city.
def current_time(city: str):
    """Returns the current time in a specified city.""" # Docstring: Describes the function's purpose.
    # Construct the API URL for wttr.in, requesting JSON format data for the given city.
    url = f"https://wttr.in/{city}?format=j1"
    # Start a try block to handle potential network or parsing errors.
    try:
        # Make a GET request to the URL and parse the response body as JSON.
        data = requests.get(url).json()
        # Extract the local observation date and time from the nested JSON structure.
        local_time = data['current_condition'][0]['localObsDateTime']
        # Return a success dictionary with the formatted time report.
        return {"status": "success", "report": f"The current time in {city} is {local_time}."}
    # Catch any exceptions (e.g., network issues, invalid city, JSON parsing errors) that occurred in the try block.
    except Exception as e:
        # Return an error dictionary with the details of the exception.
        return {"status": "error", "report": f"Could not get time for {city}: {e}"}

# Define a function named 'current_weather' that returns the current weather data in a specified city.
def current_weather(city: str):
    """Returns the current weather in a specified city.""" # Docstring: Describes the function's purpose.
    # Construct the API URL for wttr.in, requesting JSON format data for the given city.
    url = f"https://wttr.in/{city}?format=j1"
    # Make a GET request to the URL and parse the response body as JSON.
    data = requests.get(url).json()
    # Return the raw JSON data containing the weather information.
    return data

# Instantiate the root agent object using the Agent class.
root_agent = Agent(
    # Assign a unique name to the agent.
    name="weather_time_agent",
    # Specify the underlying large language model to be used by the agent.
    model="gemini-2.0-flash",
    # Start the definition of the agent's description.
    description=(
        # A brief description of the agent's capabilities.
        "Agent to answer questions about the time and weather in a city."
    ),
    # Start the definition of the agent's specific instructions.
    instruction=(
        # Detailed instructions guiding the agent's behavior.
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    # Provide a list of functions (tools) that the agent can utilize.
    tools=[current_time, current_weather],
)

# import os # Commented out: Import statement for the 'os' module (system operations).

# if os.path.exists("/Users/ishitchaudhari/Desktop/agent/my_agent/agent2.py"): # Commented out: Check if a specific file path exists.
#     print("file exists") # Commented out: Print message if the file is found.
