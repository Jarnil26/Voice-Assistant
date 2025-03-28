import os
import subprocess
import psutil


def open_application(app_name):
    print(f"Opening {app_name}...")
    
    # Define a dictionary to map application names to their respective paths or commands
    app_paths = {
        "notepad": "notepad.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "spotify": "C:\\Users\\Dell\\AppData\\Roaming\\Spotify\\Spotify.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "whatsapp": "C:\\Users\\Dell\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
        "vscode": "C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        # Add more applications and their paths as needed
    }
    
    # Check if the application is in the dictionary
    if app_name.lower() in app_paths:
        app_path = app_paths[app_name.lower()]
        try:
            subprocess.Popen(app_path)
            print(f"{app_name} opened successfully.")
        except Exception as e:
            print(f"Failed to open {app_name}. Error: {e}")
    else:
        print(f"Application '{app_name}' not found. Please check the application name and try again.")
        
def close_application(app_name):
    # Append .exe to the app name if not already present
    if not app_name.lower().endswith('.exe'):
        app_name += '.exe'

    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == app_name.lower():
                proc.terminate()
                proc.wait()
                #print(f"Closed: {proc.info['name']}")
                return
        print(f"No running process found for: {app_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example usage
    app_name = input("Enter the name of the application to open: ").strip()
    open_application(app_name)