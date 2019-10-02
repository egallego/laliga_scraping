# LaLiga_scraping

This repository contains the code to scrap results form spanish la Liga results.

When planning to scrape a website, you should always check its robots.txt first. Robots.txt is a file used by websites to let "bots" know if or how the site should be scrapped or crawled and indexed. You could access the file by adding "/robots.txt" by the end of the link of your target website. At the moment of writng this code the page of 'resultados' (the static page, not the real time one) in not listed in the disallow list. 

There are multiple concerns with scrapping data. Be responsible when doing it. This project is presented as example only, data is not pubilc avalible and no profit has been obtained from it.
## Getting Started

To start we will:
 - Install a new virtual environment 
 - Define an environment variable
 - Create the necessari tables in our POSTGRES DB.

## Installing

In a new virtual environment:

```
pip install -r requirements.txt
```
## Variable configuration
```
export DATABASE_LOGIN="postgresql://<user>:<pw>@<db_url>"
```
## Create POSTGRES tables
Here is presented the code to create two tables, table _results_ and table _calendar_.
### Table results
```
CREATE TABLE results
(
  "id" SERIAL PRIMARY KEY,
  "season" text NOT NULL,
  "competition" text NOT NULL,
  "date" timestamp NOT NULL,
  "round" integer NOT NULL,
  "local" text NOT NULL,
  "visitant" text NOT NULL,
  "result" character(1) NOT NULL,
  "goals_local" integer NOT NULL,
  "goals_visitant" integer NOT NULL,
  "possession_local" double precision,
  "possession_visitant" double precision,
  "possession_temporal" json,
  "attempts_local" json,
  "attempts_visitant" json,
  "url" character(150) NOT NULL
)
WITH (
  OIDS=FALSE
);
```


### Table calendar
```
CREATE TABLE calendar
(
  "id" SERIAL PRIMARY KEY,
  "season" text NOT NULL,
  "competition" text NOT NULL,
  "round" integer NOT NULL,
  "local" text NOT NULL,
  "visitant" text NOT NULL,
  "date" timestamp NOT NULL
)
WITH (
  OIDS=FALSE
);
```

## Run the code
There are two scripts presented as examples:
```
python 01_calendar_scraping.py --season 2017_2018
```
Get calendar information for season 2017-2018

```
python 02_scrap_laliga.py --season 2017_2018
```
Get data from page for season 2017-2018