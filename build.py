import json, os, sys

# Tämä skripti tuottaa sivuston HTML-sivut, sitemap.xml:n mukaan lukien.
# Muokkaa tekstejä tässä tiedostossa ja aja: python3 build.py .
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SITE = "https://www.autokuntoon.fi"
PHONE = "+358442061100"
PHONE_TXT = "044 206 1100"
EMAIL = "autokuntoon.business@gmail.com"
WA = "https://wa.me/358442061100"
IG = "https://www.instagram.com/autokuntoon.fi/"
TT = "https://www.tiktok.com/@autokuntoon.fi"

NAV = [
    ("/", "Etusivu"),
    ("/hinnat-ja-palvelut/", "Hinnat ja palvelut"),
    ("/tyoen-jaelkeae-kuvina/", "Työn jälkeä kuvina"),
    ("/usein-kysytyt-kysymykset/", "Usein kysytyt"),
    ("/ota-yhteyttae/", "Ota yhteyttä"),
]

SERVICES = [
    ("Peruspesu", 55, "1 h", "Nopea perussiivous auton sisätiloille.",
     ["Roskien poisto", "Sisätilojen imurointi", "Pintojen pyyhintä",
      "Penkkien imurointi", "Ovien karmit ja tavaratila"]),
    ("Kattavapesu", 80, "2 h", "Perusteellisempi pesu, kun auto kaipaa enemmän huolenpitoa.",
     ["Kaikki peruspesun työt", "Pintojen pesu pyyhinnän sijaan",
      "Penkkien imurointi ja puhdistus", "Ikkunoiden sisäpinnat",
      "Lemmikkien karvojen poisto", "Kattoverhoilu ja turvavyöt tarvittaessa"]),
    ("Deluxe-pesu", 125, "4 h", "Paras lopputulos: penkit pestään tekstiilipesurilla.",
     ["Kaikki kattavapesun työt", "Penkkien syväpesu tekstiilipesurilla"]),
]
SEAT = ("Penkkien pesu tekstiilipesurilla", 50,
        "Pelkkä penkkien syväpesu esimerkiksi kahvitahroihin tai liasta tummuneisiin penkkeihin.")

FAQ = [
    ("Miten voin varata ajan?",
     "Varaa aika WhatsAppilla tai sähköpostilla. Kerro toive päivästä, auton sijainti ja haluamasi palvelu, niin vastaamme mahdollisimman pian."),
    ("Mitä minulta tarvitaan pesua varten?",
     "Vain pestävä auto ja sähköpistoke. Tuomme itse kaikki välineet ja pesuaineet."),
    ("Kauanko pesu kestää?",
     "Peruspesu kestää noin tunnin, kattavapesu noin kaksi tuntia ja Deluxe-pesu enintään neljä tuntia. Aika riippuu palvelusta ja auton kunnosta."),
    ("Mitä pesu maksaa?",
     "Peruspesu 55 €, kattavapesu 80 € ja Deluxe-pesu 125 €. Pelkkä penkkien pesu tekstiilipesurilla maksaa 50 €. Pakettiajan ylittävä työ on 30 €/h."),
    ("Millä alueella toimitte?",
     "Pääasiassa Turussa ja Turun seudulla, esimerkiksi Kaarinassa, Raisiossa, Naantalissa, Liedossa, Ruskolla, Maskussa ja Paimiossa. Yli 15 km Turun keskustasta lisätään sovittu polttoainemaksu."),
    ("Millä voin maksaa?",
     "Tilisiirrolla, käteisellä tai MobilePaylla. Maksu hoidetaan työn jälkeen."),
    ("Ovatko pesuaineet turvallisia?",
     "Kyllä. Käytämme auton sisätilojen puhdistukseen tarkoitettuja aineita, jotka ovat turvallisia sekä autolle että matkustajille."),
    ("Kuinka nopeasti saan ajan?",
     "Tarkistamme viestit päivittäin, joten aika voi järjestyä jopa samalle päivälle."),
    ("Poistatteko koiran ja kissan karvoja?",
     "Kyllä. Lemmikkien karvojen poisto kuuluu kattavapesuun (80 €) ja Deluxe-pesuun (125 €). Peruspesussa karvoja ei erikseen poisteta."),
    ("Lähtevätkö tupakan ja muut hajut pesussa?",
     "Pesu poistaa hajua aiheuttavaa likaa, ja varsinkin penkkien syväpesu tekstiilipesurilla vähentää kankaaseen imeytyneitä hajuja. Erillistä hajunpoistokäsittelyä, kuten otsonointia, emme tee, joten emme voi luvata, että pinttynyt haju lähtee kokonaan."),
    ("Puhdistatteko nahkapenkit?",
     "Kyllä. Nahkapenkit puhdistetaan pyyhkimällä. Tekstiilipesuria käytetään vain kangaspenkkeihin."),
    ("Pesettekö lastenistuimet?",
     "Kyllä. Kerro varauksen yhteydessä, montako istuinta autossa on, niin varaamme riittävästi aikaa."),
    ("Kuuluuko kattoverhoilu ja turvavyöt pesuun?",
     "Kyllä, kattavapesussa ja Deluxe-pesussa ne puhdistetaan, jos ne ovat likaiset."),
    ("Puhdistatteko ikkunat sisäpuolelta?",
     "Kyllä, ikkunoiden sisäpinnat kuuluvat kattavapesuun ja Deluxe-pesuun."),
    ("Teettekö pesuja talvella?",
     "Kyllä, kun auto on lämpimässä autotallissa tai hallissa. Ulkona pakkasella sisäpesua ei voi tehdä kunnolla."),
    ("Pesettekö pakettiautoja ja asuntoautoja?",
     "Kyllä. Niiden hinta sovitaan erikseen auton koon ja kunnon mukaan. Kerro auton malli viestissä, niin annamme hinta-arvion."),
    ("Pitääkö minun olla kotona pesun aikana?",
     "Ei tarvitse. Riittää, että auto on auki tai avaimet sovitussa paikassa ja sähköpistoke on käytettävissä."),
    ("Voinko perua varauksen?",
     "Kyllä. Peruutus on maksuton viimeistään 48 tuntia ennen sovittua aikaa. Myöhemmin perutuista tai unohtuneista varauksista veloitamme 20 €."),
]

