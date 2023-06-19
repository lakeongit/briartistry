import requests

# User registration API endpoint
register_user_url = 'http://localhost:5000/register/user'

# User registration data
user_data = {
    'username': 'john_doe',
    'password': 'password123',
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'contact_details': '123-456-7890'
}

# Send POST request to register a user
response = requests.post(register_user_url, json=user_data)
print(response.json())  # Print the response message


# Service Provider registration API endpoint
register_provider_url = 'http://localhost:5000/register/service_provider'

# Service Provider registration data
provider_data = {
    'username': 'jane_smith',
    'password': 'password456',
    'name': 'Jane Smith',
    'email': 'jane.smith@example.com',
    'contact_details': '987-654-3210',
    'service_offerings': 'Hair Styling, Manicure'
}

# Send POST request to register a service provider
response = requests.post(register_provider_url, json=provider_data)
print(response.json())  # Print the response message
