import streamlit as st
from datetime import datetime
import pandas as pd
import urllib.parse

def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center; color: #2c3e50;'>🔒 Είσοδος</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Δώστε τον κωδικό πρόσβασης", type="password")
        if st.button("Είσοδος"):
            if pwd == "2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Λάθος κωδικός")
        return False
    return True

if not check_password():
    st.stop()

st.set_page_config(page_title="Price Analyzer 2026", page_icon="📊", layout="centered")

# --- ΠΛΗΡΗΣ ΔΙΟΡΘΩΣΗ ΓΙΑ DARK MODE & ΚΕΙΜΕΝΑ ---
st.markdown("""
    <style>
    /* Φόντο εφαρμογής */
    .stApp { background-color: #f4f4f4; }
    
    /* Επιβολή χρωμάτων σε όλα τα κείμενα για να φαίνονται σε Dark Mode */
    h1, h2, h3, h4, p, span, label { color: #2c3e50 !important; }
    
    /* Ρυθμίσεις Πίνακα: Μαύρα γράμματα σε άσπρο φόντο πάντα */
    table { color: black !important; background-color: white !important; }
    th { color: black !important; background-color: #eeeeee !important; }
    td { color: black !important; background-color: white !important; }
    
    /* Κεντρική Τιμή */
    .main-price { 
        font-size: 42px !important; 
        font-weight: bold; 
        color: #2c3e50 !important; 
        text-align: center; 
        background: white; 
        border-radius: 15px; 
        padding: 15px; 
        margin: 10px 0; 
        border: 1px solid #d5d8dc; 
    }
    
    /* Κουμπί Ανάλυσης */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #3498db; 
        color: white !important; 
        font-weight: bold; 
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

db = {
    "5.000": ["12.364", "6.683", "54,05%", "2.641", "21,36%", "802", "6,49%", "2.238", "18,10%"],
    "5.500": ["13.022", "7.167", "55,04%", "2.641", "20,28%", "860", "6,60%", "2.354", "18,08%"],
    "6.000": ["13.679", "7.650", "55,93%", "2.641", "19,31%", "918", "6,71%", "2.470", "18,06%"],
    "6.500": ["14.336", "8.133", "56,73%", "2.641", "18,42%", "976", "6,81%", "2.586", "18,04%"],
    "7.000": ["14.994", "8.617", "57,47%", "2.641", "17,61%", "1.034", "6,90%", "2.702", "18,02%"],
    "7.500": ["15.651", "9.100", "58,14%", "2.641", "16,87%", "1.092", "6,98%", "2.818", "18,01%"],
    "8.000": ["16.308", "9.583", "58,76%", "2.641", "16,19%", "1.150", "7,05%", "2.934", "17,99%"],
    "8.200": ["16.571", "9.777", "59,00%", "2.641", "15,94%", "1.173", "7,08%", "2.980", "17,98%"],
    "8.400": ["16.834", "9.970", "59,23%", "2.641", "15,69%", "1.196", "7,10%", "3.027", "17,98%"],
    "8.600": ["17.097", "10.163", "59,44%", "2.641", "15,45%", "1.220", "7,14%", "3.073", "17,97%"],
    "8.800": ["17.357", "10.357", "59,68%", "2.641", "15,19%", "1.245", "7,16%", "3.124", "17,97%"],
    "9.000": ["17.652", "10.594", "59,91%", "2.641", "14,94%", "1.271", "7,19%", "3.176", "17,96%"],
    "9.200": ["17.917", "10.811", "60,14%", "2.641", "14,69%", "1.297", "7,21%", "3.228", "17,96%"],
    "9.400": ["18.271", "11.027", "60,35%", "2.641", "14,45%", "1.323", "7,24%", "3.280", "17,95%"],
    "9.600": ["18.566", "11.244", "60,56%", "2.641", "14,22%", "1.349", "7,27%", "3.332", "17,95%"],
    "9.800": ["18.860", "11.460", "60,76%", "2.641", "14,00%", "1.375", "7,29%", "3.384", "17,94%"],
    "10.000": ["19.155", "11.677", "60,96%", "2.641", "13,79%", "1.401", "7,31%", "3.436", "17,94%"],
    "20.000": ["33.879", "22.503", "66,42%", "2.641", "7,80%", "2.700", "7,97%", "6.035", "17,81%"]
}

st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Price Analyzer</h2>", unsafe_allow_html=True)
st.write("---")

if datetime.now() > datetime(2026, 12, 24):
    st.error("System Error: Insert Coins to continue")
else:
    option = st.selectbox("Τιμή αγγελίας σε λίρες (£)", list(db.keys()))

    if st.button("ΑΝΑΛΥΣΗ ΤΙΜΗΣ"):
        v = db[option]
        st.markdown(f'<div class="main-price">{v[0]} €</div>', unsafe_allow_html=True)
        
        analysis_data = {
            "Κατηγορία": ["🇬🇧 UK", "🇬🇷 GR", "⚖️ Τέλη Ταξ", "🧾 ΦΠΑ"],
            "Ποσό (€)": [v[1], v[3], v[5], v[7]],
            "Ποσοστό": [v[2], v[4], v[6], v[8]]
        }
        st.table(pd.DataFrame(analysis_data))
        
        report = (f"📊 *REPORT ANALYZER 2026*\n"
                  f"--------------------------\n"
                  f"💷 Price GBP: {option} £\n"
                  f"💶 Final Price: {v[0]} €\n"
                  f"--------------------------\n"
                  f"🇬🇧 UK: {v[1]} ({v[2]})\n"
                  f"🇬🇷 GR: {v[3]} ({v[4]})\n"
                  f"⚖️ Tax: {v[5]} ({v[6]})\n"
                  f"🧾 VAT: {v[7]} ({v[8]})")
        
        st.markdown("<h4 style='color: #2c3e50 !important; margin-top:20px;'>💡 Αντιγράψτε το παρακάτω:</h4>", unsafe_allow_html=True)
        st.code(report, language="markdown")

        share_text = urllib.parse.quote(report)
        subject_email = urllib.parse.quote("MDN motorcycles Ανάλυση τιμής")
        
        # Ο ΤΙΤΛΟΣ ΠΟΥ ΘΑ ΦΑΙΝΕΤΑΙ ΠΑΝΤΑ
        st.markdown("<h3 style='color: #2c3e50 !important; margin-top:25px;'>📲 Κοινοποίηση</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # ΣΤΑΘΕΡΟ LINK ΓΙΑ WHATSAPP ΣΕ IPHONE
            st.markdown(f'<a href="whatsapp://send?text={share_text}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white !important;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">🟢 WhatsApp</div></a>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<a href="viber://forward?text={share_text}" target="_blank" style="text-decoration:none;"><div style="background-color:#7360f2;color:white !important;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">🟣 Viber</div></a>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown(f'<a href="fb-messenger://share" target="_blank" style="text-decoration:none;"><div style="background-color:#0084FF;color:white !important;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">🔵 Messenger</div></a>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<a href="instagram://library" target="_blank" style="text-decoration:none;"><div style="background-color:#E1306C;color:white !important;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">📸 Instagram</div></a>', unsafe_allow_html=True)

        st.markdown(f'<a href="mailto:?subject={subject_email}&body={share_text}" target="_blank" style="text-decoration:none;"><div style="background-color:#ea4335;color:white !important;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-top:5px;">📧 Email</div></a>', unsafe_allow_html=True)

st.write("---")
st.caption(f"Build: 2026.Web.2.0 | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
