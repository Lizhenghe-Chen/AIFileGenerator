from typing import *
from datetime import datetime, timedelta

# Implementation of the search tool
def search_impl(query: str) -> List[Dict[str, Any]]:
    """
    Uses a search engine to perform a query. This is a placeholder implementation.
    Replace with actual API calls to a search engine like Bing or Google.
    """
    return [
        {
            "title": "Test Title 1",
            "url": "https://example.com/1",
            "description": "Test description 1",
        }
    ]

def search(arguments: Dict[str, Any]) -> Any:
    query = arguments["query"]
    result = search_impl(query)
    return {"result": result}

# Implementation of the crawl tool
def crawl_impl(url: str) -> str:
    """
    Fetches content from a given URL. This is a placeholder implementation.
    Replace with actual web scraping logic.
    """
    return f"Test content for URL: {url}"

def crawl(arguments: dict) -> dict:
    url = arguments["url"]
    content = crawl_impl(url)
    return {"content": content}

# Implementation of the weather query tool
def weather_query_impl(city: str) -> Dict[str, Any]:
    """
    Fetches weather information for a given city. This is a placeholder implementation.
    Replace with actual API calls to a weather service.
    """
    return {"city": city, "weather": "Storm", "temperature": "25°C"}

def weather_query(arguments: Dict[str, Any]) -> Any:
    city = arguments["city"]
    result = weather_query_impl(city)
    return {"result": result}

# Implementation of the drone data query tool
def drone_data_query_impl(query: str) -> List[Dict[str, Any]]:
    """
    Fetches drone-related data based on a query. This is a placeholder implementation.
    Replace with actual logic to fetch drone data.
    """
    return [{"drone_id": 101, "status": "Destroyed", "location": "Area 51"}]

def drone_data_query(arguments: Dict[str, Any]) -> Any:
    query = arguments["query"]
    result = drone_data_query_impl(query)
    return {"result": result}

# Updated implementation of the set alarm tool with current time consideration
def set_alarm_impl(time: str, message: str, date: Optional[str] = None, repeat: Optional[str] = "none", timezone: Optional[str] = None) -> str:
    """
    Sets an alarm for a specific time with a message, date, repeat frequency, and timezone.
    Considers the current time and adjusts the alarm date if necessary.
    """
    current_time = datetime.now()

    # Parse the provided time and date
    alarm_time = datetime.strptime(time, "%H:%M").time()
    alarm_date = datetime.strptime(date, "%Y-%m-%d").date() if date else current_time.date()

    # Combine date and time into a datetime object
    alarm_datetime = datetime.combine(alarm_date, alarm_time)

    # If the alarm time is in the past, adjust the date
    if alarm_datetime < current_time:
        alarm_datetime += timedelta(days=1)

    # Format the alarm details
    alarm_details = f"Alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M')}"
    if repeat and repeat != "none":
        alarm_details += f" (repeats {repeat})"
    if timezone:
        alarm_details += f" in timezone {timezone}"
    alarm_details += f" with message: '{message}'"
    return alarm_details

def set_alarm(arguments: Dict[str, Any]) -> Any:
    time = arguments["time"]
    message = arguments["message"]
    date = arguments.get("date")
    repeat = arguments.get("repeat", "none")
    timezone = arguments.get("timezone")
    result = set_alarm_impl(time, message, date, repeat, timezone)
    return {"result": result}

# Mapping of tool names to their corresponding functions
tool_map = {
    "search": search,
    "crawl": crawl,
    "weather_query": weather_query,
    "drone_data_query": drone_data_query,
    "set_alarm": set_alarm,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Uses a search engine to find information on the internet.",
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The content to search for, extracted from the user's query."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crawl",
            "description": "Fetches content from a given URL.",
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website to fetch content from."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather_query",
            "description": "Fetches weather information for a specified city.",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to query weather information for."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "drone_data_query",
            "description": "Fetches drone-related data based on a query.",
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query conditions for fetching drone data."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_alarm",
            "description": "Sets an alarm for a specific time with a custom message, date, repeat frequency, and timezone.",
            "parameters": {
                "type": "object",
                "required": ["time", "message"],
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "The time to set the alarm for, in HH:MM format."
                    },
                    "message": {
                        "type": "string",
                        "description": "The message to display when the alarm goes off."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date to set the alarm for, in YYYY-MM-DD format. Defaults to today.",
                        "nullable": True
                    },
                    "repeat": {
                        "type": "string",
                        "description": "The repeat frequency of the alarm. Options are 'none', 'daily', 'weekly'. Defaults to 'none'.",
                        "nullable": True
                    },
                    "timezone": {
                        "type": "string",
                        "description": "The timezone for the alarm. Defaults to the system timezone.",
                        "nullable": True
                    }
                }
            }
        }
    }
]
