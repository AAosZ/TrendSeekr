# TrendSeekr

## NOTE: This is a dev build that will only work locally.

TrendSeekr is a python project that aggregates headlines from RSS feeds of different major North American news outlets.

Using spaCY, a NLP algorithm and AI models to sort headlines, TrendSeekr aims to provide users with insights into major long-term changes in the market.

## How it works

If you really want to download and use this dev build, you will require a LLM model, an embeddings model, and a high-end PC. Prepare to run into a lot of problems.

In [config.py](https://github.com/AAosZ/TrendSeekr/blob/master/config.py), replace DEFAULT_MODEL_PATH with the path to your LLM model and replace DEFAULT_EMBEDDING_MODEL_PATH with the path to your embeddings model.

For my dev build, I am using Deepseek R1 14B for the LLM model and Qwen3 0.6B for the embeddings model, but you can use what you want.

### NOTE: The embeddings model must output less than 2000 dimensions as the postgreSQL database does not accept larger than 2000 dimension vectors due to inherent PostgreSQL indexing size limitations.
