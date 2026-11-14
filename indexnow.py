#!/usr/bin/env python3
# Ilmoittaa Bingille (ja muille IndexNow-hakukoneille) sivuston kaikista sivuista.
# ChatGPT:n haku nojaa pitkälti Bingin indeksiin, joten tämä nopeuttaa näkymistä tekoälyhauissa.
#
# Käyttö sen jälkeen, kun muutokset ovat julkaistu (PR yhdistetty ja Cloudflare julkaissut):
#     python3 indexnow.py
# Vastaus 200 tai 202 = vastaanotettu.

import json
import re
import urllib.request

HOST = "www.autokuntoon.fi"
KEY = "c1d16850901ba98a2c5880f6ce5c9e1c"  # sama kuin juuren tiedosto c1d16850901ba98a2c5880f6ce5c9e1c.txt

with open("sitemap.xml", encoding="utf-8") as f:
    urls = re.findall(r"<loc>(.*?)</loc>", f.read())

data = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": urls,
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8"},
)
with urllib.request.urlopen(req) as resp:
    print(f"{len(urls)} osoitetta lähetetty, vastaus: {resp.status}")
