# TODO: (1) Fix hack around artist attribute values including commas
from urllib.request import Request, urlopen
import re
import pandas as pd
# Scrape js file, pretending to be a browser to avoid being blocked
req = Request(
    url="https://spotle.io/_app/immutable/chunks/mysteryArtists.tSfo5sab.js",
    headers={'User-Agent': 'Mozilla/5.0'}
)
jscode= urlopen(req).read()

# Grab the Pp array from the js code and extract artist info into a data frame
res = re.compile(r"const Pp=\[(.*)\]", re.MULTILINE).findall(str(jscode))
res2 = re.compile(r"\{(index[^\}]*)\}").findall(res[0])

artist_array = []
pattern3 = re.compile(r"([^,\:]*)\:([^,]*)")
for artist in res2:
    artist_dictionary = {}
    for attribute in pattern3.findall(artist):
        # Regex above assumes entries wont contain commas, which some actually do. Hack to handle this
        if not (attribute[0].startswith(" ")):
            artist_dictionary[attribute[0].replace('"','')] = attribute[1].replace('"','')
    artist_array.append(artist_dictionary)
df = pd.DataFrame(artist_array)

df.to_csv("Spotle_artist_list.csv",index=False)