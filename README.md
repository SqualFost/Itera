<img width="645" height="311" alt="image" src="https://github.com/user-attachments/assets/52bffdc1-22d7-4be5-aa0e-4ebbb17fd85b" /># ITERA

**Local CLI AI Agent powered by Ollama.**

ITERA is a lightweight terminal-based coding assistant. It combines the power of local LLMs with tool-calling capabilities for file operations, system inspection, and shell execution.

---

## Features

* **Local LLM Chat via Ollama**: Complete privacy without cloud dependencies.
* **Tool Calling System**: Autonomous agent reasoning and action capabilities.
* **File System Access**: Read, write, search, and explore files and directories.
* **System Monitoring**: Real-time CPU, RAM, disk, and battery statistics.
* **Shell Command Execution**: Run system commands directly from the chat.
* **Project Exploration**: Visual representation of project tree structures.
* **Streaming CLI Interface**: Fluid response rendering within the terminal.

---

## Architecture

```text
Itera/
├── main.py        # CLI interface (UI + chat loop)
├── model.py       # LLM wrapper + agent reasoning loop
├── tools.py       # System, file, and shell tool definitions
└── README.md      # Documentation
```

---

## Requirements

* Python 3.10+
* Ollama installed and running locally

### Install Dependencies

```bash
pip install ollama psutil rich
```

### Run

Start the CLI:

```bash
python main.py
```

Or using uv:

```bash
uv run main.py
```

---

## Usage

Once started:

```bash
ITERA > How can I help you?
```

The assistant will process the request. To exit:

* `Ctrl + C`
* `/exit`
* `/bye`

---

## Available Tools

ITERA can dynamically invoke the following tools:

### File System
* `read_file(path)`
* `read_many_files(files)`
* `write_file(path, content)`
* `list_files(path)`
* `search_files(root, query)`
* `tree(path)`

### System
* `system_info()`: Returns CPU, RAM, disk, and battery usage statistics.

### Shell
* `run_command(cmd)`: Executes system-level commands.

---

## Model Behavior

ITERA operates as a local agent following these steps:
1. The user provides an input.
2. The LLM determines if specific tools are required.
3. Tools are executed locally on the host machine.
4. The execution results are fed back into the model context.
5. A final response is generated for the user.

---

## Example

![ITERA EXAMPLE](Example_screen.png)

---

## Security Warning

The `run_command` tool executes shell commands directly on your system. Use this feature with caution and only within trusted environments.

---

## Tech Stack

* **Ollama**: Local LLM runtime.
* **Python**: Core programming language.
* **psutil**: System information retrieval.
* **rich**: Terminal UI rendering and formatting.

---

## Concept

ITERA is designed as a minimal, local alternative to tools like Claude Code or Gemini CLI, focusing on:
* Local execution and data sovereignty.
* Tool-augmented reasoning.
* Extensible agent architecture.
