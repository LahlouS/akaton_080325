# akaton_080325

vous trouverez les fichiers data a l'adresse:
https://drive.google.com/file/d/1iZ7x2a3BHaF6wLbc9ZqDXNWejF4-AYdn/view?usp=drive_link

j'ai mis tous les fichiers mais le dataset clean et merge est le fichier suivant: ***clean_joe_donald.csv***

Je vous ai laissé a dataprep effectué pour produire le dataset.

: cmd : unzip datas.zip

# Dataset Description

## Overview
This dataset contains social media data collected from Twitter. It includes metadata about users, their tweets, and their locations. The dataset is structured with various columns capturing user details, tweet content, and geographic information.

## Columns Description

| Column Name             | Data Type  | Description |
|-------------------------|-----------|-------------|
| `source`               | string    | Source of the tweet (e.g., TweetDeck, Social Mediaset). |
| `user_id`              | int64     | Unique identifier of the user. |
| `user_name`            | string    | Name of the user. |
| `user_screen_name`     | string    | Twitter handle of the user. |
| `user_description`     | string    | Bio or description provided by the user. |
| `user_followers_count` | float64   | Number of followers the user has. |
| `user_location`        | string    | Location provided by the user in their profile. |
| `lat`                  | float64   | Latitude coordinate of the user (if available). |
| `long`                 | float64   | Longitude coordinate of the user (if available). |
| `city`                 | string    | City associated with the tweet (if available). |
| `country`              | string    | Country associated with the tweet. |
| `continent`            | string    | Continent associated with the tweet. |
| `state`                | string    | State (if applicable). |
| `state_code`           | string    | State code (if applicable). |
| `collected_at`         | datetime  | Timestamp when the data was collected. |

## Notes
- Some fields may contain `NaN` values when the data is unavailable.
- Geographic data (`lat`, `long`, `city`, etc.) may be missing for some users.
- The dataset includes metadata from different sources and may require cleaning before analysis.

## Usage
This dataset can be used for various analyses, such as:
- Social media trends and engagement
- User location-based analytics
- Sentiment analysis and topic modeling

For any questions or clarifications, please reach out to the dataset provider.

