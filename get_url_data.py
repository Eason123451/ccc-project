import requests

def get_url_data(port, endpoint):
    """Fetch data from a specified port and endpoint."""
    fission_url = f"http://localhost:{port}/{endpoint}"
    try:
        response = requests.get(fission_url, verify=False)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON from response at {fission_url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None
