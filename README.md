# Github Fetcher

## About 

This project include fetching of repositories from github api of a person and store that in the local sqlite database using Sqlalchemy ORM.
and display the total number of entries distribution of entries by certain columns also top 10 entries.It also implements search functionality to find a project by id,
name ,description,fullname and also using language used.

## Setup

To setup the project locally follow the given steps below :

  * ```git clone https://github.com/yagyagoel1/githubfetcher/```
  
After Cloning it locally in root dir of the project execute these commands:

  * **Copy the .env.sample to .env or provide your own github username** 

  * ```python3 -m venv myenv```
  
  * ```source myenv/bin/activate```
  
  * ```pip install -r requirements.txt```
  
  * ```python app/fetch_store_data.py```

To Checkout the Dashboard visit(if port 8501 is not occupied):
``` http://localhost:8501```
  
To stop the program press ```Ctrl + C``` 



