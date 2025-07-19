# Teil 1 – Leitanlass und Konfiguration
import streamlit as st

st.set_page_config(page_title="Anamnese-Generator")
st.title("🫀 Anamnese-Textgenerator")

def liste_mit_und(liste):
    if len(liste) == 0:
        return ""
    elif len(liste) == 1:
        return liste[0]
    elif len(liste) == 2:
        return f"{liste[0]} und {liste[1]}"
    else:
        return f"{', '.join(liste[:-1])} und {liste[-1]}"

st.sidebar.title("Konfiguration")
aufnahmemodus = st.sidebar.radio("Vorstellung:", ["stationär", "ambulant"])
geschlecht = st.sidebar.radio("Geschlecht:", ["Patientin (w)", "Patient (m)"])

st.header("1. Leitanlass")
leitanlass = st.selectbox("Führender Aufnahmegrund", ["Vitium", "KHK", "Vorhofflimmern", "Symptome", "Freitext"])
freitext_leitanlass = ""
ziel = ""

diagnose = ""
if leitanlass == "Vitium":
    klappe = st.selectbox("Betroffene Klappe", ["Mitralklappeninsuffizienz", "Mitralklappenstenose", "Trikuspidalklappeninsuffizienz", "Trikuspidalklappenstenose", "Aortenklappeninsuffizienz", "Aortenklappenstenose"])
    if klappe != "Aortenklappenstenose":
        grad = st.selectbox("Schweregrad", ["I", "II", "III", "IV"])
        diagnose = f"{klappe} Grad {grad}"
    else:
        diagnose = "hochgradiger Aortenklappenstenose"
    ziel_option = st.selectbox("Ziel der Vorstellung", ["zur Verlaufskontrolle", "zur weiteren Diagnostik", "zur Therapieplanung", "Freitext"] if aufnahmemodus == "ambulant" else ["zur Vitienevaluation", "Freitext"])
    ziel = ziel_option if ziel_option != "Freitext" else st.text_input("Freitext Ziel")
elif leitanlass == "KHK":
    khk_typ = st.selectbox("KHK Typ", ["V.a. KHK", "1-Gefäß-KHK", "2-Gefäß-KHK", "3-Gefäß-KHK"])
    diagnose = khk_typ
    if aufnahmemodus == "ambulant":
        ziel_option = st.selectbox("Ziel der Vorstellung", ["zur Verlaufskontrolle", "zur weiteren Diagnostik", "zur Therapieplanung", "Freitext"])
        ziel = ziel_option if ziel_option != "Freitext" else st.text_input("Freitext Ziel")
    else:
        prog_grund_option = st.selectbox("Grund für Progress-Verdacht", ["progrediente Symptomatik", "auffälliges Koronar-CT", "Ischämienachweis im Stress-MRT", "Ischämienachweis in der Myokardszintigraphie", "Freitext"])
        prog_grund = prog_grund_option if prog_grund_option != "Freitext" else st.text_input("Freitext Grund")
        ziel_option = st.selectbox("Ziel der Vorstellung", ["zur Koronarangiographie", "Freitext"])
        ziel_zusatz = ziel_option if ziel_option != "Freitext" else st.text_input("Freitext Ziel")
        ziel = f"bei V.a. Progress aufgrund von {prog_grund} {ziel_zusatz}"
elif leitanlass == "Vorhofflimmern":
    vf_typ = st.selectbox("Typ des Vorhofflimmerns", ["paroxysmal", "persistierend", "permanent"])
    diagnose = f"bei {vf_typ}em Vorhofflimmern"
    ziel_option = st.selectbox("Ziel der Vorstellung", ["zur Verlaufskontrolle", "zur weiteren Diagnostik", "zur Therapieplanung", "Freitext"] if aufnahmemodus == "ambulant" else ["zur elektrischen Kardioversion", "zur Anpassung der medikamentösen Therapie", "Freitext"])
    ziel = ziel_option if ziel_option != "Freitext" else st.text_input("Freitext Ziel")
