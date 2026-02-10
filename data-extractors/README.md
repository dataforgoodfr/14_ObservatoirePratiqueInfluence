# Installation

```bash
uv sync
```


# Running extractor with local extraction tasks

Generate extraction tasks [./data/extraction_tasks.csv] from [./data/account_urls.csv]
```bash
uv run src/main.py generate_task
```

Run youtube extractor for tasks defined in [./data/extraction_tasks.csv]

The youtube extractor relies partly on the Youtube Data API.
You need an API key to use it.
See https://developers.google.com/youtube/v3/getting-started for instructions
```bash
export YOUTUBE_API_KEY=<YOUR_API_KEY> && uv run src/main.py extract -n youtube
```