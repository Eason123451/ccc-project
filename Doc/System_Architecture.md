### Route List: 11
  - `/search-vic-population` ------- GET method for vic population data
  - `/search-twitter-daily-tweets` ------- GET method for twitter daily tweets data
  - `/search-twitter-daily-average-sentiment` ------- GET method for twitter daily average sentiment data
  - `/search-twitter-busiestday-with-size` ------- GET method for twitter busiestday data
  - `/search-vic-crime-by-area` ------- GET method for vic crime by area data
  - `/search-vic-crimegov` ------- GET method for vic crimegov data
  - `/search-south-crimegov` ------- GET method for south crimegov data
  - `/mastodon/{size}` ------- GET method for mastodon data with requested size
  - `/search-vic-crime-by-offence-count` ------- GET method for vic crime by offence count data
  - `/search-viccrime-for-twitter` ------- GET method for viccrime for twitter data
  - `/search-twitter-quietestday` ------- GET method for twitter quietestday data

### Function List: 13
  - `deletemharvester` ------ delete old data in the Mastodon in a day
  - `search-south-crimegov` ----- search south crimegov data
  - `search-vic-crime-by-offence-count` ----- search vic crime by offence count
  - `search-vic-crimegov` ----- search vic crimegov data
  - `search-twitter-quietestday` ----- search twitter quietestday data
  - `search-vic-crime-by-area` ----- search vic crime by area data
  - `search-twitter-daily-tweets` ----- search twitter daily tweets data
  - `searchmharvester` ----- search mastodon data
  - `search-twitter-busiestday` ----- search
  - `mharvester` ----- fetch real-time data from Mastodon
  - `search-viccrime-for-twitter` ----- search  viccrime for twitter data
  - `search-vic-population` ----- search vic population data
  - `search-twitter-daily-average-sentiment` ----- search twitter daily average sentiment data

### ConfigMap List: 1
  - `shared-data.ymal` For ElasticSearch client password and username management

### Timetrigger List: 2
  - `mharvester-ingest` timer for every 3 minutes to run mharvester function to fetch real time from Mastodon
  - `delete-mharvester` timer to run deletemharvester function to delete the old in a day at midnight
