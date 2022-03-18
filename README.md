# FakeNews - Data Crawling und Data Analysis Repository

In diesem GitHub zum Projekt Maschinelle Fake News Erkennung bei Prof. Dr. Øyvind Eide im Kurs Digital Humanities und Informatik der Geisteswissenschaften liegen alle von mir (Nina Eckertz) verfassten Skripte zum Crawlen der Daten von Twitter mit snscrape und deren Analyse.
Die vorliegenden Skripte und Ergebnisse sind Teil eines Gruppenprojektes mit Shera Potka und Kamil Schock.

## Repository Struktur
- DataAnalysis: Base für die  Analyse Skripte für Frequency Distrubution, Topic Modelling, Sentiment Analysis und Named Entity Recognition.
- DataCrawling: Base für die Crawler Skripte für die Twitter API und snscrape. Die benutzten Datensätze für die Analysen sind im Verzeichnis DataCrawling/TwitterCrawlDirecotry/Tweets_2021
- Results: Passend zu den Analyse-Skripten die Verzeichnisse mit den gerenderten Graphen.

Jedes Skript verfügt zudem über Kommentare und DocStrings um die Struktur und Logik des Codes weitesgehend zu erklären. Die Skripte können jeweils über ihre main()-Funktion einzelnd aufgerufen werden.

## Installation
Als Entwicklungsumgebung wurde für dieses Projekt PyCharm verwendet. Ich verwende keine spezifische Version der folgenden Bibliotheken, daher können diese einfach mit PyCharm innerhalb eines Virtual Environments heruntergeladen und installier werden.
Alternativ können natürlich alle Bibliotheken auch mit pip installiert werden. 

### Verwendete Bibliotheken
- requests
- json
- os
- pandas
- plotly
- textblob_de
- re
- string
- networkx
- random
- nltk
- spacy


Sollte etwas nicht funktionieren oder weitere Fragen bestehen, bitte ich um eine schnelle Kontaktaufnahme. Viel Spaß beim Ausprobieren der Grafiken. 
