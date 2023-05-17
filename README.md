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



### Running the Server

Start the development server:



By default, the server will be accessible at `127.0.0.1:8000`.

### Tests

To run the tests:



## Usage

Once the server is running, you can navigate to the homepage at `http://127.0.0.1:8000/`. From there, you can create an account, log in, and start managing your inventory.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Django - The web framework used.
- Your name - Initial work.




