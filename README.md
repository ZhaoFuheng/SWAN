# SWAN
## databases Folder
It contains a zip file of the four curated databases. 

It also contains the keys for each table and the columns that should be not be used.

## beyond-database-questions Folder
It contains the 120 beyond database questions used in SWAN.

To answer beyond-database questions, we include two baseline solutions in SWAN, HQDL and Hybrid Query (based on BlendSQL).

## Hybrid Query over Database and LLM
In HQDL, if a question cannot be answered based on the current database schema, then one may modify the database schema (add new columns/tables) to answer the questions. 
Hence, after modifying the schema (currently a manual step), one can use LLMs to fills in the missing values.
This approach is simple and requiers no modification to the query optimizer.
- **HQDL** - This folder contains HQDL.ipynb, the pipeline code used to evaluate HQDL on SWAN. It also contains the inputs for and the outputs from the OpemAI models (via the Batch API).

## Hybrid Query (via User Defined Function)
Many companies and opensource communties have supported LLM calls directly within the SQL query.
We evaluate [BlendSQL](https://github.com/parkervg/blendsql) on our SWAN benchmark.
- **HybridQuery** - This folder contains code for running BlendSQL on SWAN. It also contains the logs for our experiments on hybrid query.


