import streamlit as st
from datetime import datetime
import pandas as pd
import urllib.parse

def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🔒 Είσοδος</h2>", unsafe_allow_html=True)
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

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(
    page_title="Price Analyzer 2026",
    page_icon="📊",
    layout="centered"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    [data-testid="stMetricValue"] { font-size: 40px; color: #2c3e50; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .main-price {
        font-size: 42px !important;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #d5d8dc;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Βάση Δεδομένων
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
    "10.200": ["19.449", "11.893", "61,15%", "2.641", "13,58%", "1.427", "7,34%", "3.488", "17,93%"],
    "10.400": ["19.744", "12.110", "61,34%", "2.641", "13,38%", "1.453", "7,36%", "3.540", "17,93%"],
    "10.600": ["20.038", "12.326", "61,51%", "2.641", "13,18%", "1.479", "7,38%", "3.592", "17,93%"],
    "10.800": ["20.333", "12.543", "61,69%", "2.641", "12,99%", "1.505", "7,40%", "3.644", "17,92%"],
    "11.000": ["20.627", "12.759", "61,86%", "2.641", "12,80%", "1.531", "7,42%", "3.696", "17,92%"],
    "11.200": ["20.922", "12.976", "62,02%", "2.641", "12,62%", "1.557", "7,44%", "3.748", "17,91%"],
    "11.400": ["21.216", "13.192", "62,18%", "2.641", "12,45%", "1.583", "7,46%", "3.800", "17,91%"],
    "11.600": ["21.511", "13.409", "62,34%", "2.641", "12,28%", "1.609", "7,48%", "3.852", "17,91%"],
    "11.800": ["21.805", "13.625", "62,49%", "2.641", "12,11%", "1.635", "7,50%", "3.904", "17,90%"],
    "12.000": ["22.100", "13.842", "62,63%", "2.641", "11,95%", "1.661", "7,52%", "3.956", "17,90%"],
    "12.200": ["22.395", "14.059", "62,78%", "2.641", "11,79%", "1.687", "7,53%", "4.008", "17,90%"],
    "12.400": ["22.689", "14.275", "62,92%", "2.641", "11,64%", "1.713", "7,55%", "4.060", "17,89%"],
    "12.600": ["22.984", "14.492", "63,05%", "2.641", "11,49%", "1.739", "7,57%", "4.112", "17,89%"],
    "12.800": ["23.278", "14.708", "63,18%", "2.641", "11,35%", "1.765", "7,58%", "4.164", "17,89%"],
    "13.000": ["23.573", "14.925", "63,31%", "2.641", "11,20%", "1.791", "7,60%", "4.216", "17,88%"],
    "13.500": ["24.309", "15.466", "63,62%", "2.641", "10,86%", "1.856", "7,64%", "4.346", "17,88%"],
    "14.000": ["25.045", "16.007", "63,91%", "2.641", "10,55%", "1.921", "7,67%", "4.476", "17,87%"],
    "14.500": ["25.782", "16.549", "64,19%", "2.641", "10,24%", "1.986", "7,70%", "4.606", "17,87%"],
    "15.000": ["26.517", "17.090", "64,45%", "2.641", "9,96%", "2.051", "7,73%", "4.735", "17,86%"],
    "15.500": ["27.253", "17.631", "64,69%", "2.641", "9,69%", "2.116", "7,76%", "4.865", "17,85%"],
    "16.000": ["27.990", "18.173", "64,93%", "2.641", "9,44%", "2.181", "7,79%", "4.995", "17,85%"],
    "16.500": ["28.726", "18.714", "65,15%", "2.641", "9,19%", "2.246", "7,82%", "5.125", "17,84%"],
    "17.000": ["29.462", "19.255", "65,36%", "2.641", "8,96%", "2.311", "7,84%", "5.255", "17,84%"],
    "17.500": ["30.199", "19.797", "65,56%", "2.641", "8,75%", "2.376", "7,87%", "5.385", "17,83%"],
    "18.000": ["30.935", "20.338", "65,74%", "2.641", "8,54%", "2.441", "7,89%", "5.515", "17,83%"],
    "18.500": ["31.671", "20.879", "65,92%", "2.641", "8,34%", "2.506", "7,91%", "5.645", "17,82%"],
    "19.000": ["32.407", "21.421", "66,10%", "2.641", "8,15%", "2.570", "7,93%", "5.775", "17,82%"],
    "19.500": ["33.143", "21.962", "66,26%", "2.641", "7,97%", "2.635", "7,95%", "5.905", "17,82%"],
    "20.000": ["33.879", "22.503", "66,42%", "2.641", "7,80%", "2.700", "7,97%", "6.035", "17,81%"]
}

# 4. Κεντρικό UI
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
        
        st.info("💡 Αντιγράψτε το παρακάτω για κοινοποίηση:")
        st.code(report, language="markdown")

        # --- ΣΥΣΤΗΜΑ SHARE ΓΙΑ MOBILE ---
        share_text = urllib.parse.quote(report)
        subject_email = urllib.parse.quote("MDN motorcycles Ανάλυση τιμής εισαγωγής απο GB")
        
        st.markdown("### 📲 Κοινοποίηση σε Social")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'''<a href="https://wa.me{share_text}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">🟢 WhatsApp</div>
                </a>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<a href="viber://forward?text={share_text}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#7360f2;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:10px;">🟣 Viber</div>
                </a>''', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f'''<a href="fb-messenger://share" target="_blank" style="text-decoration:none;">
                <div style="background-color:#0084FF;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;">🔵 Messenger</div>
                </a>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<a href="instagram://library" target="_blank" style="text-decoration:none;">
                <div style="background-color:#E1306C;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;">📸 Instagram</div>
                </a>''', unsafe_allow_html=True)

        st.markdown(f'''<a href="mailto:?subject={subject_email}&body={share_text}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#ea4335;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-top:10px;">📧 Αποστολή με Email</div>
            </a>''', unsafe_allow_html=True)

        st.caption("Σημείωση: Στο Messenger & Instagram θα χρειαστεί να κάνετε 'Επικόλληση' το κείμενο που αντιγράψατε.")

st.write("---")
st.caption(f"Build: 2026.Web.1.6 | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
