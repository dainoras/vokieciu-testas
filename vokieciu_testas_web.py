import streamlit as st
import random

klausimai = [
    {
        "klausimas": "Kaip vokiškai „labas“?",
        "atsakymai": ["Hallo", "Tschüss", "Danke", "Bitte"],
        "teisingas": 0
    },
    {
        "klausimas": "Kuris žodis reiškia „ačiū“?",
        "atsakymai": ["Bitte", "Danke", "Guten Tag", "Entschuldigung"],
        "teisingas": 1
    },
    {
        "klausimas": "Kaip vokiškai „prašau“?",
        "atsakymai": ["Tschüss", "Danke", "Bitte", "Hallo"],
        "teisingas": 2
    }
]

st.title("🧪 Vokiečių kalbos testas")

if "indeksas" not in st.session_state:
    st.session_state.indeksas = 0
    st.session_state.teisingi = 0

if st.session_state.indeksas < len(klausimai):
    k = klausimai[st.session_state.indeksas]
    st.write(f"**{k['klausimas']}**")
    pasirinkimas = st.radio("Pasirinkite atsakymą:", k["atsakymai"])
    if st.button("Patvirtinti"):
        if k["atsakymai"].index(pasirinkimas) == k["teisingas"]:
            st.success("Teisingai!")
            st.session_state.teisingi += 1
        else:
            st.error(f"Neteisingai. Teisingas atsakymas: {k['atsakymai'][k['teisingas']]}")
        st.session_state.indeksas += 1
        st.rerun()

else:
    st.balloons()
    st.write(f"✅ Testas baigtas. Rezultatas: {st.session_state.teisingi} iš {len(klausimai)} teisingų.")
    if st.button("Pradėti iš naujo"):
        st.session_state.indeksas = 0
        st.session_state.teisingi = 0
        st.rerun()


