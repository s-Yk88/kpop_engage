import pandas as pd
import numpy as np
import seaborn as sns
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

##Accessing Spotify API -- can gain access key by registering with Spotify for Developers (Documentation is also pretty thorough)
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-private"  # minimal scope for login test
))

user = sp.current_user()
print("Logged in as:", user["display_name"])


### Exploring the spotify API

## Getting an idea of the results of running a artist/ track search -- also helps us figure out the artist ids
#sp.track('6m1TWFMeon7ai9XLOzdbiR')#BTS id= '3Nrfpe0tUJi4K4DXYWgMUX'
#sp.track('3CYH422oy1cZNoo0GTG1TK')#Red Velvet '1z4g3DjTBBZKhvAroFlhOM'
#sp.track('5H1sKFMzDeMtXwND3V6hRY')#Black Pink '41MozSoPIsD1dJM0CLPjZF'
#sp.track('3zhbXKFjUDw40pTYyCgt1Y')# Twice '7n2Ycct7Beij7Dj7meI4X0'
#sp.track('6I2tqFhk8tq69iursYxuxd')#Seventeen '7nqOGRxlXj7N2JYbgNEjYH'
#sp.track('5BXr7hYZQOeRttkeWYTq5S')#Stayc '01XYiBYaoMJcNhPokrg0l0'
sp.artist('1z4g3DjTBBZKhvAroFlhOM')

## Getting an artist's top tracks
h=sp.artist_top_tracks('1z4g3DjTBBZKhvAroFlhOM') # Looking specifically at Red Velvet
track_data=[]
for item in h['tracks']:
    track=item
    if track:
        track_data.append({
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'duration_ms':track['duration_ms'],
            'album':track['album']['name'],
            'release_date': track['album']['release_date'],
            'popularity': track['popularity']
            })
df = pd.DataFrame(track_data)
df # dataframe returns 10 (max) rows of  the track name, artist, duration, album name, release date included in the top track list on an artist's spotify profile



#### CREATING MAIN DATASET

### Track Metadata

## Pull the top track track metadata from each of the chosen groups
artist_names = ["BTS", "BLACKPINK", "TWICE", "SEVENTEEN", "Stray Kids", "NCT 127", "NCT DREAM", "ENHYPEN", "TXT", "NewJeans",
                "IVE", "ITZY", "(G)I-DLE", "ATEEZ", "LE SSERAFIM", "Red Velvet", "EXO", "SHINee", "STAYC", "BABYMONSTER",
                "BOYNEXTDOOR", "xikers", "NMIXX", "Kep1er", "CRAVITY", "Billlie", "H1-KEY", "RIIZE"]

artist_ids=['3Nrfpe0tUJi4K4DXYWgMUX','41MozSoPIsD1dJM0CLPjZF','7nqOGRxlXj7N2JYbgNEjYH','2dIgFjalVxs4ThymZ67YCE','7f4ignuCJhLXfZ9giKT7rH',
            '1gBUSTR3TyDdTVFIaQnc02','5t5FqBwTcgKTaWmfEbwQY9','0ghlgldX5Dd6720Q3qFyQB','6HvZYsbFfjnjFrWF950C9d','6RHTUrRF63xao58xh9FXYJ',
            '2KC9Qb60EaY0kW4eH68vr3', '2AfmfGFbe0A0WsTYm0SDTx','68KmkJeZGfwe1OUaivBa2L','4SpbR6yFEvexJuaBpgAU5p','1z4g3DjTBBZKhvAroFlhOM',
            '3cjEqqelV9zb4BYE3qDQ4O','2hRQKC0gqlZGPrmUKbcchR','01XYiBYaoMJcNhPokrg0l0','1SIocsqdEefUTE6XKGUiVS','4hnHLgMSOiqERWBL4jINP1',
            '6QHP8St0MzfNDqjKpwtMht','28ot3wh4oNmoFOdVajibBl','5R7AMwDeroq6Ls0COQYpS4', '6FkhUhUwSPl3mGB6mmE8wn','2GQxKDojobwBjZMPf7aoh0',
            '5GwQwY63I9hrUUFlQB8FYU','2jOm3cYujQx6o1dxuiuqaX']


