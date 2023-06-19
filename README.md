# briartistry
Appointment App for BriArtistry

To run the application, follow these steps:

    Save the code as app.py.
    Install the required dependencies by running pip install flask.
    Save the script as register_users.py.
    Open a terminal or command prompt and navigate to the directory where the files are saved.
    Run the command python app.py to start the Flask server.
    In a separate terminal or command prompt, run the command python register_users.py to execute the registration script.

The script will send POST requests to the respective registration endpoints, registering a user and a service provider. The server will process the requests, save the registration data to the SQLite database, and return a JSON response indicating the success of the registration.

Remember to adjust the URLs and registration data as needed for your application.

Note: This example provides a minimal implementation for demonstration purposes. You may need to enhance the code to include data validation, error handling, authentication, and other necessary features based on your project requirements.
