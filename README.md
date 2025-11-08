# Solar Data Discovery Challenge (Week 1)

This repository contains the analysis for the Cross-Country Solar Farm Analysis challenge.

## ⚙️ Environment Setup

To reproduce the environment locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/YourUsername/solar-challenge-week1.git](https://github.com/YourUsername/solar-challenge-week1.git)
    cd solar-challenge-week1
    ```

2.  **Create and activate the virtual environment (using `venv`):**

    ```bash
    # Create
    python -m venv venv
    # Activate (Linux/macOS)
    source venv/bin/activate
    # Activate (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 📂 Suggested Folder Structure

The project uses the following structure:
├── .github/ │ └── workflows/ │ └── ci.yml ├── .gitignore ├── requirements.txt ├── README.md ├── notebooks/ # For all Jupyter Notebooks (.ipynb) ├── src/ # For reusable Python code/modules ├── tests/ # For unit tests (not fully required this week) └── scripts/ # For standalone helper scripts
