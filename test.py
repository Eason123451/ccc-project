import requests

def get_mastodon_data(port, size):
    fission_url = f"http://localhost:{port}/mastodon/{size}"
    response = requests.get(fission_url,verify=False)
    return response.json()


print(get_mastodon_data(8992,20))