def get_top_tracks(artist_ids,sp):
    track_data=[]
    for a in artist_ids:
        t=sp.artist_top_tracks(a)
        for item in t['tracks']:
            track = item
            if track:
                track_data.append({
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'duration_ms':track['duration_ms'],
                    'album':track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity']
                    })
    df = pd.DataFrame(track_data)
    return df

df=get_top_tracks(artist_ids,sp)


df.head(20)
df=df.drop_duplicates() # there is one song with multiple groups on it. To reduce confusion, I am only keeping it for one group where its ranked higher
len(df) #269 tracks



## Collaborations where the other artist is the first artist:

# some artist top tracks include collaborations so we will correct so that we look at only the kpop group as the main artist-- 
# to do that we'll create a new variable 'associated_kpop_group' that pulls the secondary artist of tracks (as often, collaborations with bigger artists, 
# list the bigger artist as the primary artist) and ultimately will use this column to correct any row that may encounter a different primary artist
western_to_korean={
"K/DA":"i-dle", 
"Coldplay":"BTS",
"Charlie Puth" :"BTS",
"JVKE":"TOMORROW X TOGETHER",
"SLANDER":'SEVENTEEN'}

df['associated_kpop_group']=0

for i in df.index:
    if df.loc[i, 'artist'] == 'K/DA':
        df.loc[i,'associated_kpop_group']= "i-dle"
    elif df.loc[i,'artist'] == 'Coldplay':
        df.loc[i,'associated_kpop_group']= 'BTS'
    elif df.loc[i,'artist']== 'Charlie Puth':
        df.loc[i,'associated_kpop_group']='BTS'
    elif df.loc[i,'artist']=='JVKE':
        df.loc[i,'associated_kpop_group']='TOMORROW X TOGETHER'
    elif df.loc[i,'artist']=='SLANDER':
        df.loc[i,'associated_kpop_group']='SEVENTEEN'
    else:
        df.loc[i,'associated_kpop_group']=df.loc[i,'artist']


df.query('artist=="JVKE"')


