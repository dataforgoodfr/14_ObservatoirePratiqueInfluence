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

## Running tiktok
As we do not have an automatic way to extract post list yet, we need to manually generate the task. For testing purposes the easiest would be to copy the extraction sample task for tiktok.

```bash
cp data/tiktok_sample_task.csv data/extraction_task.csv
uv run src/main.py extract -n tiktok
```

## Running toktok /instagram extractor
TODO

# Uploading local accounts and posts CSVs to the central noco db

```bash
uv run src/main.py upload-results
```