REVIEWS = [
    ("Matias Herlevi", "Autokuntoon.fi:n palvelu oli erinomaista! Pesijät tulivat kotipihalleni ja auto on kuin uusi. Suosittelen lämpimästi."),
    ("Kasperi Kovanen", "Olen todella tyytyväinen Autokuntoon.fi:n palveluun. Henkilökunta oli ammattitaitoista ja ystävällistä, ja auto on nyt todella puhdas."),
    ("Markus Aaltonen", "Loistavaa ja huoletonta palvelua! Auto näyttää paremmalta kuin uutena, ja kaikki hoitui omalla pihalla."),
]


def business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "AutoWash",
        "@id": SITE + "/#yritys",
        "name": "Autokuntoon.fi",
        "description": "Auton sisäpesu asiakkaan kotipihalla Turussa ja Turun seudulla. Peruspesu, kattavapesu ja Deluxe-pesu tekstiilipesurilla.",
        "url": SITE + "/",
        "logo": SITE + "/images/logo.jpg",
        "image": [SITE + "/images/logo-og.jpg", SITE + "/images/bmw-ennen-jalkeen.jpg"],
        "email": EMAIL,
        "telephone": PHONE,
        "priceRange": "50–125 €",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Tilisiirto, käteinen, MobilePay",
        "taxID": "3525496-7",
        "address": {"@type": "PostalAddress", "addressLocality": "Turku", "addressCountry": "FI"},
        "areaServed": [{"@type": "City", "name": n} for n in ["Turku", "Kaarina", "Raisio", "Naantali", "Lieto", "Rusko", "Masku", "Paimio"]],
        "sameAs": [IG, TT],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Auton sisäpesupalvelut",
            "itemListElement": [
                {"@type": "Offer", "price": str(p), "priceCurrency": "EUR",
                 "itemOffered": {"@type": "Service", "name": n, "description": d}}
                for n, p, _, d, _ in SERVICES
            ] + [{"@type": "Offer", "price": str(SEAT[1]), "priceCurrency": "EUR",
                  "itemOffered": {"@type": "Service", "name": SEAT[0], "description": SEAT[2]}}],
        },
    }


def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ
        ],
    }


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def page(path, title, desc, body, schemas=()):
    canonical = SITE + path
    nav = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a></li>'
        for h, t in NAV
    )
    schema_html = "\n".join(ld(s) for s in schemas)
    return f"""<!doctype html>
<html lang="fi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="Autokuntoon.fi">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/images/logo-og.jpg">
  <meta name="theme-color" content="#2a2b2a">
  <link rel="icon" href="/assets/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&display=swap">
  <link rel="stylesheet" href="/assets/style.css">
{schema_html}
</head>
<body>
  <a class="skip" href="#sisalto">Siirry sisältöön</a>
  <header class="site-header">
    <div class="container">
      <a class="logo" href="/" aria-label="Autokuntoon.fi etusivu"><img src="/assets/logo-auto.png" alt="" width="240" height="102"><span>AUTOKUNTOON.FI</span></a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="valikko">Valikko</button>
      <nav class="site-nav" id="valikko" aria-label="Päävalikko">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="sisalto">
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="grid">
        <div>
          <h2>Autokuntoon.fi</h2>
          <p>Auton sisäpesu kotipihallasi Turussa ja Turun seudulla.</p>
        </div>
        <div>
          <h2>Yhteystiedot</h2>
          <ul>
            <li>WhatsApp: <a href="{WA}">{PHONE_TXT}</a></li>
            <li>Sähköposti: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Y-tunnus: 3525496-7</li>
          </ul>
        </div>
        <div>
          <h2>Seuraa meitä</h2>
          <ul>
            <li><a href="{IG}" rel="noopener">Instagram</a></li>
            <li><a href="{TT}" rel="noopener">TikTok</a></li>
          </ul>
          <h2 style="margin-top:16px">Toiminta-alue</h2>
          <ul>
            <li><a href="/alueet/auton-sisapesu-turku/">Turku</a> · <a href="/alueet/auton-sisapesu-kaarina/">Kaarina</a> · <a href="/alueet/auton-sisapesu-raisio/">Raisio</a></li>
            <li><a href="/alueet/auton-sisapesu-naantali/">Naantali</a> · <a href="/alueet/auton-sisapesu-lieto/">Lieto</a> · <a href="/alueet/">Kaikki alueet</a></li>
          </ul>
          <h2 style="margin-top:16px">Oppaat</h2>
          <ul>
            <li><a href="/oppaat/auton-sisapesun-hinta-turku/">Auton sisäpesun hinta Turussa</a></li>
            <li><a href="/oppaat/auton-sisapesu-ennen-myyntia/">Auton sisäpesu ennen myyntiä</a></li>
          </ul>
        </div>
      </div>
      <p class="copy">© 2025–2026 Autokuntoon.fi</p>
    </div>
  </footer>

  <script>
    // Mobiilivalikon avaus ja sulku
    const btn = document.querySelector('.nav-toggle');
    const nav = document.getElementById('valikko');
    btn.addEventListener('click', () => {{
      const open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    }});
  </script>
</body>
</html>
"""


def cta(title="Haluatko autosi puhtaaksi?", text="Varaa aika WhatsAppilla tai sähköpostilla. Tulemme kotipihallesi Turun seudulla."):
    return f"""    <section class="section cta">
      <div class="container">
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="btn-row">
          <a class="btn" href="{WA}">Varaa WhatsAppilla</a>
          <a class="btn ghost" href="mailto:{EMAIL}?subject=Ajanvaraus%20auton%20sis%C3%A4pesuun">Lähetä sähköpostia</a>
        </div>
      </div>
    </section>"""


def price_cards(link_more=False):
    out = []
    for i, (n, p, t, d, items) in enumerate(SERVICES):
        lis = "".join(f"<li>{x}</li>" for x in items)
        featured = " featured" if i == 1 else ""
        tag = '<span class="tag">Suosituin</span>' if i == 1 else ""
        out.append(f"""          <article class="card price-card{featured}">
            {tag}
            <h3>{n}</h3>
            <div class="price">{p} € <small>/ enintään {t}</small></div>
            <p>{d}</p>
            <ul>{lis}</ul>
            <a class="btn" href="/ota-yhteyttae/">Varaa {n.lower()}</a>
          </article>""")
    return "\n".join(out)


def placeholder(text):
    return f'<div class="placeholder">{text}</div>'


# ---------- Etusivu ----------
reviews_html = "\n".join(
    f"""          <blockquote class="card">
            <p>”{t}”</p>
            <footer>{n}</footer>
          </blockquote>""" for n, t in REVIEWS)

