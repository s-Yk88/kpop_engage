# Measuring Global Discovery Signals of K-Pop from User Playlists


This analysis explores how user-curated playlists surface K-pop tracks and whether there are observable differences in engagement signals that explain exposure. Using Spotify API data for the top tracks of 27 K-pop groups, I engineered artist- and track-level features including popularity, label affiliation, group composition, and track attributes. Then combine exploratory analysis, interpretable modeling, and robustness checks to identify which signals consistently differentiate exposed tracks. The analysis highlights structural patterns in platform indicators that inform music discovery, including the role of company affiliation and audio features in playlist visibility and how exposure correlates with engagement signals.

## Methods:
- Data Visualization
- Regression Analysis
- Feature Engineering
- Observational Causal Analysis
  
## Models:
- Logistic Regression
- Elastic Net
- Covariate-Adjusted Regression

## Tools/ Packages Used:

- R
    - `corrplot` `tidyverse` `ggplot2` `car` `caret` `glmnet` `pROC` `vip` `recipes` `dotwhisker` `ggridges` 
- Python 3.13.3
    - `spotipy` `pandas` `numpy`  `networkx`
 
## Full Report:

https://zesty-bubbler-a87.notion.site/Measuring-Global-Discovery-Signals-of-K-Pop-from-User-Playlists-2025-2cc537d1e6d98067abb4d60ef65313d5?source=copy_link

### Key Takeaways:

- Playlist inclusion is relatively rare (only 13% of the sample), but is concentrated among tracks with high popularity scores.
- Track popularity is a strong predictor of inclusion, but does not fully explain engagement differences.
- Even after controlling for artist and track features, playlisted tracks show higher engagement.
- Big 4 affiliation and gender continue to have an effect even after adjustment, suggesting there is also a structural dynamic involved.
- Playlist inclusion and popularity reinforce one another and are likely to be influenced by unobserved promotional, social, and algorithmic mechanisms.
