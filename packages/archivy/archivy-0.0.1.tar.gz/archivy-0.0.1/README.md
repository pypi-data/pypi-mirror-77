# Archivy

Archivy is a self-hosted knowledge repository that allows you to safely preserve useful content that contributes to your knowledge bank.

Features:


- If you add bookmarks, their webpages contents' will be saved to ensure that you will **always** have access to it, in sync with the idea of [digital preservation](https://jeffhuang.com/designed_to_last/).
- Allows you to sync up with Pocket to gather bookmarks from there too.
- Everything is a file! For ease of access and editing, all the content is stored in markdown files with yaml front matter.
- Extensible search with Elasticsearch and its Query DSL


![demo (low res)](https://github.com/Uzay-G/archivy/raw/master/archivy.gif)
Upcoming:

- Integrations with HN, Reddit, and many more.
- Add submodules for digital identity so archivy syncs to your hn upvoted posts, reddit saved, etc...
- Option to compile data to a static site that can be deployed.
- Dark theme
- UI for grouping by tag and use NLP to automatically generate connections between posts

## Setup

### Local Setup

- Make sure your system has Python installed.
- Clone the repository.
- `cd` into the project directory.
- create a virtual env by running `python3 -m venv venv/`.
- run `pip install -r requirements.txt` or `pip3`.
- execute the `start.sh` script
- see below for setting up search functionality


### With Docker

See the `docker` branch for details on setting things up with docker.

### Setting up Search

Archivy uses [ElasticSearch](https://www.elastic.co) to provide efficient full-text search.

Add these lines to your flaskenv:

```bash
ELASTICSEARCH_ENABLED=1
ELASTICSEARCH_URL=http://localhost:9200
```

Instructions to install and run the service are provided [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).


Append these two lines to your [elasticsearch.yml config file](https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html):

```yaml
http.cors.enabled: true
http.cors.allow-origin: "http://localhost:5000"
```