home = f"""    <section class="hero">
      <div class="container hero-grid">
        <div>
        <h1>Auton sisäpesu kotipihallasi Turussa</h1>
        <p>Tulemme luoksesi ja puhdistamme autosi sisätilat huolellisesti. Sinun ei tarvitse kuin avata ovet. Hinnat alkaen 55 €.</p>
        <div class="btn-row">
          <a class="btn" href="/hinnat-ja-palvelut/">Katso hinnat</a>
          <a class="btn ghost" href="/ota-yhteyttae/">Varaa aika</a>
        </div>
        <ul class="badges">
          <li>✓ Tulemme kotipihallesi</li>
          <li>✓ Turku ja Turun seutu</li>
          <li>✓ Maksu työn jälkeen</li>
        </ul>
        </div>
        <img class="hero-logo" src="/images/logo.jpg" alt="Autokuntoon.fi-logo: piirretty urheiluauto" width="640" height="640">
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Ennen ja jälkeen</h2>
        <p class="lead">BMW:n etuosa ennen ja jälkeen sisäpesun. Hiekat ja roskat pois lattioilta, penkit ja pinnat puhtaiksi.</p>
        <img class="wide-img" src="/images/bmw-ennen-jalkeen.jpg" alt="BMW:n etumatkustajan puoli ennen ja jälkeen auton sisäpesun: likainen ja hiekkainen lattia vasemmalla, puhdas oikealla" width="1600" height="902" loading="lazy">
        <p class="note"><a href="/tyoen-jaelkeae-kuvina/">Katso lisää kuvia töistämme</a></p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Miksi pestä auto meillä?</h2>
        <div class="grid four">
          <div class="card">
            <h3>Terveys</h3>
            <p>Autoon kertyy pölyä ja likaa, jotka voivat ärsyttää hengitysteitä. Puhdas sisätila tarkoittaa raikkaampaa ilmaa ja vähemmän tukkoista nenää.</p>
          </div>
          <div class="card">
            <h3>Helppous</h3>
            <p>Tulemme kotipihallesi. Sinä avaat auton ovet ja voit tehdä sillä aikaa muuta. Maksu hoidetaan vasta työn jälkeen.</p>
          </div>
          <div class="card">
            <h3>Auto kestää pidempään</h3>
            <p>Roskat, hiekka ja pöly kuluttavat sisustaa, ja penkkeihin kuivuneet läikät voivat aiheuttaa ongelmia. Säännöllinen pesu pitää auton hyvässä kunnossa.</p>
          </div>
          <div class="card">
            <h3>Edullinen hinta</h3>
            <p>Pienenä yrityksenä emme ole arvonlisäverovelvollisia, joten voimme pitää hinnat edullisina.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section soft">
      <div class="container">
        <h2>Palvelut ja hinnat</h2>
        <p class="lead">Kolme pakettia eri tarpeisiin. Pakettiajan ylittävä työ on 30 €/h, ja penkit voi pestä tekstiilipesurilla myös erikseen 50 €:lla.</p>
        <div class="grid three">
{price_cards()}
        </div>
        <p class="note"><a href="/hinnat-ja-palvelut/">Katso kaikki palvelut ja hinnat</a> · <a href="/oppaat/auton-sisapesun-hinta-turku/">Mikä paketti sopii minulle?</a></p>
      </div>
    </section>

    <section class="section">
      <div class="container grid two">
        <div>
          <h2>Meistä</h2>
          <p>Autokuntoon.fi on pieni turkulainen yritys, joka tekee auton sisäpesuja suoraan asiakkaan kotipihalla. Olemme ylpeitä henkilökohtaisesta palvelusta ja huolellisuudesta jokaisessa yksityiskohdassa.</p>
          <p>Kuuntelemme toiveitasi myös työn aikana. Voimme sopia lisäpalveluista tai keskittyä erityisesti sinulle tärkeisiin kohtiin.</p>
        </div>
        <div>
          <h2>Missä toimimme</h2>
          <p>Meillä ei ole kiinteää toimipistettä, vaan tulemme sinun luoksesi. Toimimme pääasiassa <a href="/alueet/auton-sisapesu-turku/">Turussa</a> sekä lähikunnissa, kuten <a href="/alueet/auton-sisapesu-kaarina/">Kaarinassa</a>, <a href="/alueet/auton-sisapesu-raisio/">Raisiossa</a>, <a href="/alueet/auton-sisapesu-naantali/">Naantalissa</a>, <a href="/alueet/auton-sisapesu-lieto/">Liedossa</a>, Ruskolla, Maskussa ja Paimiossa. <a href="/alueet/">Katso koko toiminta-alue</a>.</p>
          <p>Yli 15 kilometrin päähän Turun keskustasta lisäämme pienen polttoainemaksun, josta sovitaan etukäteen.</p>
        </div>
      </div>
    </section>

    <section class="section soft">
      <div class="container">
        <h2>Asiakkaidemme palautteita</h2>
        <div class="grid three">
{reviews_html}
        </div>
        <p class="note"><a href="/tyoen-jaelkeae-kuvina/">Katso ennen ja jälkeen -kuvia töistämme</a></p>
      </div>
    </section>

{cta()}"""

# ---------- Hinnat ----------
prices = f"""    <section class="section page-hero">
      <div class="container">
        <h1>Auton sisäpesun hinnat Turussa</h1>
        <p class="lead">Kaikki pesut tehdään kotipihallasi. Hinta sisältää työn, välineet ja pesuaineet. Pakettiajan ylittävä työ on 30 €/h.</p>
      </div>
    </section>

    <section class="section soft">
      <div class="container">
        <div class="grid three">
{price_cards()}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container grid two">
        <article class="card price-card">
          <h2>{SEAT[0]}</h2>
          <div class="price">{SEAT[1]} €</div>
          <p>{SEAT[2]}</p>
          <a class="btn" href="/ota-yhteyttae/">Varaa penkkien pesu</a>
        </article>
        <div>
          <h2>Hyvä tietää</h2>
          <ul>
            <li>Tarvitsemme vain auton ja sähköpistokkeen.</li>
            <li>Yli 15 km Turun keskustasta lisätään sovittu polttoainemaksu.</li>
            <li>Maksu tilisiirrolla, käteisellä tai MobilePaylla työn jälkeen.</li>
            <li>Emme ole arvonlisäverovelvollisia, joten hintoihin ei lisätä ALV:tä.</li>
            <li>Pakettiautojen ja asuntoautojen hinta sovitaan erikseen.</li>
            <li>Talvella pesu tehdään lämpimässä autotallissa tai hallissa.</li>
            <li>Peruutus maksutta viimeistään 48 h ennen sovittua aikaa, myöhemmin 20 €.</li>
          </ul>
          <p><a href="/oppaat/auton-sisapesun-hinta-turku/">Lue opas: mihin sisäpesun hinta perustuu ja mikä paketti sopii sinulle</a></p>
        </div>
      </div>
    </section>

{cta()}"""

