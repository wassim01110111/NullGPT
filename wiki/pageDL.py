import json
import re
import traceback
from pathlib import Path

import requests

directory = Path(__file__).resolve().parent
url_list_path = directory / "url_list.json"
base_url = "https://lordofthemysteries.fandom.com/wiki/"
download_folder = directory.parent.parent / "NullGPT_HTML"
download_folder.mkdir(parents=True, exist_ok=True)


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name)


with open(url_list_path, "r", encoding="utf-8") as f:
    url_list = json.load(f)
error_urls = set()

total = len(url_list)

for i, url in enumerate(url_list, start=1):
    full_url = base_url + url
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        html_content = response.text

        filename = sanitize_filename(url) + ".html"
        file_path = download_folder / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        percent = (i / total) * 100
        print(f"Downloaded {i}/{total} ({percent:.2f}%) - {url}")

    except Exception as e:
        error_urls.add(url)
        print(f"\n❌ Error while processing URL: {url}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Traceback:")
        traceback.print_exc()

print("List of errors:")
for error in error_urls:
    print(error)
