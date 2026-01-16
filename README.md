# Library-Management-System
This repository contains the Circulation Management core of the Library System, developed using Python and MySQL. It handles the complete lifecycle of book lending, from eligibility validation to automated fine calculation.

## Testing report

### Prerequisites
- Python 3.9 or higher (3.12 recommended)
- Git installed

---
## Setup Instructions

### Step 1: Create Virtual Environment
```bash
python -m venv .venv
```

Activate the virtual environment:

- On Windows (PowerShell):
```bash
.venv\Scripts\Activate.ps1
```

- On macOS/Linux:
```bash
source .venv/bin/activate
```

### Step 2: install library
```bash
pip install -r requirements.txt
```
---

### Create a config.py files, in that you need to have the following Configuration

```bash
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your-password',
    'database': 'LibraryDB',
    'port': 3306
}
```

## Project structure

```
📦src
 ┣ 📂 UML: Design Documentation
    ┣ ClassDiagram
    ┣ DFD (Data Flow Diagram)
    ┣ ERD (Entity Relationship Diagram)
 ┣ 📂 controllers: The logic layer that coordinates between the Model and the View.
 ┣ 📂 models: The data layer of the application.
 ┣ 📂 views: The presentation layer (User Interface).
 ┗ 📜 main.py: The entry point of the application.
```