# ---------- Kuvat ----------
MIATA_PAIRS = [
    ("Kuljettajan lattia", "miata-kuljettajan-lattia", "kuljettajan jalkatila ja lattiamatto"),
    ("Kuljettajan penkki", "miata-kuljettajan-penkki", "kuljettajan nahkapenkki ja kynnys"),
    ("Kuljettajan ovi", "miata-kuljettajan-ovi", "kuljettajan oven verhoilu"),
    ("Matkustajan lattia", "miata-apparin-lattia", "etumatkustajan jalkatila"),
    ("Keskikonsoli", "miata-keskikonsoli", "keskikonsoli ja penkit"),
    ("Keskipaneeli", "miata-keskipaneeli", "keskipaneeli, vaihdekeppi ja lattia"),
]

def pair(title, slug, what, car):
    return f"""          <div class="pair">
            <h3>{title}</h3>
            <div class="pair-imgs">
              <figure><img src="/images/{slug}-ennen.jpg" alt="{car}: {what} ennen sisäpesua" width="1000" height="1333" loading="lazy"><figcaption>Ennen</figcaption></figure>
              <figure class="after"><img src="/images/{slug}-jalkeen.jpg" alt="{car}: {what} sisäpesun jälkeen" width="1000" height="1333" loading="lazy"><figcaption>Jälkeen</figcaption></figure>
            </div>
          </div>"""

miata_pairs = "\n".join(pair(t, sl, w, "Mazda MX-5") for t, sl, w in MIATA_PAIRS)
bmw_pair = pair("Etumatkustajan puoli", "bmw", "etumatkustajan penkki ja lattia", "BMW")

def img(slug, alt):
    return f"""          <figure>
            <img src="/images/{slug}.jpg" alt="{alt}" width="1000" height="1333" loading="lazy">
          </figure>"""

miata_more = "\n".join([
    img("miata-matkustamo-jalkeen", "Mazda MX-5:n puhdas matkustamo ja nahkapenkit sisäpesun jälkeen"),
    img("miata-ratti-jalkeen", "Mazda MX-5:n ratti ja mittaristo sisäpesun jälkeen"),
    img("miata-penkkien-takana-jalkeen", "Mazda MX-5:n penkkien takainen tila imuroituna"),
])

gallery = f"""    <section class="section page-hero">
      <div class="container">
        <h1>Työn jälkeä kuvina</h1>
        <p class="lead">Ennen ja jälkeen -kuvia auton sisäpesuista, joita olemme tehneet Turun seudulla. Kaikki kuvat ovat omista töistämme.</p>
      </div>
    </section>

    <section class="section soft">
      <div class="container">
        <h2>Mazda MX-5 ”Miata”: peruspesu</h2>
        <p>Omistajan mukaan edellisestä pesusta oli kulunut pitkä aika. Peruspesussa autosta poistettiin roskat, hiekka ja lika, ja asiakas oli lopputulokseen tyytyväinen.</p>
        <div class="pairs">
{miata_pairs}
        </div>
        <h3 style="margin-top:36px">Lisää kuvia pesun jälkeen</h3>
        <div class="gallery">
{miata_more}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>BMW 3-sarjan farmari</h2>
        <p>Lattioille kertynyt hiekka ja lika imuroitiin, ja penkit ja pinnat puhdistettiin. Myös tavaratila siivottiin.</p>
        <div class="pairs">
{bmw_pair}
          <div class="pair">
            <h3>Tavaratila</h3>
            <div class="pair-imgs">
              <figure class="after"><img src="/images/bmw-tavaratila-jalkeen.jpg" alt="BMW-farmarin tavaratila imuroituna sisäpesun jälkeen" width="1000" height="1333" loading="lazy"><figcaption>Jälkeen</figcaption></figure>
            </div>
          </div>
        </div>
      </div>
    </section>

{cta("Haluatko autosi loistamaan?")}"""

# ---------- UKK ----------
faq_html = "\n".join(
    f"""          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>""" for q, a in FAQ)

faqpage = f"""    <section class="section page-hero">
      <div class="container">
        <h1>Usein kysytyt kysymykset auton sisäpesusta</h1>
        <p class="lead">Vastauksia yleisimpiin kysymyksiin hinnoista, ajanvarauksesta ja pesun kulusta.</p>
      </div>
    </section>

    <section class="section soft">
      <div class="container faq">
{faq_html}
      </div>
    </section>

{cta("Jäikö jokin askarruttamaan?", "Kysy rohkeasti WhatsAppilla tai sähköpostilla, vastaamme mahdollisimman pian.")}"""

# ---------- Yhteys ----------
contact = f"""    <section class="section page-hero">
      <div class="container">
        <h1>Ota yhteyttä ja varaa auton sisäpesu</h1>
        <p class="lead">Nopein tapa varata aika on WhatsApp. Kerro viestissä toivottu päivä, auton sijainti ja haluamasi palvelu.</p>
      </div>
    </section>

    <section class="section soft">
      <div class="container grid two">
        <div class="card">
          <h2>Yhteystiedot</h2>
          <ul class="contact-list">
            <li>WhatsApp: <a href="{WA}">{PHONE_TXT}</a></li>
            <li>Sähköposti: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li>Instagram: <a href="{IG}" rel="noopener">@autokuntoon.fi</a></li>
            <li>TikTok: <a href="{TT}" rel="noopener">@autokuntoon.fi</a></li>
          </ul>
          <p style="margin-top:20px"><a class="btn" href="{WA}">Avaa WhatsApp</a></p>
        </div>
        <div class="card">
          <h2>Sijainti</h2>
          <p>Meillä ei ole kiinteää toimipistettä, vaan tulemme kotipihallesi. Toimimme pääasiassa Turussa ja Turun seudulla.</p>
          <p style="margin-top:12px">Yli 15 km Turun keskustasta lisätään polttoainemaksu, josta sovitaan aina etukäteen.</p>
          <p style="margin-top:12px">Y-tunnus: 3525496-7</p>
        </div>
      </div>
    </section>"""


