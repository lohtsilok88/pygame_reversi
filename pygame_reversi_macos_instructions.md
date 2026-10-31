# Run `pygame_reversi` on macOS

These instructions show how to clone and run the Reversi game repository on a Mac using Terminal.

Repository: https://github.com/lohtsilok88/pygame_reversi

## 1. Open Terminal

Open **Terminal** on your Mac (press `Command + Space`, type `Terminal`, then press Enter).

## 2. Check that Git and Python are installed

Run:

```bash
git --version
python3 --version
```

If either command is unavailable, install the missing tool before continuing. You can install Apple's command-line tools (which include Git) with:

```bash
xcode-select --install
```

Install Python 3 from [python.org](https://www.python.org/downloads/macos/) if `python3` is not available.

## 3. Clone the repository

Run:

```bash
git clone https://github.com/lohtsilok88/pygame_reversi.git
cd pygame_reversi
```

## 4. Create and activate a virtual environment

This keeps the game's Python packages separate from other projects:

```bash
python3 -m venv venv
source venv/bin/activate
```

When activated, the environment name (usually `(venv)`) appears at the start of the Terminal prompt.

## 5. Install the dependencies

First, check the files in the repository:

```bash
ls -la
```

If the repository contains `requirements.txt`, install its listed dependencies:

```bash
python -m pip install -r requirements.txt
```

If there is no `requirements.txt` and the project uses Pygame, install Pygame:

```bash
python -m pip install pygame
```

If the repository's README gives different installation instructions, follow those instructions.

## 6. Find the Python entry point

List the Python files:

```bash
find . -maxdepth 3 -name "*.py"
```

Check `README.md` for the intended run command, if present:

```bash
cat README.md
```

The main file might be named `main.py` or `reversi.py`, but the correct filename depends on the repository. Do not assume either name without checking.

## 7. Run the game

Use the actual entry-point filename found in the previous step. For example:

```bash
python main.py
```

Or, if the entry point is named `reversi.py`:

```bash
python reversi.py
```

If the main file is inside a folder, include that folder in the path, for example:

```bash
python src/main.py
```

## Troubleshooting

### `git: command not found`

Install Apple's command-line tools:

```bash
xcode-select --install
```

### `python3: command not found`

Install Python 3 from [python.org](https://www.python.org/downloads/macos/).

### `No module named pygame`

Activate the virtual environment, then install Pygame:

```bash
source venv/bin/activate
python -m pip install pygame
```

### You are not sure which file to run

From inside the repository folder, run:

```bash
pwd
ls -la
find . -maxdepth 3 -name "*.py"
```

Check the repository's `README.md` for its recommended launch command.

### Leave the virtual environment

When you have finished:

```bash
deactivate
```

To run the game another time, open Terminal, go to the project folder, activate the environment, and run the game:

```bash
cd pygame_reversi
source venv/bin/activate
python main.py
```

Replace `main.py` with the actual entry-point filename if it is different.
