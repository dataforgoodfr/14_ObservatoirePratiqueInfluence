# Installation

```
uv sync
```


# Run extractor with local extraction tasks

Generate extraction tasks from [./data/account_urls.csv]
```
uv run src/generate_tasks.py
```

Run youtube extractor for tasks defined in [./data/extraction_tasks.csv]

The youtube extractor relies partly on the Youtube Data API.
You need an API key to use it.
See https://developers.google.com/youtube/v3/getting-started for instructions
```
export YOUTUBE_API_KEY=<YOUR_API_KEY> && uv run src/main.py -n youtube
```