# ---------- Opas: sisäpesun hinta ----------
ART_PATH = "/oppaat/auton-sisapesun-hinta-turku/"
ART_TITLE = "Auton sisäpesun hinta Turussa: mitä pesu maksaa ja mitä se sisältää"
ART_DATE = "2026-11-09"

def article_schema(path=None, title=None, date=None, image="/images/bmw-ennen-jalkeen.jpg"):
    path, title, date = path or ART_PATH, title or ART_TITLE, date or ART_DATE
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "datePublished": date,
        "dateModified": date,
        "inLanguage": "fi",
        "mainEntityOfPage": SITE + path,
        "image": SITE + image,
        "author": {"@id": SITE + "/#yritys"},
        "publisher": {"@id": SITE + "/#yritys"},
    }

def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
            for i, (n, u) in enumerate(items)
        ],
    }

price_rows = "\n".join(
    f"            <tr><td>{n}</td><td>{p} €</td><td>enintään {t}</td><td>{d}</td></tr>"
    for n, p, t, d, _ in SERVICES
) + f"\n            <tr><td>{SEAT[0]}</td><td>{SEAT[1]} €</td><td>–</td><td>Pelkät penkit, esimerkiksi tahrojen poistoon.</td></tr>"

article = f"""    <article class="section">
      <div class="container prose">
        <nav class="crumbs" aria-label="Murupolku"><a href="/">Etusivu</a> › <span>Oppaat</span> › <span>Sisäpesun hinta</span></nav>
        <h1>{ART_TITLE}</h1>
        <p class="meta">Julkaistu 9.11.2026 · Autokuntoon.fi</p>

        <p class="answer"><strong>Lyhyesti:</strong> Autokuntoon.fi:n auton sisäpesu maksaa Turussa 55–125 € paketista riippuen. Peruspesu (imurointi ja pintojen pyyhintä) on 55 €, kattavapesu 80 € ja Deluxe-pesu penkkien syväpesulla 125 €. Pesu tehdään asiakkaan kotipihalla, joten autoa ei tarvitse viedä minnekään.</p>

        <h2>Hinnat paketeittain</h2>
        <div class="table-wrap">
        <table>
          <thead><tr><th>Palvelu</th><th>Hinta</th><th>Kesto</th><th>Sisältö</th></tr></thead>
          <tbody>
{price_rows}
          </tbody>
        </table>
        </div>
        <p>Jos pakettiaika ylittyy, lisätyö maksaa 30 €/h. Yli 15 kilometrin päähän Turun keskustasta lisätään polttoainemaksu, josta sovitaan etukäteen. Emme ole arvonlisäverovelvollisia, joten hintoihin ei tule ALV:tä.</p>

        <h2>Mikä vaikuttaa sisäpesun hintaan?</h2>
        <ul>
          <li><strong>Auton kunto.</strong> Hiekka, roskat ja kuivuneet tahrat lisäävät työaikaa. Säännöllisesti pesty auto valmistuu peruspesun ajassa.</li>
          <li><strong>Auton koko.</strong> Farmarissa ja tila-autossa on enemmän imuroitavaa ja pyyhittävää kuin pienessä kaksipaikkaisessa.</li>
          <li><strong>Penkkien materiaali.</strong> Kangaspenkit voi syväpestä tekstiilipesurilla. Nahkapenkit puhdistetaan pyyhkimällä.</li>
          <li><strong>Lemmikin karvat ja tahrat.</strong> Karvojen irrottaminen kankaasta ja tahrojen käsittely vievät aikaa.</li>
          <li><strong>Matka.</strong> Turussa ja lähikunnissa matka sisältyy hintaan, kauempana lisätään polttoainemaksu.</li>
        </ul>

        <h2>Mikä paketti sopii minulle?</h2>
        <ul>
          <li><strong>Peruspesu 55 €</strong> sopii, kun auto on arkikäytössä ja kaipaa imurointia ja pintojen puhdistusta.</li>
          <li><strong>Kattavapesu 80 €</strong> sopii, kun pinnoissa on pinttynyttä likaa tai edellisestä pesusta on kulunut pitkä aika.</li>
          <li><strong>Deluxe-pesu 125 €</strong> sopii ennen auton myyntiä (<a href="/oppaat/auton-sisapesu-ennen-myyntia/">lue opas</a>), kangaspenkkien tahroihin tai kun haluat sisätilat mahdollisimman lähelle uutta.</li>
          <li><strong>Penkkien pesu 50 €</strong> riittää, jos muu auto on siisti, mutta penkeissä on esimerkiksi kahvitahroja.</li>
        </ul>
        <p>Jos et ole varma, lähetä WhatsAppilla kuva auton sisätiloista, niin suosittelemme sopivan paketin.</p>

        <h2>Esimerkki: Mazda MX-5:n peruspesu</h2>
        <p>Mazda MX-5:n edellisestä pesusta oli kulunut pitkä aika, ja lattioilla oli hiekkaa, lehtiä ja roskia. Peruspesu 55 €:lla riitti: lattiat imuroitiin, pinnat pyyhittiin ja nahkapenkit puhdistettiin. <a href="/tyoen-jaelkeae-kuvina/">Katso ennen ja jälkeen -kuvat</a>.</p>
        <figure style="margin:0">
          <img class="wide-img" src="/images/bmw-ennen-jalkeen.jpg" alt="BMW:n etumatkustajan puoli ennen ja jälkeen sisäpesun" width="1600" height="902" loading="lazy">
          <figcaption class="meta">BMW 3-sarjan farmari ennen ja jälkeen sisäpesun.</figcaption>
        </figure>

        <h2>Kotipihalla vai pesulassa?</h2>
        <p>Kun pesu tehdään kotipihalla, säästät ajomatkan ja odottelun. Voit tehdä sillä aikaa muuta, ja maksu hoidetaan vasta kun olet nähnyt lopputuloksen. Pesua varten tarvitaan vain sähköpistoke.</p>

        <h2>Kuinka usein auto kannattaa pestä sisältä?</h2>
        <p>Suosittelemme arkikäytössä olevalle autolle peruspesua muutaman kerran vuodessa, esimerkiksi kevään hiekoitussesongin jälkeen ja ennen talvea. Kangaspenkkien syväpesu riittää yleensä kerran vuodessa tai tarpeen mukaan.</p>
      </div>
    </article>

{cta("Varaa sisäpesu kotipihallesi", "Lähetä viesti, niin sovitaan aika. Turku, Kaarina, Raisio, Naantali, Lieto, Rusko, Masku ja Paimio.")}"""