elif leitanlass == "Symptome":
    symptome = st.multiselect("Leitsymptome", ["typische Angina pectoris", "atypischer thorakaler Schmerz", "Dyspnoe", "Palpitationen", "Synkope"])
    diagnose = ", ".join(symptome)
    ziel_option = st.selectbox("Ziel der Vorstellung", ["zur Verlaufskontrolle", "zur weiteren Diagnostik", "zur Therapieplanung", "Freitext"] if aufnahmemodus == "ambulant" else ["zur Anpassung der medikamentösen Therapie", "zur weiteren Diagnostik und Therapie", "Freitext"])
    ziel = ziel_option if ziel_option != "Freitext" else st.text_input("Freitext Ziel")
else:
    freitext_leitanlass = st.text_input("Freitext zur Aufnahmediagnose")
    diagnose = freitext_leitanlass
    ziel = st.text_input("Ziel der Vorstellung")

freitext_zusatz = st.text_input("Zusätzlicher Diagnosetext (optional)")

# Textgenerierung vorbereiten
geschl = "der o.g. Patientin" if geschlecht == "Patientin (w)" else "des o.g. Patienten"
satz = f"""**Aufnahmegrund**  
Die Aufnahme {geschl} erfolgt bei {diagnose}"""
if freitext_zusatz:
    satz += f" und {freitext_zusatz}"
satz += f" {ziel}.  \n\n"

st.subheader("📄 Generierter Text")
st.markdown(satz)

# Teil 2 – Vorbefunde
st.header("2. Kontext & Ziel")
letzter_aufenthalt = st.text_input("Letzter Aufenthalt (z.B. KH XY bei kardialer Dekompensation)")
therapie = st.text_input("Therapie im letzten Aufenthalt (z.B. Rekompensation mittels Diurese)")
echo = st.text_input("Echokardiographischer Befund (nur bei Vitium)")
lvef = st.selectbox("LVEF-Funktion", ["erhaltener", "gering reduzierter", "mittelgradig reduzierter", "hochgradig reduzierter"])
lvef_wert = st.text_input("LVEF-Wert")

# Teil 3 – Symptomatik
st.header("3. Symptomatik")
belastbarkeit = st.selectbox("Kardiopulmonale Belastbarkeit", ["uneingeschränkte", "gering eingeschränkte", "mäßig eingeschränkte", "deutlich eingeschränkte"])
dyspnoe = st.selectbox("Dyspnoe NYHA", ["NYHA I", "NYHA II", "NYHA III", "NYHA IV"])
aktivitaeten = st.text_input("Alltägliche Aktivitäten")
aktiv_level = st.selectbox("Aktivitätseinschränkung", ["uneingeschränkt", "entsprechend nur eingeschränkt"])

symptom_liste = [
    "typische Angina pectoris", "Dyspnoe", "Schwindel", "Synkopen",
    "subjektive Herzrhythmusstörungen", "Orthopnoe", "Nykturie",
    "periphere Ödeme", "Claudicatio"
]

verneint = st.multiselect("Folgende Symptome wurden verneint:", symptom_liste)

angaben = []
if "Schwindel" not in verneint and st.checkbox("Schwindel vorhanden"):
    schwindel_auspraegung = st.selectbox("Ausprägung Schwindel", ["leicht", "mittel", "deutlich"])
    schwindel_qualitaet = st.text_input("Qualität Schwindel")
    schwindel_belastung = st.selectbox("Belastungsabhängigkeit", ["nein", "Belastung", "Lageänderung", "keine Trigger ersichtlich"])
    angaben.append(f"Es besteht Schwindel, Ausprägung {schwindel_auspraegung}, Qualität {schwindel_qualitaet}, abhängig von: {schwindel_belastung}.")

if "Synkopen" not in verneint and st.checkbox("Synkope vorhanden"):
    synkope_anzahl = st.text_input("Anzahl Synkopen")
    synkope_dauer = st.text_input("in welchem Zeitraum")
    synkope_belastung = st.text_input("Belastungsabhängigkeit Synkopen")
    angaben.append(f"Synkopen: {synkope_anzahl} in {synkope_dauer}, {synkope_belastung}.")

