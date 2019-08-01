
#SET THE FOLLOWING ENVIRONMENT VARIABLES BEFORE RUNNING THIS PROGRAM:
    # SPOTIPY_CLIENT_ID
    # SPOTIPY_CLIENT_SECRET
    # SPOTIPY_REDIRECT_URI

import spotipy
import spotipy.util as util


scope = 'user-library-read'

token = util.prompt_for_user_token("harry.roxas11", scope) #CHANGE FIRST PARAMETER TO YOUR SPOTIFY DEVELOPER ACCOUNT

#Open file with track ids and their spotify ids and save to dictionary
all_tracks = {}
with open("track_tags2.txt") as f:
    all_tracks = dict(x.rstrip().split(None, 1) for x in f)

if token: #Check if succesful connection to spotify api
    sp = spotipy.Spotify(auth=token)

    #GET SPOTIFY AUDIO FEATURES FOR EACH TRACK
    with open("dataset.csv", 'w') as f: #save to csv file
        for id in all_tracks.keys():
            all_tracks[id] = eval(all_tracks[id])

            spotifyID = all_tracks[id][2]
            try:
                features = sp.audio_features(spotifyID)[0] #api call to get spotify audio features
                
                f.write("%s,%f,%f,%f,%f,%f,%f,%s\n" % (id,features['danceability'],features['acousticness'],features['energy'],features['loudness'],features['tempo'],features['valence'],all_tracks[id][0]))
            except spotipy.client.SpotifyException: # catch if token expires to renew token
                token = util.prompt_for_user_token("harry.roxas11", scope)
                sp = spotipy.Spotify(auth=token)

                features = sp.audio_features(spotifyID)[0]
                
                f.write("%s,%f,%f,%f,%f,%f,%f,%s\n" % (id,features['danceability'],features['acousticness'],features['energy'],features['loudness'],features['tempo'],features['valence'],all_tracks[id][0]))