# LaLiga_scraping

This repository contains the code to scrap results form spanish la Liga results.

## Getting Started

...

## Installing

In a new virtual environment:

```
pip install -r requirements.txt
```

## Create tables
### table results
```
CREATE TABLE results
(
  "id" SERIAL PRIMARY KEY,
  "temporada" text NOT NULL,
  "competicio" text NOT NULL,
  "data" timestamp NOT NULL,
  "jornada" integer NOT NULL,
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
ALTER TABLE public.resultats
  OWNER TO <user>;
```


### Table calendar
```
CREATE TABLE calendar
(
  "id" SERIAL PRIMARY KEY,
  "temporada" text NOT NULL,
  "competicio" text NOT NULL,
  "jornada" integer NOT NULL,
  "local" text NOT NULL,
  "visitant" text NOT NULL,
  "hora" timestamp NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.calendari
  OWNER TO <user>;
```