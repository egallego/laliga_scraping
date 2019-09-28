# LaLiga_scraping

This repository contains the code to scrap results form spanish la Liga results.

## Getting Started

...

## Installing

In a new virtual environment:

```
pip install -r requirements.txt
```
## Variable configuration
```
export DATABASE_LOGIN="postgresql://<user>:<pw>@<db_url>"
```
## Create tables
### table results
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
  "resultat" character(1) NOT NULL,
  "gols_local" integer NOT NULL,
  "gols_visitant" integer NOT NULL,
  "possesio_local" double precision,
  "possesio_visitant" double precision,
  "possesio_temporal" json,
  "ocasions_local" json,
  "ocasions_visitant" json,
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