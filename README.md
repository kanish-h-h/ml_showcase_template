# ML Showcase Flask Application

**Specialized template designed specifically for demonstrating AI work professionally.**

This repository hosts a Flask web application meticulously crafted to showcase machine learning models and AI agents in a professional and interactive manner. It provides a structured environment for deploying, demonstrating, and interacting with various AI functionalities.

## Project Overview

This is a Python Flask web application designed to showcase machine learning models and AI agents. It leverages popular libraries such as `scikit-learn`, `numpy`, `pandas`, `joblib` for ML and data handling, `plotly` for advanced data visualization, and `gunicorn` for robust production deployment. The application's modular design ensures clear separation of concerns across models, agents, configuration, and routing, facilitating easy expansion and maintenance.

## Key Features

*   **ML Model Showcase:** The application provides dedicated pages and API endpoints to demonstrate various machine learning models (e.g., sentiment analysis). It features a centralized `ModelManager` for efficient loading, caching, and management of models.
*   **AI Agent Demos:** Interactive demonstrations of AI agents (e.g., Research Assistant, Data Analyst) are integrated, allowing users to interact with and understand their capabilities. The `BaseAgent` class provides a foundation for developing diverse agent functionalities.
*   **API Endpoints:** Comprehensive RESTful APIs are exposed for both model predictions (e.g., `/api/predict/sentiment`) and agent interactions (e.g., `/api/agent/<agent_name>/chat`), enabling seamless programmatic access and integration with other systems.
*   **Modular Design:** The codebase is organized into distinct, logical modules (`app/models`, `app/agents`, `app/templates`, `app/static`) to promote code reusability, testability, and maintainability.
*   **Configuration Management:** A robust configuration system in `config.py` allows for easy management of environment-specific settings (development, production, testing), ensuring flexibility and security across different deployment stages.

## Technologies Used

*   **Web Framework:** [Flask](https://flask.palletsprojects.com/) - A lightweight and powerful Python web framework.
*   **Machine Learning & Data Science:**
    *   [scikit-learn](https://scikit-learn.org/): For classical machine learning algorithms and tools.
    *   [NumPy](https://numpy.org/): The fundamental package for numerical computing in Python.
    *   [Pandas](https://pandas.pydata.org/): For efficient data manipulation and analysis.
    *   [Joblib](https://joblib.readthedocs.io/): For serializing and deserializing Python objects, particularly useful for ML models.
*   **Visualization:** [Plotly](https://plotly.com/python/) - For creating interactive, high-quality data visualizations for web applications.
*   **Deployment:** [Gunicorn](https://gunicorn.org/): A robust WSGI HTTP server for Unix, used for serving the Flask application in production environments.
*   **Configuration:** [python-dotenv](https://pypi.org/project/python-dotenv/): Manages environment variables from a `.env` file, simplifying configuration.

## Building and Running

To set up and run this project locally:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ml_showcase_template
    ```
2.  **Create a virtual environment:**
    It is highly recommended to use a virtual environment to isolate project dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    Install all required Python packages listed in `requirement.txt`.
    ```bash
    pip install -r requirement.txt
    ```
4.  **Set environment variables:**
    Copy the `.env.example` file to `.env` in the project root directory. Open `.env` and fill in any necessary environment variables, such as `SECRET_KEY`.
    ```bash
    cp .env.example .env
    ```
5.  **Run the application (development mode):**
    Start the Flask development server.
    ```bash
    python run.py
    ```
    The application will typically be accessible at `http://localhost:5949`. Check your console output for the precise URL.

## Development Conventions

*   **Modular Structure:** The project adheres to a modular design, separating functionalities into dedicated directories (`app/models`, `app/agents`, `app/routes`, `app/templates`, `app/static`). This promotes clear organization, reusability, and easier maintenance.
*   **Centralized Configuration:** All application configurations are managed through `config.py`, offering distinct settings for development, testing, and production environments. This approach ensures adaptability and security, leveraging environment variables for dynamic configuration loading.
*   **Development Mocking:** Key components like `ModelManager` and agent implementations include mock objects. This allows developers to run and test the application's interface and core logic effectively, even when complete ML models or complex agent integrations are still under development.
*   **Comprehensive Error Handling:** Custom error pages are implemented for common HTTP status codes (e.g., 404 Not Found, 500 Internal Server Error). These handlers enhance user experience by providing informative feedback for unexpected situations.
*   **Jinja2 Template Helpers:** `app/__init__.py` utilizes Jinja2 context processors to inject global variables such as `app_name`, `app_version`, and `current_year` into all HTML templates. This ensures consistent branding and dynamic content rendering across the application.

## How to Extend

*   **Adding new ML Models:** Place your trained models (`.pkl` or `.joblib` format) in the `app/models/` directory. Create a new wrapper class in `app/models/your_models.py` (or a new file) that uses `ModelManager.get_model()` to load your model and define its prediction logic.
*   **Adding new AI Agents:** Create a new class inheriting from `BaseAgent` in `app/agents/agent_system.py` (or a new file). Implement the `process()` method with your agent's specific logic. Register your new agent in the `AGENTS` dictionary within `app/agents/agent_system.py`.
*   **Adding new Demos/Routes:** Define new routes in `app/routes.py` and create corresponding HTML templates in `app/templates/demos/`.
*   **Customizing UI:** Modify `app/static/css/style.css` and the HTML templates in `app/templates/` to change the application's appearance.