# ---------- Opas: sisäpesu ennen myyntiä ----------
ART2_PATH = "/oppaat/auton-sisapesu-ennen-myyntia/"
ART2_TITLE = "Auton sisäpesu ennen myyntiä: näin saat autosta paremman ensivaikutelman"
ART2_DATE = "2026-11-09"

article2 = f"""    <article class="section">
      <div class="container prose">
        <nav class="crumbs" aria-label="Murupolku"><a href="/">Etusivu</a> › <span>Oppaat</span> › <span>Sisäpesu ennen myyntiä</span></nav>
        <h1>{ART2_TITLE}</h1>
        <p class="meta">Julkaistu 9.11.2026 · Autokuntoon.fi</p>

        <p class="answer"><strong>Lyhyesti:</strong> Ostaja tekee päätöksensä pitkälti sen perusteella, miltä auto näyttää ja tuoksuu sisältä. Ennen myyntiä kannattaa imuroida ja puhdistaa kaikki pinnat sekä syväpestä kangaspenkit. Turussa Autokuntoon.fi:n Deluxe-pesu (125 €) sisältää kaiken tämän, ja se tehdään kotipihallasi.</p>

        <h2>Miksi sisäpesu kannattaa ennen myyntiä?</h2>
        <ul>
          <li><strong>Myynti-ilmoituksen kuvat.</strong> Puhtaat penkit ja lattiat näyttävät kuvissa paremmilta, ja ilmoitus erottuu muista.</li>
          <li><strong>Ensivaikutelma koeajolla.</strong> Likainen sisätila saa ostajan epäilemään, että autoa on hoidettu muutenkin huonosti.</li>
          <li><strong>Vähemmän tingittävää.</strong> Tahrat ja roskat ovat helppoja perusteita pyytää hinnasta alennusta.</li>
          <li><strong>Hajut pois.</strong> Penkkien syväpesu poistaa kankaaseen imeytynyttä likaa, joka usein aiheuttaa ummehtuneen hajun.</li>
        </ul>

        <h2>Muistilista ennen myyntiä</h2>
        <ol>
          <li>Tyhjennä auto omista tavaroistasi: hansikaslokero, ovitaskut, tavaratila ja penkkien alustat.</li>
          <li>Imuroi lattiat, matot, penkit ja tavaratila. Muista penkkien välit ja kiskot.</li>
          <li>Pese kojelauta, keskikonsoli, ovien verhoilut ja ovien karmit.</li>
          <li>Syväpese kangaspenkit tekstiilipesurilla, jos niissä on tahroja tai tummumia.</li>
          <li>Puhdista ikkunat sisäpuolelta, jotta kuvissa ei näy heijastuksia ja raitoja.</li>
          <li>Ota myynti-ilmoituksen kuvat heti pesun jälkeen päivänvalossa.</li>
        </ol>

        <h2>Minkä paketin valitsen?</h2>
        <ul>
          <li><strong>Deluxe-pesu 125 €</strong> (enintään 4 h) on paras valinta myyntiin: kaikki pinnat pestään ja kangaspenkit syväpestään tekstiilipesurilla.</li>
          <li><strong>Kattavapesu 80 €</strong> (enintään 2 h) riittää, jos penkit ovat nahkaa tai ne ovat jo valmiiksi siistit.</li>
          <li><strong>Penkkien pesu 50 €</strong> sopii, jos olet itse imuroinut ja pyyhkinyt auton, mutta penkeissä on tahroja.</li>
        </ul>
        <p>Katso kaikki hinnat ja pakettien sisällöt <a href="/hinnat-ja-palvelut/">hintasivulta</a> tai lue <a href="/oppaat/auton-sisapesun-hinta-turku/">opas sisäpesun hinnasta</a>.</p>

        <figure style="margin:0">
          <img class="wide-img" src="/images/bmw-ennen-jalkeen.jpg" alt="BMW:n etumatkustajan puoli ennen ja jälkeen sisäpesun" width="1600" height="902" loading="lazy">
          <figcaption class="meta">Ero näkyy heti: BMW 3-sarjan farmari ennen ja jälkeen sisäpesun.</figcaption>
        </figure>

        <h2>Milloin pesu kannattaa tehdä?</h2>
        <p>Paras hetki on päivä tai kaksi ennen myynti-ilmoituksen kuvaamista. Silloin auto on puhtaimmillaan sekä kuvissa että ensimmäisillä koeajoilla. Varaa aika hyvissä ajoin. Tarkistamme viestit päivittäin, ja aika voi järjestyä jopa samalle päivälle.</p>
      </div>
    </article>

{cta("Myymässä autoa?", "Varaa Deluxe-pesu kotipihallesi Turun seudulla. Lähetä viesti, niin sovitaan aika.")}"""

PAGES = [
    ("/", "Auton sisäpesu kotipihalla Turussa | Autokuntoon.fi",
     "Auton sisäpesu suoraan kotipihallasi Turussa ja Turun seudulla. Peruspesu 55 €, kattavapesu 80 €, Deluxe-pesu 125 €. Varaa aika WhatsAppilla.",
     home, [business_schema()]),
    ("/hinnat-ja-palvelut/", "Hinnat ja palvelut – auton sisäpesu Turku | Autokuntoon.fi",
     "Auton sisäpesun hinnat: peruspesu 55 €, kattavapesu 80 €, Deluxe-pesu 125 € ja penkkien pesu tekstiilipesurilla 50 €. Tulemme kotipihallesi Turussa.",
     prices, [business_schema()]),
    ("/tyoen-jaelkeae-kuvina/", "Työn jälkeä kuvina – ennen ja jälkeen | Autokuntoon.fi",
     "Ennen ja jälkeen -kuvia Autokuntoon.fi:n tekemistä auton sisäpesuista Turun seudulla.",
     gallery, []),
    ("/usein-kysytyt-kysymykset/", "Usein kysytyt kysymykset – auton sisäpesu | Autokuntoon.fi",
     "Vastauksia auton sisäpesun hintoihin, kestoon, maksutapoihin ja toiminta-alueeseen Turussa.",
     faqpage, [faq_schema()]),
    ("/ota-yhteyttae/", "Ota yhteyttä – varaa auton sisäpesu | Autokuntoon.fi",
     "Varaa auton sisäpesu kotipihallesi Turussa WhatsAppilla tai sähköpostilla. Vastaamme nopeasti.",
     contact, []),
    (ART_PATH, "Auton sisäpesun hinta Turussa 2026 – hinnat ja paketit | Autokuntoon.fi",
     "Paljonko auton sisäpesu maksaa Turussa? Peruspesu 55 €, kattavapesu 80 €, Deluxe 125 €. Katso mitä hintaan sisältyy ja mikä paketti sopii autollesi.",
     article, [article_schema(), breadcrumb_schema([("Etusivu", "/"), ("Auton sisäpesun hinta Turussa", ART_PATH)])]),
    (ART2_PATH, "Auton sisäpesu ennen myyntiä – muistilista ja hinnat | Autokuntoon.fi",
     "Myymässä autoa? Puhdas sisätila parantaa ensivaikutelmaa ja myynti-ilmoituksen kuvia. Muistilista ennen myyntiä ja Deluxe-pesu kotipihalla Turussa 125 €.",
     article2, [article_schema(ART2_PATH, ART2_TITLE, ART2_DATE), breadcrumb_schema([("Etusivu", "/"), ("Auton sisäpesu ennen myyntiä", ART2_PATH)])]),
]

