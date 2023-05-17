# Inventory Management System

This is a robust inventory management system built with Django. It allows businesses to keep track of their inventory in real-time. It's efficient, user-friendly, and highly customizable to meet your business needs.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7+
- Django 3.2+
- pip (Python package installer)

### Installation

1. Clone the repo
    ```
    git clone https://git@github.com:bokievkhushnud/FYP.git
    ```
2. Navigate into the project directory
    ```
    cd ims
    ```

3. Create a Python virtual environment and activate it
    ```
    python3 -m venv venv
    source venv/bin/activate  # Unix or MacOS
    .\venv\Scripts\activate   # Windows
    ```

4. Install the required packages
    ```
    pip install -r requirements.txt
    ```

### Database Setup

This project uses Django's default SQLite database. If you wish to use other databases, adjust the DATABASES setting in settings.py according to your preference.

Run the following command to apply migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

### Running the Server

Start the development server:

By default, the server will be accessible at `127.0.0.1:8000`.


## Usage

Once the server is running, you can navigate to the homepage at `http://127.0.0.1:8000/`. From there, you can create an account, log in, and start managing your inventory.
First, you should create a superuser by running the follwing command:
    ```
    python manage.py createsuperuser
    ```
After, you can create departments and assign admins to them, and then admins can start managing their inventory.
Note: All the users except superuser should create accoutn by registering via auth page using UCA email.

## License

This project belongs to UCA

## Acknowledgments

- Django - The web framework used.
- Khushnud Boqiev - Initial work.
