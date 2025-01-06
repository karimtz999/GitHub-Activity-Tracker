import sys
import urllib.request
import json

# Function to display the ASCII logo/banner
def display_logo():
    logo = r"""
 ________  __    __  ________        _______   __    __       
|        \|  \  |  \|        \      |       \ |  \  |  \      
 \$$$$$$$$| $$  | $$| $$$$$$$$      | $$$$$$$\| $$  | $$      
   | $$   | $$__| $$| $$__          | $$__| $$ \$$\/  $$      
   | $$   | $$    $$| $$  \         | $$    $$  >$$  $$       
   | $$   | $$$$$$$$| $$$$$         | $$$$$$$\ /  $$$$\       
   | $$   | $$  | $$| $$_____       | $$  | $$|  $$ \$$\      
   | $$   | $$  | $$| $$     \      | $$  | $$| $$  | $$      
    \$$    \$$   \$$ \$$$$$$$$       \$$   \$$ \$$   \$$      
                                                              
                                                              
                                                              
    """
    print(logo)
    print("Welcome to GitHub Activity Tracker!\n")

# Function to fetch data from GitHub API
def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read())
                return data
    except urllib.error.HTTPError as e:
        print(f"Error: Unable to fetch data for {username}. HTTP Error {e.code}.")
    except urllib.error.URLError as e:
        print(f"Error: Network error occurred. Details: {e.reason}.")
    return None

# Function to display user activity
def display_activity(events):
    if not events:
        print("No recent activity found.")
        return

    print("\nRecent GitHub Activity:")
    for event in events[:10]:  # Limit to 10 events
        if event["type"] == "PushEvent":
            repo_name = event["repo"]["name"]
            commits = len(event["payload"]["commits"])
            print(f"- Pushed {commits} commit(s) to {repo_name}")
        elif event["type"] == "IssuesEvent":
            action = event["payload"]["action"]
            repo_name = event["repo"]["name"]
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event["type"] == "WatchEvent":
            repo_name = event["repo"]["name"]
            print(f"- Starred {repo_name}")
        else:
            print(f"- {event['type']} in {event['repo']['name']}")

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        return

    display_logo()  # Display logo at the start
    username = sys.argv[1]
    print(f"Fetching recent activity for GitHub user: {username}...\n")
    events = fetch_github_activity(username)
    display_activity(events)

if __name__ == "__main__":
    main()
