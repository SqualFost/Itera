import os, time
import sys
import tty
import termios
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

console = Console()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def launch_ui(ai_name="demo"):
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

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    clear_terminal()

    with console.status("[bold sea_green2]Initializing ITERA...", spinner="bouncingBar"):
        time.sleep(1)

    console.print(launch_ui())
    console.print("\n[dim]— Press M to change model[/dim]\n")

if __name__ == "__main__":
    main()