nykturie = st.text_input("Nykturie (z.B. 1-2x/Nacht)")
if nykturie:
    angaben.append(f"Nykturie: {nykturie}x/Nacht.")

symptom_freitexte = {}
for symptom in symptom_liste:
    if symptom not in verneint and symptom not in ["Schwindel", "Synkopen"]:
        if symptom == "typische Angina pectoris":
            angina_beschreibung = st.selectbox("Angina-Beschreibung", [
                "bei schwerer körperlicher Belastung, entsprechend CCS I",
                "bei moderater körperlicher Belastung, entsprechend CCS II",
                "bei leichter körperlicher Belastung, entsprechend CCS III",
                "in Ruhe, entsprechend CCS IV"
            ])
            symptom_freitexte[symptom] = angina_beschreibung
        else:
            beschreibung = st.text_input(f"Weitere Beschreibung zu: {symptom}")
            if beschreibung:
                symptom_freitexte[symptom] = beschreibung

bp = st.text_input("Blutdruck in der Häuslichkeit")
nicht_bekannt = st.multiselect("Folgende Erkrankungen sind nicht bekannt:", ["Schilddrüsenerkrankungen", "Nierenerkrankungen", "Lungenerkrankungen"])


# Teil 4 – Weitere Anamnese
st.header("4. Weitere Anamnese")
tumor_verneint = st.checkbox("Keine Tumoranamnese")
blutung_verneint = st.checkbox("Keine relevante Blutung in der Vergangenheit")
infekt_verneint = st.checkbox("Kein akuter Infekt bei Vorstellung")
stuhl_miktion_verneint = st.checkbox("Stuhlgang und Miktion unauffällig")
zusatz_anamnese = st.text_input("Optionaler Freitext zur Allgemeinanamnese")

cvrf = st.multiselect("CV-Risikofaktoren", [
    "arterielle Hypertonie", "Hyperlipidämie", "positive Familienanamnese",
    "Diabetes mellitus Typ I", "Diabetes mellitus Typ II",
    "Lipoprotein(a)-Erhöhung", "ehemaliger Nikotingebrauch", "fortgesetzter Nikotingebrauch"
])

familie = st.selectbox("Familienstand / Wohnen", ["Alleinlebend", "mit Partner/Familie lebend", "in Pflegeeinrichtung"])
pflegegrad = st.selectbox("Pflegegrad", ["kein PG", "PG I", "PG II", "PG III"])
pflegehilfe = st.selectbox("Pflegeunterstützung", ["kein PD", "Haushaltshilfe", "Pflegedienst"])
frequenz = ""
if pflegegrad != "kein PG":
    frequenz = st.text_input("Frequenz der Unterstützung (z.B. 2x/Woche)")
phq = st.text_input("PHQ-9 Punktzahl")

# Teil 5 – Noxen
st.header("5. Noxen")
nikotin_status = st.selectbox("Nikotingebrauch", ["kein Gebrauch", "ehemals", "aktuell"])
nikotin_menge = ""
nikotin_py = ""
if nikotin_status in ["ehemals", "aktuell"]:
    nikotin_py = st.text_input("Packyears (z.B. 20 py)")
if nikotin_status == "aktuell":
    nikotin_menge = st.text_input("Aktueller Konsum (z.B. 10 Zigaretten/Tag)")

alkohol_status = st.selectbox("Alkoholkonsum", ["kein Gebrauch", "ehemals", "aktuell"])
alkohol_details = ""
if alkohol_status == "aktuell":
    alkohol_details = st.text_input("Beschreibung Alkoholkonsum (z.B. gelegentlich 1 Bier)")

drogen_details = st.text_input("Drogenanamnese (Freitext, z.B. früherer Cannabiskonsum)")

# Button und Textgenerierung
if st.button("📝 Text generieren"):
    geschl = "der o.g. Patientin" if geschlecht == "Patientin (w)" else "des o.g. Patienten"
    artikel_gross = "Die" if geschlecht == "Patientin (w)" else "Der"
    artikel_klein = "die" if geschlecht == "Patientin (w)" else "der"
    berichtende_person = "Patientin" if geschlecht == "Patientin (w)" else "Patient"

    satz = f"""**Aufnahmegrund**  
Die Aufnahme {geschl} erfolgt bei {diagnose}"""
    if freitext_zusatz:
        satz += f" und {freitext_zusatz}"
    satz += f" {ziel}.  \n\n"