# ---------- Paikkakuntasivut ----------
# (slug, nimi, inessiivi, genetiivi, illatiivi, johdanto, alueet, matka, oma vinkki)
CITIES = [
    ("turku", "Turku", "Turussa", "Turun", "Turkuun",
     "Autokuntoon.fi on turkulainen yritys, ja Turku on kotialueemme. Tulemme pesemään autosi sisältä kotipihallesi, työpaikan parkkipaikalle tai taloyhtiön pihaan, joten sinun ei tarvitse ajaa pesulaan eikä odotella.",
     ["Keskusta", "Hirvensalo", "Runosmäki", "Varissuo", "Nummi", "Uittamo", "Skanssi", "Ilpoinen", "Härkämäki", "Moikoinen"],
     "Turussa matka sisältyy hintaan. Polttoainemaksu lisätään vain, jos osoite on yli 15 kilometrin päässä Turun keskustasta, esimerkiksi osassa saaristoa. Siitä sovitaan aina etukäteen.",
     "Kerrostalossa asuvan kannattaa varmistaa, että pihalla tai autokatoksessa on sähköpistoke. Usein lämmitystolpan pistoke riittää."),
    ("kaarina", "Kaarina", "Kaarinassa", "Kaarinan", "Kaarinaan",
     "Kaarina rajautuu Turkuun, joten se kuuluu lähialueeseemme. Pesemme auton sisältä suoraan kotipihallasi, eikä autoa tarvitse viedä minnekään.",
     ["Keskusta", "Littoinen", "Kuusisto", "Hovirinta", "Rauvola", "Piikkiö"],
     "Kaarinan keskustaan, Littoisiin ja Kuusistoon tulemme ilman lisämaksua. Piikkiön suunnalla matka voi ylittää 15 kilometriä Turun keskustasta, jolloin lisätään pieni polttoainemaksu. Kerromme sen etukäteen.",
     "Omakotitalon pihalla pesu on helppo järjestää: tarvitsemme vain sähköpistokkeen ja tilaa avata auton ovet."),
    ("raisio", "Raisio", "Raisiossa", "Raision", "Raisioon",
     "Raisio on vain lyhyen ajomatkan päässä Turusta, joten tulemme sinne usein. Auton sisäpesu tehdään kotipihallasi, ja voit tehdä sillä aikaa muuta.",
     ["Keskusta", "Kaanaa", "Ihala", "Kerttula", "Vaisaari", "Kuloinen"],
     "Raision keskusta on noin 10 kilometrin päässä Turun keskustasta, joten matka sisältyy hintaan koko Raisiossa.",
     "Jos auto on päivän töissä, pesu voidaan sopia myös iltaan, kun auto on taas kotipihassa."),
    ("naantali", "Naantali", "Naantalissa", "Naantalin", "Naantaliin",
     "Tulemme Naantaliin pesemään auton sisältä kotipihallesi tai vaikka kesämökille. Riittää, että auton lähellä on sähköpistoke.",
     ["Keskusta", "Luonnonmaa", "Karvetti", "Rymättylä", "Merimasku", "Velkua"],
     "Naantalin keskusta on noin 15 kilometrin päässä Turun keskustasta, joten polttoainemaksu riippuu tarkasta osoitteesta. Rymättylään, Merimaskuun ja Velkualle lisätään aina polttoainemaksu. Kerromme summan ennen kuin varaus vahvistetaan.",
     "Kesämökillä pesu onnistuu, kunhan sähköä on saatavilla. Kerro varatessasi, jos perille on hankala löytää."),
    ("lieto", "Lieto", "Liedossa", "Liedon", "Lietoon",
     "Tulemme Lietoon pesemään auton sisältä kotipihallasi. Pesu sopii arkiautolle, lapsiperheen autolle tai ennen auton myyntiä.",
     ["Kirkonkylä", "Ilmarinen", "Avantti", "Loukinainen", "Littoinen", "Tarvasjoki"],
     "Ilmarinen, Avantti ja Liedon puoleinen Littoinen ovat lähellä Turkua, joten sinne matka sisältyy hintaan. Kirkonkylä on noin 15 kilometrin rajalla, ja Tarvasjoelle lisätään polttoainemaksu. Kerromme sen aina etukäteen.",
     "Lapsiperheen autossa lastenistuimet kannattaa jättää paikalleen, sillä puhdistamme myös ne."),
]
AREA_PATH = "/alueet/"

def city_path(slug):
    return f"{AREA_PATH}auton-sisapesu-{slug}/"

def city_faq(c):
    slug, name, ine, gen, ill, intro, districts, travel, tip = c
    return [
        (f"Tuletteko {ill} pesemään auton?",
         f"Kyllä. Pesemme autoja {ine}, esimerkiksi näillä alueilla: {', '.join(districts)}. Pesu tehdään kotipihallasi, ja tarvitsemme vain sähköpistokkeen."),
        (f"Maksaako matka {ill} lisää?", travel),
        (f"Paljonko auton sisäpesu maksaa {ine}?",
         f"Peruspesu maksaa 55 €, kattavapesu 80 €, Deluxe-pesu 125 € ja pelkkä penkkien pesu tekstiilipesurilla 50 €. Hinnat ovat samat kaikkialla, ja niihin ei lisätä ALV:tä."),
    ]

