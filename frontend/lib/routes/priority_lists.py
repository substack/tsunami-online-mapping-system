from __common__ import *
import simplejson as json

@get('/data/priority-lists/get')
def priority_lists(request) :
    return json.dumps([
        {
            "name" : "1",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_1.kml",
        },
        {
            "name" : "2",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_2.kml",
        },
        {
            "name" : "3",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_3.kml",
        },
        {
            "name" : "4",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_4.kml",
        },
        {
            "name" : "5",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_5.kml",
        },
        {
            "name" : "6",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_6.kml",
        },
        {
            "name" : "7",
            "kml" : "http://burn.giseis.alaska.edu/kml/priority_list_7.kml",
        },
    ]);