## Given track name, link track id, just in case
def get_spotify_track_id(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    items = results.get('tracks', {}).get('items')
    if items:
        return items[0]['id']
    return None

df['spotify_track_id'] = df.apply(lambda row: get_spotify_track_id(row['track_name'], row['artist']),axis=1)


### Artist Metadata
# Pulls artist id, ,followers, popularity score and genre metadata
# Caveat: Must get it to match the associated kpop group rather than any collaborators that may take top billing
import time
def get_artist_info(track_id):
    try:
        #collab=['4gzpq5DPGxSnKTe4SA8HAU','6VuMaDnrHyPL1p4EHjYLi7','164Uj4eKjl6zTBKfJLFKKK']
        track = sp.track(track_id)
        if track['artists'][0]['id']=='4gzpq5DPGxSnKTe4SA8HAU' or track['artists'][0]['id']=='6VuMaDnrHyPL1p4EHjYLi7'or track['artists'][0]['id']=='164Uj4eKjl6zTBKfJLFKKK':
            artist_id=track['artists'][1]['id']
        elif track['artists'][0]['id']=='4gOc8TsQed9eqnqJct2c5v': #K/DA
            artist_id='2AfmfGFbe0A0WsTYm0SDTx' 
        else:
            artist_id = track['artists'][0]['id']

        artist = sp.artist(artist_id)
        time.sleep(0.5)
        x= pd.Series({
            'artist_id':artist['id'],
            'artist_followers': artist['followers']['total'],
            'artist_popularity': artist['popularity'],
            'artist_genres': ', '.join(artist['genres'])
        })
        return x
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify error on track {track_id}: {e}")
    except Exception as e:
        print(f"General error on track {track_id}: {e}")

    # Return default if failed
    return pd.Series({
        'artist_id':None,
        'artist_followers': None,
        'artist_popularity': None,
        'artist_genres': None
    })
df[['artist_id','artist_followers', 'artist_popularity', 'artist_genres']] = df['spotify_track_id'].apply(get_artist_info)


# double check artist inclusion:
df['artist'].unique()



### User Playlist Exposure
import time 

def count_playlist_inclusions(sp, df, search_queries, playlist_limit):
    
    
    track_to_playlists = {}  # track_id → list of playlist IDs

    print(f"Searching across {len(search_queries)} keyword(s): {search_queries}")

  # 1. Search for playlists by keyword and return unique playlists
    for query in search_queries:
        print(f"Searching playlists for: '{query}'")
        h = sp.search(q=query, type='playlist', limit=playlist_limit)
        playlist_ids = set(p['id'] for p in h['playlists']['items']if p!=None)  # we no longer have to filter out spotify editorial-- can't even access
    
  # 2. Gather track appearances in those unique playlists
    for p in playlist_ids:
        pid=p
        try:
            tracks = sp.playlist_tracks(pid, market='US', limit=playlist_limit)['items']
            for item in tracks:
                track = item.get('track')
                if track and track.get('id'):
                    tid = track['id']
                    if tid not in track_to_playlists:
                        track_to_playlists[tid] = []
                    track_to_playlists[tid].append(pid)
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to load playlist {pid}: {e}")
            continue
    print(f"Total unique playlists scanned: {len(playlist_ids)}")
    print(f"Total unique tracks collected: {len(track_to_playlists)}")

    #3. Count appearances and track playlist sources
    df['user_playlist_count'] = df['spotify_track_id'].apply(lambda x: len(track_to_playlists.get(x, [])))

    df['which_user_playlists'] = df['spotify_track_id'].apply(lambda x: ','.join(track_to_playlists.get(x, [])) if x in track_to_playlists else '')

    print("Appended playlist inclusion columns to df")
    return df, list(playlist_ids)


search_queries=["hits","stan","korean","group","kpop","k-pop","k pop"] #not case sensitive-
#admittedly not too creative but the search function tends to fail if looking at more than 50 playlists

df_new,searched_playlists=count_playlist_inclusions(sp, df, search_queries, playlist_limit=50)

#27 unique playlists scanned across all queries
#333 total unique tracks on those playlists

df.sort_values(by='user_playlist_count',ascending=False).head(20) #can check which songs 




### Adding other publicly available Metadata (from outside of spotipy)

## Group Management (company name/ big4 code)
# adding more metadata/ covariates- management companies
company_metadata={
    "BTS":"Big Hit Music",
    "BLACKPINK":"YG Entertainment",
    "TWICE":"JYP Entertainment",
    "SEVENTEEN":"Pledis Entertainment",
    "Stray Kids":"JYP Entertainment",
    "NCT 127":"SM Entertainment",
    "NCT DREAM":"SM Entertainment",
    "ENHYPEN":"Belift Lab",
    "TOMORROW X TOGETHER":"Big Hit Music",
    "NewJeans":"ADOR",
    "IVE":"Starship Entertainment",
    "ITZY":"JYP Entertainment",
    "i-dle":"Cube Entertainment",
    'LE SSERAFIM':"Source Music",
    'Red Velvet':"SM Entertainment",
    'EXO':"SM Entertainment",
    'SHINee':"SM Entertainment",
    'STAYC':"High Up Entertainment",
    'BABYMONSTER':"YG Entertainment",
    'BOYNEXTDOOR':"KOZ Entertainment",
    'NMIXX':"SQU4D",
    'Kep1er':"WakeOne Entertainment",
    'CRAVITY':"Starship Entertainment",
    'xikers':'KQ Entertainment',
    'Billlie':"Mystic Story",
    'H1-KEY':"Grandline Group",
    'RIIZE':"SM Entertainment",
    'ATEEZ':"KQ Entertainment"
}
# Function to get associated group
def get_associated_management(artist):
    return company_metadata.get(artist,None)

# Apply function to create new column
df['company'] = df['associated_kpop_group'].apply(get_associated_management)
#df.head()

# adding big 4 code:
df['big4']=0
for i in df.index:
    if df.loc[i, 'company'] =='Big Hit Music' or df.loc[i, 'company'] =='YG Entertainment' or df.loc[i,'company']=='SM Entertainment' or df.loc[i,'company']=='Pledis Entertainment' or df.loc[i,'company']=='JYP Entertainment' or df.loc[i,'company']=='Belift Lab' or df.loc[i,'company']=='ADOR' or df.loc[i,'company']=='KOZ Entertainment' :
        df.loc[i, 'big4'] = 1
#df.tail(30)


## Gender 
gender_metadata={
    "BTS":"M",
    "BLACKPINK":"F",
    "TWICE":"F",
    "SEVENTEEN":"M",
    "Stray Kids":"F",
    "NCT 127":"M",
    "NCT DREAM":"M",
    "ENHYPEN":"M",
    "TOMORROW X TOGETHER":"M",
    "NewJeans":"F",
    "IVE":"F",
    "ITZY":"F",
    "i-dle":"F",
    'LE SSERAFIM':"F",
    'Red Velvet':"F",
    'EXO':"M",
    'SHINee':"M",
    'STAYC':"F",
    'BABYMONSTER':"F",
    'BOYNEXTDOOR':"M",
    'NMIXX':"F",
    'Kep1er':"F",
    'CRAVITY':"M",
    'xikers':'M',
    'Billlie':"F",
    'H1-KEY':"F",
    'RIIZE':"M",
    'ATEEZ':"M"
}
def get_associated_gender(artist):
    return gender_metadata.get(artist,None)

df['gender'] = df['associated_kpop_group'].apply(get_associated_gender)


## Debut - ultimately to be used as age marker for artist
debut_metadata={
    "BTS":"2013-06-13",
    "BLACKPINK":"2016-08-08",
    "TWICE":"2015-10-20",
    "SEVENTEEN":"2015-05-26",
    "Stray Kids":"2018-03-25",
    "NCT 127":"2016-07-07",
    "NCT DREAM":"2016-08-25",
    "ENHYPEN":"2020-11-23",
    "TOMORROW X TOGETHER":"2019-03-04",
    "NewJeans":"2022-07-22",
    "IVE":"2021-12-01",
    "ITZY":"2019-02-12",
    "i-dle":"2018-05-18",
    'LE SSERAFIM':"2022-05-02",
    'Red Velvet':"2014-08-01",
    'EXO':"2012-04-08",
    'SHINee':"2008-05-28",
    'STAYC':"2020-11-12",
    'BABYMONSTER':"2024-04-01",
    'BOYNEXTDOOR':"2023-05-23",
    'NMIXX':"2022-02-22",
    'Kep1er':"2022-01-03",
    'CRAVITY':"2020-04-14",
    'xikers':'2023-03-30',
    'Billlie':"2021-11-10",
    'H1-KEY':"2022-01-05",
    'RIIZE':"2023-09-04",
    'ATEEZ':"2018-10-24"
}
def get_debut(artist):
    return debut_metadata.get(artist,None)

df['debut'] = df['associated_kpop_group'].apply(get_debut)
df['debut']=pd.to_datetime(df['debut'])




### Making some of the variables a little more useful

## Track Recency
df['release_date']=pd.to_datetime(df['release_date'])
df['days_since_release'] = pd.to_datetime('2025-08-02') - df['release_date']
df['days_since_release']= df['days_since_release'].dt.days
#df.head()


## Group Age
df['age_days'] = pd.to_datetime('2025-08-02') - df['debut']
df['age_days']= df['age_days'].dt.days

## Main target variable - playlist exposure
df['playlist_exposure'] = (df['user_playlist_count'] > 0).astype(int)
