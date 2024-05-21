import requests

def get_mastodon_data(port):
    fission_url = f"http://localhost:{port}/search-vic-population"
    response = requests.get(fission_url,verify=False)
    return len(response.json())


print(get_mastodon_data(9030))