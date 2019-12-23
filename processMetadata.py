#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import json
import requests
from lxml import etree
import eyed3
from google.cloud import storage

def extractMetadata(song,sid):
    metadataDic = {}
    sg = eyed3.load(song)

    metadataDic['sid'] = sid
    metadataDic['title'] = sg.tag.title
    metadataDic['album'] = sg.tag.album

    if ';' in sg.tag.artist:
        sg.tag.artist=sg.tag.artist.replace(';',', ')
    elif '&' in sg.tag.artist:
        sg.tag.artist=sg.tag.artist.replace('&',', ')
    metadataDic['artist'] = sg.tag.artist

    try:
        None != sg.tag.genre
    except AttributeError as e:
        metadataDic['genre'] = sg.tag.genre.name

    metadataDic['year'] = sg.tag.getBestDate().year
    time_secs = sg.info.time_secs
    m,s = divmod(time_secs, 60)
    metadataDic['duration'] = '{0:02d}:{1:02d}'.format(m,s)

    return metadataDic
 
def inverseMetadata_old(url):
    response = requests.get(url)
    songlist = response.json()

    titles,albums,artists,genres,years,durations = {},{},{},{},{},{}
    sidls = []
    for v in songlist:
        sid = v.get('sid')
        title = v.get('title').lower()
        album = v.get('album').lower()
        artist = v.get('artist').lower()
        genre = v.get('genre').lower()
        year = v.get('year')
        duration = v.get('duration')

        titles[title] = sid

        if albums.get(album) == None:
            albums[album] = [sid]
        else:
            sidls = albums.get(album)
            if sid not in sidls:
                sidls.append(sid)
                albums[album] = sidls

        artistlist = artist.split(',')
        for atst in artistlist:
            atst = atst.strip()
            if artists.get(atst) == None:
                artists[atst] = [sid]
            else:
                sidls = artists.get(atst)
                if sid not in sidls:
                    sidls.append(sid)
                    artists[atst] = sidls

        if genres.get(genre) == None:
            genres[genre] = [sid]
        else:
            sidls = genres.get(genre)
            if sid not in sidls:
                sidls.append(sid)
                genres[genre] = sidls

        if years.get(year) == None:
            years[year] = [sid]
        else:
            sidls = years.get(year)
            if sid not in sidls:
                sidls.append(sid)
                years[year] = sidls

        if durations.get(duration) == None:
            durations[duration] = [sid]
        else:
            sidls = durations.get(duration)
            if sid not in sidls:
                sidls.append(sid)
                durations[duration] = sidls

    # to facilitate further search task, inverse each metadate
    titleurl = url[:-10]+'titles.json'
    rep=requests.put(titleurl, json.dumps(titles))
    print(rep.text)

    albumurl = url[:-10]+'albums.json'
    requests.put(albumurl, json.dumps(albums))

    artisturl = url[:-10]+'artists.json'
    res=requests.put(artisturl, json.dumps(artists))

    genreurl = url[:-10]+'genres.json'
    requests.put(genreurl, json.dumps(genres))

    yearurl = url[:-10]+'years.json'
    requests.put(yearurl, json.dumps(years))

    durationurl = url[:-10]+'durations.json'
    requests.put(durationurl, json.dumps(durations))
    
