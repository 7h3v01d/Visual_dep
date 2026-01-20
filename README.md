# VisualDep - Python Import Visualizer

**VisualDep** is a lightweight tool that analyzes Python projects and creates interactive **import dependency graphs** — helping you understand module relationships, spot tightly coupled code, and identify widely used shared modules.

---

⚠️ **LICENSE & USAGE NOTICE — READ FIRST**

This repository is **source-available for private technical evaluation and testing only**.

- ❌ No commercial use  
- ❌ No production use  
- ❌ No academic, institutional, or government use  
- ❌ No research, benchmarking, or publication  
- ❌ No redistribution, sublicensing, or derivative works  
- ❌ No independent development based on this code  

All rights remain exclusively with the author.  
Use of this software constitutes acceptance of the terms defined in **LICENSE.txt**.

---

Comes with two interfaces:

- **CLI** — `VisualDep.py` (fast, scriptable)
- **GUI** — `gui.py` (Tkinter-based, beginner-friendly)

Both generate beautiful interactive graphs using **Plotly** (2D or 3D).

https://github.com/7h3v01d/Visual_dep/assets/12345678/abcdef12-3456-7890-abcd-ef1234567890  
*(replace with actual screenshot / recording GIF when you upload one)*

## Features

- Visualizes **internal module imports** (and optionally external packages)
- 2D **and** 3D interactive graphs
- Shows **top shared modules** (most imported / central modules)
- Reproducible layouts with `--seed`
- Saves result as self-contained HTML file
- Simple Tkinter GUI with directory picker, options, live console & auto-open in browser

## Screenshots

### GUI

![GUI Screenshot](https://via.placeholder.com/780x520.png?text=GUI+Screenshot+-+replace+me)  
*(replace with real screenshot)*

### Example 3D Graph

![3D Graph Example](https://via.placeholder.com/800x600.png?text=3D+Interactive+Graph+Example)  
*(replace with real Plotly HTML export screenshot)*

## Installation

Requires **Python 3.8+**.


### Recommended: create a virtual environment first
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```
### Install dependencies
```bash
pip install networkx plotly
```
That's it — no other heavy dependencies!

### Usage
### 1. Using the GUI (recommended for most users)
```Bash
python gui.py
```
- Click Browse to select your project folder
- Choose 2D or 3D
- Optional: include external packages, show shared modules, set custom output file or seed
- Click Generate Graph

The graph opens automatically in your browser (or is saved if you specified an output path).

---
### 2. Using the CLI
Basic usage — current directory:
```Bash
python VisualDep.py
```
Most useful examples:
```Bash
# Save to file (most common)
python VisualDep.py /path/to/your/project --output deps.html

# 2D graph
python VisualDep.py --dim 2 --output graph-2d.html

# Include external libraries (numpy, requests, etc.)
python VisualDep.py --include-external --output full-deps.html

# Show top 10 most imported/shared modules
python VisualDep.py --show-shared

# Reproducible layout
python VisualDep.py --seed 123 --output stable.html
```

### Example Output

After running:
```text
textTop shared modules/packages (by number of connections):
myapp.core.utils: 18 connections
myapp.models.base: 14 connections
typing: 11 connections
os: 9 connections
...
```
…and you get a nice interactive Plotly graph like this:

(insert real screenshot or link to example HTML)

---
### Project Structure
```text
python-import-visualizer/
├── VisualDep.py       # Core CLI logic + graph generation
├── gui.py             # Tkinter graphical interface
├── README.md
└── requirements.txt   # (optional – you can create it)
```
Requirements (requirements.txt)
```text
txtnetworkx>=3.0
plotly>=5.0
```
---
### Limitations / Known Issues

- Very large projects (> 1000 modules) may become slow or visually cluttered
- Relative imports with high level values might be misresolved in rare cases
- External package nodes appear without version information
- No edge labels / directionality yet (undirected graph)

---

### Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

### License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
