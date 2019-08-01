import os
import sqlite3
import json


if __name__ == '__main__':
    chosen_tracks = {}
    all_tracks = {}

    #Open file with track ids and tags and save to dictionary
    with open("track_tags.txt") as f:
        chosen_tracks = dict(x.rstrip().split(None, 1) for x in f)

    #Open file that contains all tracks and their information
    with open("unique_tracks.txt") as f:
        songs = f.readlines()

        #Match track ids with song ids
        for song in songs:
            info = song.split("<SEP>")
            all_tracks[info[0]] = info[1]

    #Get the corresponding song id for the chosen tracks
    for id in chosen_tracks.keys():
        chosen_tracks[id] = eval(chosen_tracks[id])
        chosen_tracks[id].append(all_tracks[id])

    #FIND THE TRACKS WITH AVAILABLE SPOTIFY IDS IN THE DATA
    unmatched_tracks = []
    for id in chosen_tracks.keys():
        chosen_tracks[id] = eval(chosen_tracks[id])
        sid = chosen_tracks[id][1]

        basepath = 'millionsongdataset_echonest/' #path of file that contains the spotify ids
        #traverse each folder in the path
        with os.scandir(basepath) as folders:
            for folder in folders:
                if(sid[slice(2,4)] == folder.name): #match song id with the folder
                    with os.scandir(folder) as entries:
                        for entry in entries:
                            matched = False
                            if(sid == entry.name[slice(18)] and entry.is_file()): #if song id matches with a file
                                matched = True
                                with open(basepath + folder.name + '/' + entry.name, 'r') as f:
                                    track_dict = json.load(f)
                                
                                #match song id with the songs in the file
                                songs = track_dict['response']['songs'] 
                                if(len(songs) > 0):
                                    for i in range(len(songs)):
                                        song_id = songs[i]['id']
                                        if(sid == song_id):
                                            tracks = songs[i]['tracks']
                                            if(len(tracks) > 0):
                                                count = 0
                                                #fetch the corresponding spotify id for the current song id
                                                for j in range(len(tracks)):
                                                    if(tracks[j]['catalog'] == 'spotify'):
                                                        count = count + 1
                                                        chosen_tracks[id].append(tracks[j]['foreign_id'])
                                                if count == 0:
                                                    matched = False
                                            else:
                                                matched = False
                                        else:
                                            matched = False
                                else:
                                    matched = False
                            if matched:
                                break
                        if not matched: #if song id does not match with any spotify id
                            unmatched_tracks.append(id)

    #remove all tracks with no matching spotify id
    for id in unmatched_tracks:
        chosen_tracks.pop(id)


    #FIND THE FINAL COUNT OF TRACKS PER EMOTION
    happy_count = 0
    sad_count = 0
    relaxed_count = 0
    angry_count = 0
    ambiguous_count = 0

    for id in chosen_tracks.keys():
        if chosen_tracks[id][0] == 'happy':
            happy_count = happy_count + 1
        elif chosen_tracks[id][0] == 'sad':
            sad_count = sad_count + 1
        elif chosen_tracks[id][0] == 'relaxed':
            relaxed_count = relaxed_count + 1
        elif chosen_tracks[id][0] == 'angry':
            angry_count = angry_count + 1
        elif chosen_tracks[id][0] == 'ambiguous':
            ambiguous_count = ambiguous_count + 1
    
    print("Happy Tracks: ", happy_count)
    print("Sad Tracks: ", sad_count)
    print("Relaxed Tracks: ", relaxed_count)
    print("Angry Tracks: ", angry_count)
    print("Ambiguous Tracks: ", ambiguous_count)

    #Save the new list of track ids with their spotify id in a new file
    with open('track_tags2.txt', 'w') as f:
        for k in chosen_tracks.keys():
            f.write("%s %s\n" % (k, chosen_tracks[k]))