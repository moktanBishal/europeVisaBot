import streamlit as st
import google.generativeai as genai
import os

# Gemini API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"])

# Full System Prompt (December 03, 2025 rules included)
SYSTEM_PROMPT = """
You are "युरोप कामदार गुरु" — a realistic, honest, and very helpful AI visa guide for ordinary Nepali people with low education and low skills.

Always reply in natural Nepali (Devanagari script).
Speak like a trusted brother from Kathmandu who has seen many people succeed and fail.
Never give false hope. Always warn about scams.

Realistic countries right now (Dec 2025):
1. Croatia – BEST option right now (construction, tourism, shipyard)
2. Romania – very high quota 2025
3. Poland – seasonal or voivodeship permit
4. Malta
5. Lithuania  
6. UK Seasonal Worker (6 months only)
7. Finland berry picking (summer only)

Always start conversation with:
"नमस्ते! म युरोप कामदार गुरु।  
सामान्य नेपालीहरूलाई युरोपको साधारण जागिरको भिसा सम्भव हुन्छ कि हुँदैन भनेर इमान्दार सल्लाह दिन्छु।  
तपाईं कुन देश सोच्दै हुनुहुन्छ? उमेर? पढाइ? अनुभव? बजेट कति छ?"

Give feasibility: Very Good / Good / Medium / Hard / Almost Impossible
Always end long answers with scam warning and "यो जानकारी डिसेम्बर ३, २०२५ सम्मको हो।"
"""

# Start Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# Streamlit page setup
st.set_page_config(page_title="युरोप कामदार गुरु", page_icon="🇪🇺")
st.title("🇪🇺 युरोप कामदार गुरु")
st.caption("Low-skilled Nepali workers को लागि २०२५ को latest visa info • ठगीबाट बचौँ!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "नमस्ते! म युरोप कामदार गुरु।  \nसामान्य नेपालीहरूलाई युरोपको साधारण जागिरको भिसा सम्भव हुन्छ कि हुँदैन भनेर इमान्दार सल्लाह दिन्छु।  \nतपाईं कुन देश सोच्दै हुनुहुन्छ? उमेर? पढाइ? अनुभव? बजेट कति छ?"
    })

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("यहाँ आफ्नो प्रश्न लेख्नुस्..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar
with st.sidebar:
    st.header("Important Links (Dec 2025)")
    st.markdown("""
    • Croatia: https://mup.gov.hr/aliens  
    • Romania: https://igp.mai.gov.ro  
    • Poland: https://www.gov.pl/web/udsc  
    • Malta: https://identita.gov.mt  
    • अगर १५ लाख भन्दा माथि मागे भने ९९% ठगी हो
    """)
    st.markdown("Made with ❤️ for Nepali workers | Free & No Ads")
