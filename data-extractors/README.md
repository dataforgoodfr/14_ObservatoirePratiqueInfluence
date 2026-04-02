# Running extraction using staging server 

* Clone [this repository](https://github.com/dataforgoodfr/14_ObservatoirePratiqueInfluence) locally. (see [Cloning a repository](https://docs.github.com/fr/repositories/creating-and-managing-repositories/cloning-a-repository) for instructions)
* Install uv (https://docs.astral.sh/uv/getting-started/installation/)
* In data-extractors folder of cloned repository run `uv sync`
* Copy [.env.example] file to [.env] it is configured by default to use the staging server
* Set API_KEY value with the value provided on mattermost


## Run the tiktok extractor
Run `uv run src/main.py extract -n tiktok` in data-extractors folder.

## Run the instagram extractor
Instagram rejects scraping when coming from non mobile connections.

So you need to connect your PC to internet through your phone mobile connection using a hotspot. Ensure wifi is disabled on the phone otherwise this is useless.
Then run `uv run src/main.py extract -n instagram` in data-extractors folder.

## Run the youtube extractor
* Configure the YOUTUBE__API_KEY in [.env]
* run `uv run src/main.py extract -n youtube`


# Developpment guide

## Installation
* clone reposstiory
* install uv
* In data-extractors folder of cloned repository run `uv sync`

## Configure .env file
Copy [.env.example] file to [.env] and set/modify the relevant values.


## Testing scraping locally

Either:
* start the local server (see sepcific doc) and configure .env to use it
* use BACKEND=fs to use a local file based task management

### Generating extraction tasks from a list of account urls


Generate extraction tasks from [./data/account_urls.csv].
*Warning* this will push the task to the configured backend so DO NOT use this with staging server
When BACKEND=fs the tasks will be written to [./data/extraction_tasks.csv] 
```bash
uv run src/main.py generate-task
```

### Running extractors with BACKEND=fs
This allows to run the extraction tasks defined in [./data/extraction_tasks.csv] using a given extractor.
And stores the results in [./data/accounts.csv] and [./data/posts.csv]

# Using upload-results CLI

To upload local accounts and posts CSVs to the central noco db
Configure  UPLOAD_NOCODB_... in [.env]

```bash
uv run src/main.py upload-results
```