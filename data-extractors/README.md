# Installation

```bash
uv sync
```


# Configure .env file
Copy [.env.example] file to [.env] and set/modify the relevant values.


# Generating extraction tasks locally from a list of account urls

Generate extraction tasks [./data/extraction_tasks.csv] from [./data/account_urls.csv]
```bash
uv run src/main.py generate-task
```

# Run extractors locally from the list of extraction tasks
This allows to run the extraction tasks defined in [./data/extraction_tasks.csv] using a given extractor.
And stores the results in [./data/accounts.csv] and [./data/posts.csv]

## Running youtube extractor
The youtube extractor relies on the Youtube Data API.
You need to configure YOUTUBE_API_KEY in the .env file to be able to use it.
Then run
```bash
uv run src/main.py extract -n youtube
```

## Running tiktok extractor

Tiktok default extractor uses TikTokApi which itself uses paywright.
Current implementation defaults to headed mode (headless=False) to avoid bans so it opens a browser windows.
To avoid this you can use xvfb  (X virtual frame buffer) to run the command
```bash
xvfb-run uv run src/main.py extract -n tiktok
```

## Running instagram extractor

Note: Running instagram extractor needs to use a mobile internet connexion
```bash
uv run src/main.py extract -n instagram
```

# Uploading local accounts and posts CSVs to the central noco db

```bash
uv run src/main.py upload-results
```
