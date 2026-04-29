
import requests
import sys

# --- CONFIG ---
GIST_ID = "Your_Gist_Id_Here"
TOKEN = "YOUR_GITHUB_TOKEN_HERE" # <->
FILE_NAME = "tunnel_url.txt"

def update_gist(new_url):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            FILE_NAME: {
                "content": new_url
            }
        }
    }

r = requests.patch(url, headers=headers, json=paylo>
    if r.status_code == 200:
        print(f"✅ Gist updated: {new_url}")
    else:
        print(f"❌ Error {r.status_code}: {r.text}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_gist(sys.argv[1])
    else:
        print("Usage: python update.py <url>")

