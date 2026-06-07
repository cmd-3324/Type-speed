



import sys
import os
import platform
from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass, field
import subprocess
from pathlib import Path
from datetime import datetime
from PIL import Image 
from time import time
from sentences import generate_string
from scorer import calculate_score
from plot import plot_scores
# image = Image.open("speed_test.png")
# image.show()
all_scores = []
@dataclass
class MenuItem:
    key: str
    label: str
    action: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
class Menu(ABC):
    def __init__(self, title):
        self.title = title
        self.items = []
        self.running = True
    def add_item(self, key, label, action, *args, **kwargs):
        self.items.append(MenuItem(key, label, action, args, kwargs))
        
    @staticmethod
    def clear_screen():
        os.system("cls" if platform.system() == "Windows" else "clear")
    @abstractmethod
    def render(self):
        pass
    
    def handle_choice(self, choice):
        for item in self.items:
            if choice.lower() == item.key.lower():
                item.action(*item.args, **item.kwargs)
                return True
        return False
    def run(self):
        while self.running:
            self.clear_screen()
            self.render()
            choice = input("\n  Choice: ").strip()
            if not self.handle_choice(choice):
                print("Invlaid")
                input("Press Enter .. ") 
class BoxMenu(Menu):
    WIDTH = 44
    def _line(self, char="═", corners=("╔","╗","╝","╚")):
            return f"{corners[0]}{char * self.WIDTH}{corners[1]}"
    
    def render(self):
        print(self._line())
        print(f"║{self.title.center(self.WIDTH)}║")
        print(self._line("═", ("╠","╣","╝","╚")))
        for item in self.items:
            print(f"║  {item.key}. {item.label:<{self.WIDTH-5}}║")
        print(self._line("═", ("╚","╝","╝","╚")))
class App:
    def __init__(self):
        self.menu = None
    def register_menu(self, menu):
        self.menu = menu
    def start(self):
        if self.menu is None:
            raise RuntimeError("No menu")
        self.menu.run()

def action_exit():
    print("\n  Done.\n")
    sys.exit(0)
def open_chart(filepath="speed_test.png"):
    path = Path(filepath)
    if not os.path.exists(path):
        print(F"File \t {filepath} does not exist")
        return 
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])
settings = {
    "chunks": 6,
    "chunk_length": 5,
    "symbols": True,
    "numbers": True,
    "uppercase": True
}
def action_settings():
    
    print("\n  CURRENT SETTINGS")
    print(f"  1. Chunks: {settings['chunks']}")
    print(f"  2. Chunk Length: {settings['chunk_length']}")
    print(f"  3. Symbols: {settings['symbols']}")
    print(f"  4. Numbers: {settings['numbers']}")
    print(f"  5. Uppercase: {settings['uppercase']}")
    print(f"  6. Back")
    
    user_input = input("\n Change Option : ").strip()
    if user_input == "1":
        settings["chunks"] = int(input("  Chunks (3-10): "))
    elif user_input == "2":
        settings["chunk_length"] = int(input("  Length (3-8): "))
    elif user_input == "3":
        settings["symbols"] = not settings["symbols"]
        print(f"  Symbols: {settings['symbols']}")
    elif user_input == "4":
        settings['numbers'] = not settings['numbers']
        print(F"Numbers : {settings['numbers']}")
    elif user_input == "5":
        settings['uppercase'] = not settings['uppercase']
        print(f"Uppercase : {settings['uppercase']}")
    input("... Press Enter ....")
    
    
def action_start():
    target = generate_string(
        chunks=settings["chunks"],
        chunk_length=settings['chunk_length'],
        uppercase = settings['uppercase'],
        numbers = settings['numbers'],
        symbols = settings['symbols'],
    )
    print(f"Type this : \n\n {target} ")
    input("... Press Enter If you are ready...")
    started_game = time()
    user_input = input("Go on : ")
    end_game = time()
    elapsed = end_game - started_game
    wpm, accuracy = calculate_score(target, user_input, elapsed)
    all_scores.append({
        "wpm": wpm,
        "accuracy": accuracy,
        "time": elapsed,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    print(f"\n  Time: {elapsed:.1f}s | WPM: {wpm} | Accuracy: {accuracy}%")
    input("\n  ...Press Enter...")
    

def action_view_scores():
    if not all_scores:
         print("There is no scores yet. Play to add")
         return 
    plot_scores(all_scores)
    open_chart("speed_test.png")
    input("...Press Enter ...")
# ---- Main ----
def main():
    menu = BoxMenu("Type Speed - Track Your Speed")
    menu.add_item("1", "Start Test ", action_start)
    menu.add_item("2","Settings", action_settings)
    menu.add_item("3", "View Last Chart", action_view_scores)
    menu.add_item("5", "Exit", action_exit)
    
    app = App()
    app.register_menu(menu)
    app.start()
if __name__ == "__main__":
    main()