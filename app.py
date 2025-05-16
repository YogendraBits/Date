import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_player import st_player
import sqlite3
import json
from datetime import datetime
import requests

# --- Page Setup ---
st.set_page_config(page_title="Virtual Date Invite 💕", layout="wide",initial_sidebar_state="collapsed")

# --- DB Setup ---
conn = sqlite3.connect('responses.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    special_msg TEXT,
    submitted_at TEXT,
    status TEXT
)''')
conn.commit()

with st.sidebar:
    st_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ", playing=True, loop=True)
# --- Admin Login ---
st.sidebar.title("Admin Login")
admin_logged_in = False
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    if username == "admin" and password == "adminpassword":
        admin_logged_in = True
        st.sidebar.success("Logged in as admin!")
        st.session_state['admin_logged_in'] = True
    else:
        st.sidebar.error("Incorrect credentials")
elif st.session_state.get('admin_logged_in'):
    admin_logged_in = True




# --- Background Music ---
# audio_file = open("music.mp3", "rb")
# st.audio(audio_file.read(), format='audio/mp3')



def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- 1. Isometric Heart Filled Animation ---
isometric_heart = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json")
st_lottie(isometric_heart, height=200, key="isometric_heart")


# --- Image Carousel ---
st.markdown("### Some moments and memories 💞")
carousel_images = [
    ("images/kitten1.jpg", "Remember our first call? 😸"),
    ("images/kitten2.jpg", "This reminds me of you 💖"),
    ("images/kitten3.jpg", "I can't wait to make more memories like this.")
]

cols = st.columns(len(carousel_images))
for i, (img_url, caption) in enumerate(carousel_images):
    with cols[i]:
        st.image(img_url, use_container_width=True)
        st.caption(caption)


# --- Title and Intro ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #FF4B4B;'>Hey love 💌</h1>
        <h3>I have something to ask you...</h3>
    </div>
""", unsafe_allow_html=True)
# --- The Question ---
st.markdown("""
    <div style="
        text-align: center; 
        background: #fff8e7;
        padding: 10px; 
        border-radius: 15px; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-width: 1500px;
        margin: 20px auto;
        color: #b22222;
    ">
        <h2 style="margin-bottom: 10px;">Would you like to go on a virtual lunch/dinner date with me? 🍽️💑</h2>
        <p style="font-size: 1.1rem; color: #800000;">Let’s create memories together, even from miles apart.</p>
    </div>
""", unsafe_allow_html=True)

# Centering buttons nicely with some padding
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    if st.button("💕 Yes, of course!", use_container_width=True):
        st.session_state['answer'] = "yes"
with col2:
    if st.button("🥲 Rain check?", use_container_width=True):
        st.session_state['answer'] = "no"

if st.session_state.get('answer') == "yes":
    st.success("🎉 Yay! You made my day! 🥰", icon="🎉")
    st.subheader("💌 Let's set up our date!")
    with st.form("date_form", clear_on_submit=False):
        date_choice = st.date_input("📅 Pick a day for our date", min_value=datetime.today())
        time_choice = st.time_input("⏰ Pick a time")
        special_msg = st.text_area("✨ Anything special you'd like for our date?")

        submitted = st.form_submit_button("💌 Confirm Date", use_container_width=True)

        if submitted:
            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO responses (date, time, special_msg, submitted_at, status) VALUES (?, ?, ?, ?, ?)",
                (date_choice.strftime("%Y-%m-%d"), time_choice.strftime("%H:%M:%S"), special_msg, submitted_at, "accepted")
            )
            conn.commit()
            st.balloons()
            st.snow()
            st.markdown(
                f"**Awesome! I can't wait to see you on "
                f"{date_choice.strftime('%A, %B %d, %Y')} at {time_choice.strftime('%I:%M %p')}!**"
            )
            if special_msg.strip():
                st.info(f"📝 I'll remember this: \"{special_msg}\"")
            st.session_state.pop('answer', None)

elif st.session_state.get('answer') == "no":
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO responses (date, time, special_msg, submitted_at, status) VALUES (?, ?, ?, ?, ?)",
        ("", "", "", submitted_at, "declined")
    )
    conn.commit()
    st.warning("💛 No worries! Let’s find another time soon.")
    st.session_state.pop('answer', None)


# --- Admin View ---
if admin_logged_in:
    st.markdown("---")
    st.subheader("📋 Submitted Responses")
    rows = c.execute("SELECT * FROM responses ORDER BY submitted_at DESC").fetchall()

    if not rows:
        st.info("No responses yet.")
    else:
        for row in rows:
            st.markdown(f"""
                - **ID**: {row[0]}
                - **Date**: {row[1] or '—'}
                - **Time**: {row[2] or '—'}
                - **Message**: {row[3] or '—'}
                - **Submitted at**: {row[4]}
                - **Status**: {row[5].capitalize()}
            """)
            if st.button(f"🗑️ Delete ID {row[0]}", key=f"del_{row[0]}"):
                c.execute("DELETE FROM responses WHERE id = ?", (row[0],))
                conn.commit()
                st.success(f"Deleted response ID {row[0]}")
                st.rerun()
