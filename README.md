# autokuntoon-site

Autokuntoon.fi:n verkkosivusto: auton sisäpesu kotipihalla Turussa.

Sivusto on tavallista HTML:ää ja CSS:ää. Sivujen HTML tuotetaan skriptillä `build.py`: tekstit, hinnat ja sivut ovat siellä. Muokkaa `build.py`:tä ja aja `python3 build.py`, niin kaikki sivut ja `sitemap.xml` päivittyvät. Tuotetut HTML-tiedostot tallennetaan repoon, joten Cloudflare julkaisee ne sellaisenaan.

## Rakenne

| Tiedosto | Mitä se on |
|---|---|
| `index.html` | Etusivu |
| `hinnat-ja-palvelut/index.html` | Hinnat ja palvelut |
| `tyoen-jaelkeae-kuvina/index.html` | Ennen ja jälkeen -kuvat |
| `usein-kysytyt-kysymykset/index.html` | UKK |
| `oppaat/…/index.html` | Hakusanoihin kohdistetut oppaat |
| `build.py` | Tuottaa kaikki sivut |
| `ota-yhteyttae/index.html` | Yhteystiedot |
| `assets/style.css` | Kaikkien sivujen ulkoasu |
| `images/` | Kuvat (lisätään myöhemmin) |
| `sitemap.xml`, `robots.txt` | Hakukoneille: mitä sivuja on ja saa indeksoida |
| `llms.txt` | Tekoälyhauille (GEO): tiivis kuvaus yrityksestä |

Osoitteet ovat samat kuin vanhassa Webador-sivustossa, joten Googlen jo löytämät linkit toimivat jatkossakin.

## SEO ja GEO

- Jokaisella sivulla on oma otsikko (`<title>`), kuvausteksti ja yksi H1-pääotsikko.
- Etusivulla ja hintasivulla on rakenteinen data (schema.org `AutoWash`): palvelut, hinnat, alue ja yhteystiedot.
- UKK-sivulla on `FAQPage`-rakenteinen data, josta Google ja tekoälyt voivat poimia vastauksia suoraan.

## Esikatselu omalla koneella

```
python3 -m http.server 8000
```

Avaa sitten selaimessa http://localhost:8000
