import requests

def get_url_data(port, endpoint):
    """Generic function to fetch data from a given Fission function endpoint."""
    fission_url = f"http://localhost:{port}/{endpoint}"
    response = requests.get(fission_url, verify=False)
    return response.json()