def city_schemas(c):
    slug, name, ine, gen, *_ = c
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Auton sisäpesu",
        "name": f"Auton sisäpesu {ine}",
        "url": SITE + city_path(slug),
        "provider": {"@id": SITE + "/#yritys"},
        "areaServed": {"@type": "City", "name": name},
        "offers": [
            {"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "EUR"}
            for n, p, *_ in SERVICES
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in city_faq(c)
        ],
    }
    crumbs = breadcrumb_schema([("Etusivu", "/"), ("Toiminta-alue", AREA_PATH), (f"Auton sisäpesu {name}", city_path(slug))])
    return [business_schema(), service, faq, crumbs]

def city_body(c):
    slug, name, ine, gen, ill, intro, districts, travel, tip = c
    others = " · ".join(f'<a href="{city_path(o[0])}">{o[1]}</a>' for o in CITIES if o[0] != slug)
    faq_html = "\n".join(
        f"""          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>""" for q, a in city_faq(c))
    district_lis = "".join(f"<li>{d}</li>" for d in districts)
    return f"""    <section class="hero page-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Murupolku" style="color:#cfc8bb"><a href="/" style="color:#e6e1d8">Etusivu</a> › <a href="{AREA_PATH}" style="color:#e6e1d8">Toiminta-alue</a> › <span>{name}</span></nav>
        <h1>Auton sisäpesu {ine}</h1>
        <p>{intro}</p>
        <div class="btn-row">
          <a class="btn" href="{WA}">Varaa WhatsAppilla</a>
          <a class="btn ghost" href="/hinnat-ja-palvelut/">Katso hinnat</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container prose">
        <p class="answer"><strong>Lyhyesti:</strong> Autokuntoon.fi pesee auton sisältä kotipihallasi {ine}. Peruspesu maksaa 55 €, kattavapesu 80 € ja Deluxe-pesu penkkien syväpesulla 125 €. Varaus WhatsAppilla tai sähköpostilla, ja maksu vasta työn jälkeen.</p>

        <h2>Missä päin {gen} pesemme?</h2>
        <p>Tulemme kaikkialle {ill}. Tässä esimerkkejä alueista, joilla pesemme:</p>
        <ul class="district-list">{district_lis}</ul>

        <h2>Matka ja polttoainemaksu</h2>
        <p>{travel}</p>

        <h2>Näin pesu etenee</h2>
        <ol>
          <li>Lähetä viesti WhatsAppilla tai sähköpostilla. Kuva auton sisätiloista auttaa valitsemaan sopivan paketin.</li>
          <li>Sovimme ajan ja paikan. Sinun ei tarvitse olla kotona, kunhan auto on auki tai avaimet sovitussa paikassa.</li>
          <li>Pesemme auton sisältä omilla välineillämme. Tarvitsemme vain sähköpistokkeen.</li>
          <li>Maksat tilisiirrolla, käteisellä tai MobilePaylla, kun olet nähnyt lopputuloksen.</li>
        </ol>
        <p><strong>Vinkki:</strong> {tip}</p>
      </div>
    </section>

    <section class="section soft">
      <div class="container">
        <h2>Hinnat {ine}</h2>
        <p class="lead">Hinnat ovat samat kaikkialla Turun seudulla. Pakettiajan ylittävä työ maksaa 30 €/h.</p>
        <div class="grid three">
{price_cards()}
        </div>
        <p class="note">Pelkkä penkkien pesu tekstiilipesurilla maksaa {SEAT[1]} €. Pakettiautot ja asuntoautot hinnoitellaan erikseen.</p>
      </div>
    </section>

    <section class="section">
      <div class="container prose">
        <h2>Usein kysyttyä: {name}</h2>
        <div class="faq">
{faq_html}
        </div>
        <p>Lisää vastauksia löydät <a href="/usein-kysytyt-kysymykset/">usein kysyttyjen kysymysten sivulta</a>. Lue myös <a href="/oppaat/auton-sisapesun-hinta-turku/">opas sisäpesun hinnasta</a> ja <a href="/tyoen-jaelkeae-kuvina/">katso ennen ja jälkeen -kuvat</a>.</p>
        <p class="meta">Pesemme myös muualla: {others}</p>
      </div>
    </section>

{cta(f"Varaa auton sisäpesu {ine}", "Lähetä viesti, niin sovitaan aika. Vastaamme yleensä saman päivän aikana.")}"""

area_cards = "\n".join(
    f"""          <a class="card area-card" href="{city_path(c[0])}">
            <h3>Auton sisäpesu {c[1]}</h3>
            <p>{', '.join(c[6][:4])} ja muut alueet</p>
          </a>""" for c in CITIES)

areas = f"""    <section class="hero page-hero">
      <div class="container">
        <h1>Toiminta-alue</h1>
        <p>Pesemme autoja asiakkaan kotipihalla Turussa ja Turun seudulla. Valitse paikkakuntasi, niin näet alueet, matkakulut ja hinnat.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="grid three">
{area_cards}
        </div>
        <p class="note" style="margin-top:24px">Tulemme myös Ruskolle, Maskuun ja Paimioon. Yli 15 kilometrin päähän Turun keskustasta lisätään polttoainemaksu, josta sovitaan aina etukäteen.</p>
      </div>
    </section>

{cta()}"""

PAGES += [
    (AREA_PATH, "Toiminta-alue – auton sisäpesu Turun seudulla | Autokuntoon.fi",
     "Auton sisäpesu kotipihalla Turussa, Kaarinassa, Raisiossa, Naantalissa ja Liedossa. Katso alueet, matkakulut ja hinnat.",
     areas, [breadcrumb_schema([("Etusivu", "/"), ("Toiminta-alue", AREA_PATH)])]),
] + [
    (city_path(c[0]),
     f"Auton sisäpesu {c[1]} – kotipihalla alk. 55 € | Autokuntoon.fi",
     f"Auton sisäpesu kotipihallasi {c[2]}. Peruspesu 55 €, kattavapesu 80 €, Deluxe-pesu 125 €. Tulemme luoksesi, maksu vasta työn jälkeen.",
     city_body(c), city_schemas(c))
    for c in CITIES
]

for path, title, desc, body, schemas in PAGES:
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(path, title, desc, body, schemas))

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for path, *_ in PAGES:
        f.write(f"  <url><loc>{SITE}{path}</loc></url>\n")
    f.write("</urlset>\n")
print("ok")
