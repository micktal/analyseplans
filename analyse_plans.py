import pdfplumber
import re
import pandas as pd
from pathlib import Path

# 📄 Mets ici le nom exact de ton fichier PDF (copie-le dans le même dossier)
PDF_FILE = "SLA1-PRO-SUR-CSI-01-ADM-TN-20-PLA-7029-A.pdf"

# 🔍 Motifs à rechercher (tu pourras en ajouter selon les plans)
PATTERNS = [
    r"\bCAM\s*T?\d+(?:\.\d+)?",
    r"\bCaméra Type\s*\d+",
    r"\bVIDEOPORTIER\b",
    r"\bCOUP DE POING\b",
    r"\bSERRURE\b",
    r"\bLECTEUR BADGE\b",
    r"\bDETECTEUR\b"
]

results = []

# 🔧 Ouvre le PDF
with pdfplumber.open(PDF_FILE) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        for pattern in PATTERNS:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                snippet = text[max(0, match.start()-40):match.end()+40].replace("\n", " ")
                results.append({
                    "page": i,
                    "motif_trouvé": match.group(0),
                    "extrait_contexte": snippet
                })

# 📊 Crée un tableau Excel avec les résultats
df = pd.DataFrame(results)
output_file = "résultats_analyse.xlsx"
df.to_excel(output_file, index=False)

print(f"✅ Analyse terminée ! {len(results)} éléments trouvés.")
print(f"📁 Fichier exporté : {output_file}")
