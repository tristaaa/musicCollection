from flask import Flask,render_template,request,jsonify
import requests
import json
from collections import Counter
import re


app = Flask(__name__)

musicurl = 'https://music-7f27a.firebaseio.com/music.json'

@app.route("/")
def hello():
    return render_template("index.html")

def processRepData(repData,sidlist):
    if repData!=None:
        sids = repData
        if type(sids) == int:
            sidlist += [sids]
        else:
            sidlist += sids

@app.route("/searchkeyword", methods=['POST'])
def searchkeyword():
    keyword = request.form.get('keyword')
    artdata = request.form.get('arts')
    gendata = request.form.get('gens')
    yrdata = request.form.get('yrs')
    page = request.form.get("page")

    songlist,sidlist,result_list,alist,glist,ylist = [],[],[],[],[],[]
    if keyword!=None and keyword!='': # keyword search
        search_words = str(keyword).lower()
        # for each word in the keyword, search in each metadata to get the list of matched sids
        for search_word in search_words.split():
            titleurl = musicurl[:-10]+'titles/'+search_word+'.json'
            albumurl = musicurl[:-10] + 'albums/'+search_word+'.json'
            artisturl = musicurl[:-10] + 'artists/'+search_word+'.json'
            genreurl = musicurl[:-10] + 'genres/'+search_word+'.json'
            yearurl = musicurl[:-10] + 'years/'+search_word+'.json'
            durationurl = musicurl[:-10] + 'durations/'+search_word+'.json'

            response_data = requests.get(titleurl).json()
            processRepData(response_data,sidlist)

            response_data = requests.get(albumurl).json()
            processRepData(response_data, sidlist)

            response_data = requests.get(artisturl).json()
            processRepData(response_data, sidlist)

            response_data = requests.get(genreurl).json()
            processRepData(response_data, sidlist)

            response_data = requests.get(yearurl).json()
            processRepData(response_data, sidlist)

            response_data = requests.get(durationurl).json()
            processRepData(response_data, sidlist)

        if len(sidlist)>0:
            minsid = str(min(sidlist))
            maxsid = str(max(sidlist))
            songs = requests.get(musicurl+'?orderBy="sid"&startAt='+minsid+'&endAt='+maxsid).json()
            for sid_tuple in Counter(sidlist).most_common(): # in the order of most matching to least matching
                songlist.append(songs.get(str(sid_tuple[0])))
    else:
        songlist = requests.get(musicurl).json()

    if (artdata==None and gendata==None and yrdata==None) \
        or (artdata=='[]' and gendata=='[]' and yrdata=='[]'):
        result_list = songlist[:]
    else: # for facet search, get filtered result: result_list
        for song in songlist:
            if artdata!=None and artdata!='[]':
                arts = re.sub(",[\s]+", ",", song.get('artist')).split(',')
                if all(a not in artdata for a in arts): continue
            if gendata!=None and gendata!='[]':
                if song.get('genre') not in gendata: continue
            if yrdata!=None and yrdata!='[]':
                if str(song.get('year')) not in yrdata:continue
            result_list.append(song)
    
    # return the content of the facet, only show the top 5 results
    for song in result_list:
        arts = song.get('artist')
        alist.extend(re.sub(",[\s]+", ",", arts).split(','))
        glist.append(song.get('genre'))
        ylist.append(song.get('year'))
    alist = Counter(alist).most_common(5)
    glist = Counter(glist).most_common(5)
    ylist = Counter(ylist).most_common(5)

    # Pagination
    N = 10 # show 10 records in one page
    show_first_page = 0
    page = int(page)
    if page > 1:
        show_first_page = 1
    offset = (page-1)*N # start index of record
    count = len(result_list) # total records count
    total = (count+9)//10 # total page number
    page_list = get_page_list(total,page) # a list of shown page numbers, default show 5 pages
    result_list = result_list[offset:offset+N] # one page record
    
    ret_data = {
        "result_list":result_list,
        "page":page,"count":count,"total":total,"show_first_page":show_first_page,"page_list":page_list,
        "alist":alist,"glist":glist,"ylist":ylist
    }
    return jsonify(ret_data)


def get_page_list(total,page):
    show_page = 5   
    pageoffset = 2  
    start = 1    
    end = total  

    if total > show_page:
        if page > pageoffset:
            start = page - pageoffset
            if total > page + pageoffset:
                end = page + pageoffset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
        if page + pageoffset > total:
            start = start - (page + pageoffset - end)
    page_list = [i for i in range(start, end + 1)]
    return page_list

if __name__ == "__main__":
    app.run()
