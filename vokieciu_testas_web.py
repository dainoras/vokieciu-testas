
import streamlit as st

# Klausimų sąrašas
questions = [
    {
        "question": "Kaip vokiškai pasakyti 'aš esu'?",
        "options": ["Ich bin", "Du bist", "Er ist", "Wir sind"],
        "answer": "Ich bin"
    },
    {
        "question": "Wer ist das?",
        "options": ["Der Mann", "Die Frau", "Das Kind", "Der Hund"],
        "answer": "Die Frau"
    },
    {
        "question": "Kuris iš šių žodžių vokiškai reiškia 'namas'?",
        "options": ["Haus", "Katze", "Baum", "Buch"],
        "answer": "Haus"
    }
]

def show_question(index):
    st.markdown(f"### --- Klausimas {index + 1}/{len(questions)} ---")
    question = questions[index]
    user_answer = st.radio(question["question"], question["options"], key=index)
    return user_answer == question["answer"], question["answer"]

def main():
    st.title("Vokiečių kalbos testavimo programėlė")
    st.markdown("## Pasirinkite veiksmą")

    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.correct_answers = 0
        st.session_state.answers = []

    if st.button("Pradėti naują testą") or st.session_state.step == 0:
        st.session_state.step = 1
        st.session_state.correct_answers = 0
        st.session_state.answers = []

    if 1 <= st.session_state.step <= len(questions):
        correct, correct_answer = show_question(st.session_state.step - 1)
        if st.button("Tęsti"):
            if correct:
                st.success("Teisingai!")
                st.session_state.correct_answers += 1
            else:
                st.error(f"Neteisingai. Teisingas atsakymas yra: {correct_answer}")
            st.session_state.step += 1

    elif st.session_state.step > len(questions):
        st.markdown("## --- Testo rezultatai ---")
        st.write(f"Teisingai atsakėte į {st.session_state.correct_answers} iš {len(questions)} klausimų.")
        if st.session_state.correct_answers == len(questions):
            st.success("Puikiai! Puikios žinios!")
        elif st.session_state.correct_answers >= len(questions) // 2:
            st.info("Geras rezultatas! Tęskite mokymąsi ir gilinkite žinias.")
        else:
            st.warning("Reikia pasistengti dar labiau. Praktika daro meistrą!")

        st.session_state.step = 0

if __name__ == "__main__":
    main()
