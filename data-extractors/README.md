# Installation

```bash
uv sync
```


# Configure .env file
Copy [.env.example] file to [.env] and set/modify the relevant values. 


# Generating extraction tasks locally from a list of account urls

Generate extraction tasks [./data/extraction_tasks.csv] from [./data/account_urls.csv]
```bash
uv run src/main.py generate_task
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

## Running toktok/instagram extractor
TODO

# Uploading local accounts and posts CSVs to the central noco db

```bash
uv run src/main.py upload-results
```