# Vorbefunde
    satz += "**Vorbefunde**  \n"
    if letzter_aufenthalt:
        satz += f"{artikel_gross} {berichtende_person} war zuletzt stationär im {letzter_aufenthalt}.  \n"
    if therapie:
        satz += f"Hier {therapie}.  \n"
    if leitanlass == "Vitium" and echo:
        satz += f"Es erfolgte die echokardiographische Darstellung der {diagnose} mit {echo} bei {lvef} LVEF von {lvef_wert}%.  \n"
    satz += "\n"

    # Anamnese
    satz += "**Anamnese**  \n"
    satz += f"Im Anamnesegespräch berichtet {artikel_klein} {berichtende_person} über eine {belastbarkeit} kardiopulmonale Belastbarkeit mit Dyspnoe entsprechend {dyspnoe}.  \n"
    satz += f"Alltägliche Aktivitäten wie {aktivitaeten} können {aktiv_level} durchgeführt werden.  \n\n"

    # Symptome
    satz += "**Symptome**  \n"
    for a in angaben:
        satz += f"- {a}  \n"
    for symptom, text in symptom_freitexte.items():
        satz += f"- {symptom}: {text}.  \n"
    satz += "\n"

    # Weitere Angaben
    satz += "**Weitere Angaben**  \n"
    if verneint:
        satz += f"- Verneinte Beschwerden: {liste_mit_und(verneint)}  \n"
    if nicht_bekannt:
        organe = []
        if "Schilddrüsenerkrankungen" in nicht_bekannt:
            organe.append("Schilddrüse")
        if "Nierenerkrankungen" in nicht_bekannt:
            organe.append("Nieren")
        if "Lungenerkrankungen" in nicht_bekannt:
            organe.append("Lunge")
        satz += f"- Keine Erkrankungen der {liste_mit_und(organe)} bekannt  \n"
    if tumor_verneint:
        satz += "- Keine Tumoranamnese  \n"
    if blutung_verneint:
        satz += "- Keine relevante Blutung in der Vergangenheit  \n"
    if infekt_verneint:
        satz += "- Kein akuter Infekt bei Vorstellung  \n"
    if stuhl_miktion_verneint:
        satz += "- Stuhlgang und Miktion unauffällig  \n"
    if zusatz_anamnese:
        satz += f"- {zusatz_anamnese}  \n"
    if cvrf:
        satz += f"- CV-Risikofaktoren: {liste_mit_und(cvrf)}  \n"

    # Noxen
    satz += "**Noxen**  \n"
    if nikotin_status != "kein Gebrauch":
        satz += f"- Nikotinkonsum: {nikotin_status}"
        if nikotin_status == "aktuell" and nikotin_menge:
            satz += f", aktuell {nikotin_menge}"
        if nikotin_py:
            satz += f", {nikotin_py}"
        satz += "  \n"
    else:
        satz += "- Kein Nikotinkonsum  \n"

    if alkohol_status != "kein Gebrauch":
        satz += f"- Alkoholkonsum: {alkohol_status}"
        if alkohol_status == "aktuell" and alkohol_details:
            satz += f", {alkohol_details}"
        satz += "  \n"
    else:
        satz += "- Kein Alkoholkonsum  \n"

    if drogen_details:
        satz += f"- Drogenanamnese: {drogen_details}  \n"
    else:
        satz += "- Keine Drogenanamnese bekannt  \n"
        
    satz += f"- Familienstand / Pflege: {familie}, {pflegegrad}, {pflegehilfe}"
    if pflegegrad != "kein PG" and frequenz:
        satz += f" ({frequenz})"
    satz += "  \n"
    if phq:
        satz += f"- PHQ-9: {phq} Punkte  \n"



# Ausgabe
st.subheader("📄 Generierter Text")
st.markdown(satz)
