from pathlib import Path

base_url = "https://lordofthemysteries.fandom.com/wiki/"
download_folder = Path(__file__).resolve().parent.parent.parent / "NullGPT_HTML"

download_folder.mkdir(parents=True, exist_ok=True)
print(download_folder)
