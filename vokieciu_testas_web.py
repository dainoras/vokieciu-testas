import random
import json
from datetime import datetime
import streamlit as st

# Failo pavadinimas, kuriame saugosime rezultatus
REZULTATU_FAILAS = "rezultatai.json"
rezultatu_istorija = []

# Klausimai pagal lygius
klausimai_pagal_lygi = {
    "A1": [
        {"klausimas": "Kuris iš šių žodžių vokiškai reiškia 'namas'?", "atsakymai": ["Haus", "Katze", "Baum", "Buch"], "teisingas_atsakymas": 0, "lygis": "A1", "tema": "Žodynas"},
        {"klausimas": "Kaip vokiškai pasakyti 'aš esu'?", "atsakymai": ["Ich bin", "Du bist", "Er ist", "Wir sind"], "teisingas_atsakymas": 0, "lygis": "A1", "tema": "Gramatika"},
        {"klausimas": "Wer ist das?", "atsakymai": ["Der Mann", "Die Frau", "Das Kind", "Der Hund"], "teisingas_atsakymas": 1, "lygis": "A1", "tema": "Daiktavardžiai"}
    ],
    "B2": [
        {"klausimas": "Kuris iš šių sakinių yra gramatiškai teisingas?", "atsakymai": ["Ich habe Hunger.", "Ich bin Hunger.", "Hunger ich habe.", "Habe ich Hunger."], "teisingas_atsakymas": 0, "lygis": "B2", "tema": "Sakinio struktūra"}
    ]
}

# Funkcija, kad pateiktume klausimą su atsakymais
def pateikti_klausima(klausimas):
    """
    Pateikia klausimą Streamlit sąsajoje ir leidžia vartotojui pasirinkti atsakymą.
    """
    atsakymai = klausimas['atsakymai']
    pasirinkimas = st.radio(klausimas['klausimas'], atsakymai)
    return atsakymai.index(pasirinkimas)

# Atlikti testą
def atlikti_testa(klausimai_pagal_lygi, lygis):
    """
    Atlieka tam tikro lygio testą ir saugo rezultatus.
    """
    if lygis not in klausimai_pagal_lygi:
        st.write(f"Atsiprašome, šiuo metu nėra {lygis} lygio klausimų.")
        return

    atrinkti_klausimai = klausimai_pagal_lygi[lygis]

    if not atrinkti_klausimai:
        st.write(f"Atsiprašome, šiuo metu nėra {lygis} lygio klausimų.")
        return

    random.shuffle(atrinkti_klausimai)
    klausimu_skaicius = len(atrinkti_klausimai)
    teisingi_atsakymai = 0

    st.write(f"\nPradedamas {lygis} lygio testas (iš viso {klausimu_skaicius} klausimų):")

    for i, klausimas in enumerate(atrinkti_klausimai):
        st.write(f"\n--- Klausimas {i + 1}/{klausimu_skaicius} ---")
        vartotojo_pasirinkimas = pateikti_klausima(klausimas)

        if vartotojo_pasirinkimas == klausimas['teisingas_atsakymas']:
            st.success("Teisingai!")
            teisingi_atsakymai += 1
        else:
            teisingas_atsakymas = klausimas['atsakymai'][klausimas['teisingas_atsakymas']]
            st.error(f"Neteisingai. Teisingas atsakymas yra: {teisingas_atsakymas}")

    st.write(f"\n--- Testo rezultatai ---")
    st.write(f"Teisingai atsakėte į {teisingi_atsakymai} iš {klausimu_skaicius} klausimų.")

    procentas = (teisingi_atsakymai / klausimu_skaicius) * 100
    if procentas >= 80:
        st.success("Puikus rezultatas! Toliau praktikuokitės ir galite pereiti prie aukštesnio lygio.")
    elif procentas >= 50:
        st.warning("Geras rezultatas! Tęskite mokymąsi ir gilinkite žinias.")
    else:
        st.error("Reikėtų daugiau pastangų. Peržiūrėkite pagrindines temas ir atlikite daugiau pratimų.")

    # Sukuriame įrašą apie testo rezultatus
    rezultatas = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lygis": lygis,
        "teisingi_atsakymai": teisingi_atsakymai,
        "bendras_klausimų_skaičius": klausimu_skaicius,
        "procentas": round(procentas, 2)
    }
    rezultatu_istorija.append(rezultatas)
    issaugoti_rezultatus() # Išsaugome rezultatus po kiekvieno testo

# Išsaugoti rezultatus į failą
def issaugoti_rezultatus():
    """
    Išsaugo rezultatų istoriją į JSON failą.
    """
    try:
        with open(REZULTATU_FAILAS, 'w') as failas:
            json.dump(rezultatu_istorija, failas)
        st.write("Rezultatai sėkmingai išsaugoti.")
    except Exception as e:
        st.write(f"Klaida išsaugant rezultatus: {e}")

# Nuskaityti rezultatus iš failo
def nuskaityti_rezultatus():
    """
    Nuskaito rezultatų istoriją iš JSON failo.
    """
    try:
        with open(REZULTATU_FAILAS, 'r') as failas:
            global rezultatu_istorija
            rezultatu_istorija = json.load(failas)
        st.write("Rezultatai sėkmingai nuskaityti.")
    except FileNotFoundError:
        st.write("Rezultatų failas nerastas. Pradedama nauja istorija.")
        rezultatu_istorija = []
    except json.JSONDecodeError:
        st.write("Klaida nuskaitant rezultatus iš failo. Pradedama nauja istorija.")
        rezultatu_istorija = []

# Streamlit programa
def paleisti_programa():
    """
    Paleidžia vokiečių kalbos testavimo programą.
    """
    nuskaityti_rezultatus() # Nuskaitome rezultatus paleidžiant programą

    st.title("Vokiečių kalbos testavimo programėlė")

    veiksmu = ["Pradėti naują testą", "Peržiūrėti rezultatus", "Baigti"]
    pasirinkimas = st.selectbox("Pasirinkite veiksmą", veiksmu)

    if pasirinkimas == veiksmu[0]:
        lygiai = list(klausimai_pagal_lygi.keys())
        lygis = st.selectbox("Pasirinkite norimą testo lygį", lygiai)

        if lygis:
            atlikti_testa(klausimai_pagal_lygi, lygis)

    elif pasirinkimas == veiksmu[1]:
        if rezultatu_istorija:
            for rezultatas in rezultatu_istorija:
                st.write(f"Data: {rezultatas['data']}, Lygis: {rezultatas['lygis']}, Rezultatas: {rezultatas['teisingi_atsakymai']}/{rezultatas['bendras_klausimų_skaičius']} ({rezultatas['procentas']}%)")
        else:
            st.write("Dar neatlikote nei vieno testo.")

    elif pasirinkimas == veiksmu[2]:
        issaugoti_rezultatus() # Išsaugome rezultatus prieš baigdami programą
        st.write("Ačiū, kad naudojotės mūsų vokiečių kalbos testavimo programėle!")

# Paleisti aplikaciją
if __name__ == "__main__":
    paleisti_programa()
