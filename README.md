# FormFusion

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Issues](#issues)
- [Contributing](#contributing)


## Setup
To set up and run the platform, follow these steps:

### Prerequisites
- Python 3.8+
- `uagents` library

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/aastha51551/FormFusion.git
    ```

2. Enter the folder and in the termiinal run this to install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Agents
1. Start the Organisation Agent:
    ```sh
    python organisation.py
    ```

2. Start the User Agent:
    ```sh
    python user.py
    ```

## Usage
Once the agents are running, the User Agent will automatically query the Organisation Agent for available forms at regular intervals. The user can then submit filled forms to the Organisation Agent.

### Sample Interaction
1. **Query Form:**
    - The User Agent sends a query request for the form titled "Internship Session".
    - The Organisation Agent responds with the form details.

    **Query Request:**
    ```json
    {
        "body": "Please provide the form details",
        "title": "Internship Session"
    }
    ```

    **Query Response:**
    ```json
    {
        "forms": {
            "body": "This is an internship application form",
            "title": "Internship Session",
            "description": "Form to apply for internship",
            "fields": ["Name", "Email", "Phone", "Resume"]
        }
    }
    ```

2. **Submit Form:**
    - The User Agent submits the filled form.
    - The Organisation Agent stores the submission and responds with a success message.

    **Submit Request:**
    ```json
    {
        "title": "Internship Session",
        "fields": ["John Doe", "john.doe@example.com", "123-456-7890", "Resume content here"]
    }
    ```

    **Submit Response:**
    ```json
    {
        "success": true
    }
    ```

## Issues
If you encounter any issues or bugs, please report them in the [Issues](https://github.com/yourusername/form-platform/issues) section of the GitHub repository.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

Please ensure your code adheres to the existing coding standards and includes appropriate tests.
