import streamlit as st
import pdfplumber
import re
import pandas as pd
from io import BytesIO

# --- 🔒 Sécurité : mot de passe simple ---
def check_password():
    """Affiche un champ de mot de passe avant d'accéder à l'app"""
    st.sidebar.title("🔒 Accès sécurisé")
    password = st.sidebar.text_input("Entrez le mot de passe :", type="password")

    # Change ici le mot de passe si tu veux un autre
    if password == "fiducial2025":
        return True
    elif password:
        st.error("Mot de passe incorrect.")
        return False
    else:
        st.info("Veuillez entrer le mot de passe pour accéder à l'application.")
        return False

# Si le mot de passe est faux, on bloque tout le reste du code
if not check_password():
    st.stop()
# ----------------------------------------

# Fonction d’analyse du PDF
def analyser_pdf(file):
    patterns = [
        r"\bCAM\s*T?\d+(?:\.\d+)?",
        r"\bCaméra Type\s*\d+",
        r"\bVIDEOPORTIER\b",
        r"\bCOUP DE POING\b",
        r"\bSERRURE\b",
        r"\bLECTEUR BADGE\b",
        r"\bDETECTEUR\b"
    ]
    results = []

    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for pattern in patterns:
                for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                    snippet = text[max(0, match.start()-40):match.end()+40].replace("\n", " ")
                    results.append({
                        "Page": i,
                        "Motif trouvé": match.group(0),
                        "Contexte": snippet
                    })
    return pd.DataFrame(results)

# Interface Streamlit
st.set_page_config(page_title="Analyseur de Plans Fiducial", layout="centered")
st.title("🔍 Analyse automatique de plans de sécurité")
st.write("Importez un plan PDF pour identifier les systèmes de sûreté (caméras, détecteurs, interphones, etc.)")

uploaded_file = st.file_uploader("📂 Sélectionnez un plan PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Analyse en cours..."):
        df = analyser_pdf(uploaded_file)
    st.success(f"✅ Analyse terminée — {len(df)} éléments détectés.")
    st.dataframe(df)

    # Bouton d’export Excel
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Télécharger les résultats (Excel)",
        data=buffer,
        file_name="résultats_analyse.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👆 Déposez un plan PDF pour démarrer l’analyse.")
