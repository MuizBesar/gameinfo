import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser

def get_released_games(api_key, release_date):
    url = f"https://api.rawg.io/api/games?key={api_key}&dates={release_date},{release_date}&ordering=released&page_size=20"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        games = data["results"]
        
        game_info = ""
        
        if games:
            for game in games:
                title = game["name"]
                release_date = game["released"]
                
                platforms = [platform["platform"]["name"] for platform in game["platforms"]]
                platforms = [platform for platform in platforms if platform not in ["Android", "iOS"]]
                
                if not platforms:
                    continue
                
                game_info += f"Title: {title}\n"
                game_info += f"Release Date: {release_date}\n"
                game_info += f"Platforms: {', '.join(platforms)}\n"
                game_info += "----------------------\n"
        else:
            game_info = "No games found."
        
        game_text.delete(1.0, tk.END)
        game_text.insert(tk.END, game_info)
    else:
        messagebox.showerror("Error", "Failed to retrieve released games.")

def fetch_games():
    api_key = api_key_entry.get()
    release_date = release_date_entry.get()
    
    get_released_games(api_key, release_date)

def open_rawg(event):
    webbrowser.open("https://rawg.io/")

# Create the main window
window = tk.Tk()
window.title("Released Video Games")

# Create labels and entry fields
api_key_label = tk.Label(window, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(window)
api_key_entry.pack()

release_date_label = tk.Label(window, text="Release Date (YYYY-MM-DD):")
release_date_label.pack()
release_date_entry = tk.Entry(window)
release_date_entry.pack()

fetch_button = tk.Button(window, text="Fetch Games", command=fetch_games)
fetch_button.pack()

# Create a scrollable text area
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

game_text = tk.Text(window, height=20, width=80, yscrollcommand=scrollbar.set)
game_text.pack()

scrollbar.config(command=game_text.yview)

# Create powered by RAWG hyperlink
rawg_label = tk.Label(window, text="Powered by RAWG", fg="blue", cursor="hand2")
rawg_label.pack()
rawg_label.bind("<Button-1>", open_rawg)

# Start the GUI event loop
window.mainloop()
