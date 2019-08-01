import os
import sys
import sqlite3
import random

#function to sanitize a tag so it can be included or queried in the db
def sanitize(tag):
    tag = tag.replace("'","''")
    return tag

if __name__ == '__main__':

    dbtags = 'lastfm_tags.db' #DB for lastFM tags
    dblyrics = 'mxm_dataset.db' #DB for lyrics

    #Check if db exists
    if not os.path.isfile(dbtags):
        print('ERROR: db file %s does not exist?' % dbtags)

    #Connect to database
    conn = sqlite3.connect(dbtags) 

    #Merge lyrics database with tags database
    sql = "ATTACH DATABASE '%s' AS dblyrics" %dblyrics
    conn.execute(sql)

    #FIND TRACKS THAT MATCH THE GIVEN TAGS
    basepath = 'tags/' #path of files that contain the tags
    track_tags= {}
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                fh = open('tags/' + entry.name, "r")
                tags = fh.readlines()
                
                #FIND UNIQUE TRACKS IN THE DB WITH THE CURRENT EMOTION TAG AND HAS AVAILABLE LYRICS
                for tag in tags:
                    sql = "SELECT tids.tid FROM tid_tag, tids, tags WHERE tids.tid IN (SELECT track_id FROM dblyrics.lyrics) AND tids.ROWID=tid_tag.tid AND tid_tag.tag=tags.ROWID AND tags.tag='%s'" % sanitize(tag.rstrip())
                    res = conn.execute(sql)
                    data = res.fetchall()
                    for id in data:
                        id = id[0]
                        if id in track_tags:
                            track_tags[id].append(entry.name.split(".")[0])
                        else:
                            track_tags[id] = [entry.name.split(".")[0]]

        print("Total tracks: ", len(track_tags))

        #COUNT TRACKS WITH MULTIPLE EMOTIONAL TAGS
        multi_tags_count = 0
        for id in track_tags.keys():
            if len(track_tags[id]) > 1:
                multi_tags_count = multi_tags_count + 1
        
        print("Tracks w/ multiple tags: ", multi_tags_count)

    #Close the DB connection
    conn.close()
    
    #COUNT THE NUMBERS OF TRACKS FOR EACH TAG
    vague_tracks = {}
    for id in track_tags.keys():
        track_tags[id] = eval(track_tags[id])
        if len(track_tags[id]) > 1:
            tag_count = {'happy' : 0, 'sad' : 0, 'angry' : 0, 'relaxed' : 0}
            for tag in track_tags[id]:
                if tag == 'happy':
                    tag_count['happy'] = tag_count['happy'] + 1
                elif tag == 'sad':
                    tag_count['sad'] = tag_count['sad'] + 1
                elif tag == 'angry':
                    tag_count['angry'] = tag_count['angry'] + 1
                else:
                    tag_count['relaxed'] = tag_count['relaxed'] + 1
            
            max_val = max(tag_count.values())
            max_tag = [k for k, v in tag_count.items() if v == max_val] 
            if(len(max_tag) > 1): #If there are emotion tags with equal count, mark as ambiguous
                track_tags[id] = ['ambiguous']
                vague_tracks[id] = max_tag
            else: #Else emotion with max tags becomes the final emotion of the track
                track_tags[id] = max_tag
    
    #Save the track ids and their tags to a file
    with open('track_tags.txt', 'w') as f:
        for k in track_tags.keys():
            f.write("%s %s\n" % (k, track_tags[k]))

    #Save tracks with ambiguous tag to a separate file
    with open('vague_tracks.txt', 'w') as f:
        for k in vague_tracks.keys():
            f.write("%s %s\n" % (k, vague_tracks[k]))

     