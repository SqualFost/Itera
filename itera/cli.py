import os
import time
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .agent import Agent, list_models, reset_context

console = Console()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def launch_ui(model):
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
    infos.append(f"{model}\n\n", style="bold green")
    infos.append(f"Date : \n", style="bold white")
    infos.append(f"{date_str}\n\n", style="yellow")
    infos.append(f"Hour : \n", style="bold white")
    infos.append(f"{time_str}", style="yellow")

    grid = Table.grid(padding=(0, 10))
    grid.add_column(no_wrap=True)
    grid.add_column(justify="left")
    grid.add_row(Text(itera_ascii, style="bold sea_green2"), infos)

    return Panel(grid, border_style="sea_green2", expand=False, padding=(1, 3))

def launch_selection():
    models = list_models()

    table = Table(title="Select an AI Model", border_style="sea_green2")
    table.add_column("Index", justify="right", style="bold")
    table.add_column("Model", style="green")

    for i, m in enumerate(models):
        table.add_row(str(i), m)

    console.print(Panel(table, border_style="sea_green2", padding=(1, 2)))

    while True:
        console.print("[bold sea_green2]Select model index > [/bold sea_green2]", end="")
        choice = input()

        if not choice.isdigit():
            console.print("[red]Invalid input. Enter a number.[/red]")
            continue

        idx = int(choice)

        if 0 <= idx < len(models):
            return models[idx]
        else:
            console.print("[red]Index out of range.[/red]")

def main(model):
    clear_terminal()

    with console.status("[bold sea_green2]Initializing ITERA...", spinner="bouncingBar"):
        time.sleep(1)

    if not model or model not in list_models():
        model = launch_selection()

        clear_terminal()
        with console.status("[bold sea_green2]Switching model...", spinner="bouncingBar"):
            time.sleep(0.5)

    agent = Agent(model=model)

    console.print(launch_ui(model))

    console.print("\n[dim]— Press Ctrl+C to exit[/dim]\n")
    console.print(f"[bold yellow4]ITERA > [/bold yellow4]Hi, how can I help you today ?\n")

    try:
        max_steps = 25
        step = 0

        while step < max_steps:
            step += 1
            console.print("[bold sea_green2]USER > [/bold sea_green2]", end="")
            text = input()
            print()

            if text.lower() in ['/exit', '/bye']:
                break
            elif text == '/model':
                console.print(list_models())
            elif text == '/reset':
                reset_context(agent)
            else:
                output = agent.chat(text)
                console.print("[bold yellow4]ITERA > [/bold yellow4]", end="")
                console.print(Markdown(output.strip()))
                print()

    except KeyboardInterrupt:
        pass
    finally:
        clear_terminal()
        with console.status("[bold sea_green2]Exiting ITERA...", spinner="bouncingBar"):
            time.sleep(1)
        clear_terminal()
