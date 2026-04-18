import os
import time
import platform
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .agent import model_chat, list_models, reset_context

console = Console()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def launch_ui(ai_name="ITERA"):
    itera_ascii = r"""
 /$$$$$$ /$$$$$$$$ /$$$$$$$$ /$$$$$$$   /$$$$$$ 
|_  $$_/|__  $$__/| $$_____/| $$__  $$ /$$__  $$
  | $$     | $$   | $$      | $$  \ $$| $$  \ $$
  | $$     | $$   | $$$$$   | $$$$$$$/| $$$$$$$$
  | $$     | $$   | $$__/   | $$__  $$| $$__  $$
  | $$     | $$   | $$      | $$  \ $$| $$  | $$
 /$$$$$$   | $$   | $$$$$$$$| $$  | $$| $$  | $$
|______/   |__/   |________/|__/  |__/|__/  |__/
""".strip("\n")

    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")

    infos = Text()
    infos.append(f"Active model : \n", style="bold white")
    infos.append(f"{ai_name}\n\n", style="bold green")
    infos.append(f"Date : \n", style="bold white")
    infos.append(f"{date_str}\n\n", style="yellow")
    infos.append(f"Hour : \n", style="bold white")
    infos.append(f"{time_str}", style="yellow")

    grid = Table.grid(padding=(0, 10))
    grid.add_column(no_wrap=True)
    grid.add_column(justify="left")
    grid.add_row(Text(itera_ascii, style="bold sea_green2"), infos)

    return Panel(grid, border_style="sea_green2", expand=False, padding=(1, 3))

def main():
    clear_terminal()

    with console.status("[bold sea_green2]Initializing ITERA...", spinner="bouncingBar"):
        time.sleep(1)

    console.print(launch_ui())
    console.print("\n[dim]— Press Ctrl+C to exit[/dim]\n")
    console.print(f"ITERA > Hi {platform.uname().node.split('.')[0]}\n")
    
    try:
        max_steps = 25
        step = 0
        current_model = "gemma4:e4b"

        while step < max_steps:
            step += 1
            text = input("USER > ")

            if text.lower() in ['/exit', '/bye']:
                break
            elif text == '/model':
                console.print(list_models())
            elif text == '/reset':
                reset_context()
            else:
                output = model_chat(text, current_model)
                console.print("\nITERA >")
                console.print(Markdown(output))

    except KeyboardInterrupt:
        pass
    finally:
        clear_terminal()
        with console.status("[bold sea_green2]Exiting ITERA...", spinner="bouncingBar"):
            time.sleep(1)
        clear_terminal()

if __name__ == "__main__":
    main()
