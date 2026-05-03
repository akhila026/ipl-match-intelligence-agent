import datetime
from google.adk.agents import Agent

def get_current_time(city: str) -> dict:
    """
    Get the current time for a given city.
    
    Args:
        city (str): The name of the city to get the time for. Supported cities are New York, London, and Tokyo.
        
    Returns:
        dict: A dictionary containing 'status' ('success' or 'error'). If successful, contains 'time' data. If error, contains 'error_message'.
    """
    # Mock data for demonstration purposes
    mock_time_data = {
        "New York": "10:00 AM",
        "London": "3:00 PM",
        "Tokyo": "12:00 AM (Next Day)"
    }
    
    # In a real tool, we might use the datetime module, but here we use mock data
    # current_time = datetime.datetime.now()
    
    if city in mock_time_data:
        return {"status": "success", "time": mock_time_data[city]}
    return {"status": "error", "error_message": f"Time data not available for {city}"}

def get_weather(city: str) -> dict:
    """
    Get the current weather condition and temperature for a given city.
    
    Args:
        city (str): The name of the city to get weather for. Supported cities are New York, London, and Tokyo.
        
    Returns:
        dict: A dictionary containing 'status' ('success' or 'error'). If successful, contains 'temperature' and 'condition'. If error, contains 'error_message'.
    """
    mock_weather_data = {
        "New York": {"temperature": "72°F", "condition": "Sunny"},
        "London": {"temperature": "60°F", "condition": "Cloudy"},
        "Tokyo": {"temperature": "68°F", "condition": "Rainy"}
    }
    
    if city in mock_weather_data:
        data = mock_weather_data[city]
        return {
            "status": "success", 
            "temperature": data["temperature"], 
            "condition": data["condition"]
        }
    return {"status": "error", "error_message": f"Weather data not available for {city}"}

root_agent = Agent(
    model='gemini-flash-latest',
    name='weather_time_agent',
    description='A helpful agent that provides weather and time information for selected cities.',
    instruction='You are a helpful assistant. Use the provided tools to answer time and weather questions concisely. Only answer questions regarding supported cities.',
    tools=[get_current_time, get_weather]
)