def inverseMetadata(url):
    titles,albums,artists,genres,years,durations = {},{},{},{},{},{}
    sidls = []
    songlist = requests.get(url).json()
    for v in songlist:
        sid = v.get('sid')
        title = v.get('title').lower()
        album = v.get('album').lower()
        artist = v.get('artist').lower()
        genre = v.get('genre').lower()
        year = v.get('year')
        duration = v.get('duration')

        split_tlt = title.split()
        for st in split_tlt:
            if titles.get(st) == None:
                titles[st] = [sid]
            else:
                sidls = titles.get(st)
                if sid not in sidls:
                    sidls.append(sid)
                    titles[st] = sidls

        split_ablum = album.split()
        for sa in split_ablum:
            if albums.get(sa) == None:
                albums[sa] = [sid]
            else:
                sidls = albums.get(sa)
                if sid not in sidls:
                    sidls.append(sid)
                    albums[sa] = sidls

        artistlist = artist.split(',')
        for atst in artistlist:
            atst = atst.strip()
            split_art = atst.split()
            for sa in split_art:
                if artists.get(sa) == None:
                    artists[sa] = [sid]
                else:
                    sidls = artists.get(sa)
                    if sid not in sidls:
                        sidls.append(sid)
                        artists[sa] = sidls

        if genres.get(genre) == None:
            genres[genre] = [sid]
        else:
            sidls = genres.get(genre)
            if sid not in sidls:
                sidls.append(sid)
                genres[genre] = sidls

        if years.get(year) == None:
            years[year] = [sid]
        else:
            sidls = years.get(year)
            if sid not in sidls:
                sidls.append(sid)
                years[year] = sidls

        if durations.get(duration) == None:
            durations[duration] = [sid]
        else:
            sidls = durations.get(duration)
            if sid not in sidls:
                sidls.append(sid)
                durations[duration] = sidls

    # to facilitate further search task, inverse each metadate
    titleurl = url[:-10]+'titles.json'
    rep=requests.put(titleurl, json.dumps(titles))

    albumurl = url[:-10]+'albums.json'
    requests.put(albumurl, json.dumps(albums))

    artisturl = url[:-10]+'artists.json'
    res=requests.put(artisturl, json.dumps(artists))

    genreurl = url[:-10]+'genres.json'
    requests.put(genreurl, json.dumps(genres))

    yearurl = url[:-10]+'years.json'
    requests.put(yearurl, json.dumps(years))

    durationurl = url[:-10]+'durations.json'
    requests.put(durationurl, json.dumps(durations))



def uploadFiles(file_path):
    client = storage.Client.from_service_account_json('551musickey.json')
    bucket = client.get_bucket('music-7f27a.appspot.com')
    file_name = file_path[6:]
    blob = storage.Blob(file_name, bucket)

    with open(file_path, 'rb') as my_file:
        blob.upload_from_file(my_file, content_type="audio/mp3")
        blob.make_public()
        download_url = blob.public_url
        return download_url

def uploadPics(file_path):
    client = storage.Client.from_service_account_json('551musickey.json')
    bucket = client.get_bucket('music-7f27a.appspot.com')
    file_name = 'images/'+file_path[6:-3]+'png'
    blob = storage.Blob(file_name, bucket)

    try:
        with open(file_name, 'rb') as my_file:
            blob.upload_from_file(my_file, content_type="image/png")
            blob.make_public()
            pic_src = blob.public_url
            return pic_src
    except FileNotFoundError as e:
        print('Error:----',e)
        return None


def main(argv):
    file_dir = argv[1]
    songlist = []
    n=77
    url = 'https://music-7f27a.firebaseio.com/music.json'
    # url = 'https://music-7f27a.firebaseio.com/music/'+str(n)+'.json'
    sid = 0

    # for root, dirs, files in os.walk(file_dir):  
    #     for file in sorted(files):
    #         if(os.path.splitext(file)[1]=='.mp3'):
    #             if sid==n:
    #                 song = os.path.join(root, file)
    #                 metadataDic={}
    #                 metadataDic = extractMetadata(song,sid) 
    #                 # metadataDic['download_url'] = uploadFiles(song)
    #                 metadataDic['pic_src'] = uploadPics(song)
    #                 title = metadataDic.get('title') 
    #                 songlist.append(metadataDic)
    #             sid +=1

    # # jsondata = json.dumps(songlist)
    # # response_data = requests.put(url, jsondata)
    # jsondata = json.dumps(songlist[0])
    # response_data = requests.patch(url, jsondata)
    inverseMetadata(url)




if __name__ == '__main__':
    main(sys.argv)
    

