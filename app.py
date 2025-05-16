import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_player import st_player
import sqlite3
import json
from datetime import datetime
import requests

# --- Page Setup ---
st.set_page_config(page_title="Virtual Date Invite 💕",
                   layout="wide", initial_sidebar_state="collapsed")

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
    st_player("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
              playing=True, loop=True)
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


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# --- 1. Isometric Heart Filled Animation ---
isometric_heart = load_lottieurl(
    "https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json")
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
    <style>
        /* Container styling */
        .custom-container {
            text-align: center;
            background: #fff8e7;
            padding: 15px 10px;
            border-radius: 15px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            max-width: 95%;
            margin: 20px auto;
            color: #b22222;
            box-sizing: border-box;
        }
        /* Heading and paragraph spacing */
        .custom-container h2 {
            margin-bottom: 10px;
            font-size: 1.5rem;
        }
        .custom-container p {
            font-size: 1.1rem;
            color: #800000;
            margin-top: 0;
        }

        /* Buttons container */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .button-container > div {
            flex: 1 1 200px;  /* flexible width, min 200px */
            max-width: 300px;
        }

        /* On small screens, stack buttons vertically */
        @media (max-width: 480px) {
            .custom-container h2 {
                font-size: 1.25rem;
            }
            .custom-container p {
                font-size: 1rem;
            }
            .button-container {
                flex-direction: column;
                gap: 10px;
            }
            .button-container > div {
                max-width: 100%;
            }
        }
    </style>

    <div class="custom-container">
        <h2>Would you like to go on a virtual lunch/dinner date with me? 🍽️💑</h2>
        <p>Let’s create memories together, even from miles apart.</p>
    </div>
""", unsafe_allow_html=True)

# Buttons in a flex container with some styling to match the CSS class
cols = st.columns(2, gap="large")
with st.container():
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    with cols[0]:
        if st.button("💕 Yes, of course!", use_container_width=True):
            st.session_state['answer'] = "yes"
    with cols[1]:
        if st.button("🥲 Rain check?", use_container_width=True):
            st.session_state['answer'] = "no"
    st.markdown('</div>', unsafe_allow_html=True)


# Rest of your logic unchanged (just to keep it concise here)
if st.session_state.get('answer') == "yes":
    st.success("🎉 Yay! You made my day! 🥰", icon="🎉")
    st.subheader("💌 Let's set up our date!")
    if not st.session_state.get("date_submitted"):
        with st.form("date_form", clear_on_submit=False):
            date_choice = st.date_input(
                "📅 Pick a day for our date", min_value=datetime.today())
            time_choice = st.time_input("⏰ Pick a time")
            special_msg = st.text_area(
                "✨ Anything special you'd like for our date?")
            submitted = st.form_submit_button(
                "💌 Confirm Date", use_container_width=True)

            if submitted:
                submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute(
                    "INSERT INTO responses (date, time, special_msg, submitted_at, status) VALUES (?, ?, ?, ?, ?)",
                    (date_choice.strftime("%Y-%m-%d"), time_choice.strftime("%H:%M:%S"),
                     special_msg, submitted_at, "accepted")
                )
                conn.commit()
                st.session_state["date_choice"] = date_choice
                st.session_state["time_choice"] = time_choice
                st.session_state["special_msg"] = special_msg
                st.session_state["date_submitted"] = True
                st.balloons()
                st.snow()

    # Show confirmation card if form has been submitted
    if st.session_state.get("date_submitted"):
        date_choice = st.session_state["date_choice"]
        time_choice = st.session_state["time_choice"]
        special_msg = st.session_state["special_msg"]

        with st.container():
            st.markdown(
                f"""
                <div style='
                    background-color: #e6ffed;
                    border-left: 6px solid #2ecc71;
                    border-radius: 15px;
                    padding: 20px;
                    margin-top: 25px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    font-family: "Segoe UI", sans-serif;
                '>
                    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                        <div style='font-size: 28px; margin-right: 10px;'>✅</div>
                        <h3 style='color: #2ecc71; margin: 0;'>Date Confirmed!</h3>
                    </div>
                    <p style='font-size: 17px; color: #333; line-height: 1.6;'>
                        <strong>Woohoo! 🎉 I can't wait to see you on<br>
                        <span style='color: #27ae60;'>{date_choice.strftime('%A, %B %d, %Y')}</span> at 
                        <span style='color: #27ae60;'>{time_choice.strftime('%I:%M %p')}</span>!</strong>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if special_msg.strip():
                st.markdown(
                    f"""
                    <div style='
                        background-color: #fff8e6;
                        border-left: 6px solid #ffcd58;
                        border-radius: 10px;
                        padding: 15px;
                        margin-top: 15px;
                        font-family: "Segoe UI", sans-serif;
                    '>
                        <div style='font-size: 20px;'>💌 <strong>Special request:</strong></div>
                        <p style='margin: 5px 0 0; color: #5a4c00;'>“{special_msg}”</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# st.session_state.pop('answer', None)

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
    rows = c.execute(
        "SELECT * FROM responses ORDER BY submitted_at DESC").fetchall()

    if not rows:
        st.info("No responses yet.")
    else:
        # Global CSS styles for cards and buttons
        st.markdown(
            """
            <style>
            body, .container {
                background-color: #f5f7fa;
                padding: 20px;
            }
            .card {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: flex-start;
                border-radius: 14px;
                padding: 20px 24px;
                margin-bottom: 18px;
                background: #fff;
                box-shadow: 0 6px 14px rgba(0,0,0,0.06);
                font-family: 'Inter', system-ui, sans-serif;
                color: #2c3e50;
                min-width: 280px;
                transition: box-shadow 0.3s ease, transform 0.3s ease;
                border-left-width: 8px;
                border-left-style: solid;
            }
            .card:hover {
                box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
                transform: translateY(-4px);
            }
            .status-block {
                flex: 1 1 30%;
                min-width: 150px;
                text-align: right;
            }
            .response-info {
                flex: 1 1 65%;
                min-width: 220px;
            }
            p {
                margin: 6px 0;
                line-height: 1.4;
            }
            @media (max-width: 480px) {
                .card {
                    flex-direction: column !important;
                }
                .response-info, .status-block {
                    min-width: 100% !important;
                    text-align: left !important;
                }
                .status-block {
                    margin-top: 12px;
                }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Status badge colors and icons
        status_color_map = {
            "accepted": "#4CAF50",
            "pending": "#FF9800",
            "declined": "#F44336"
        }

        status_icon_map = {
            "accepted": "✅",
            "pending": "⏳",
            "declined": "❌"
        }

        for row in rows:
            id_, date_, time_, msg, submitted_at, status = row
            status_lower = status.lower()
            status_color = status_color_map.get(status_lower, "#757575")
            status_icon = status_icon_map.get(status_lower, "ℹ️")

            # Build HTML card
            card_html = f"""
            <div class="card" style="border-left-color: {status_color};">
                <div class="response-info">
                    <p style="font-weight: 600; font-size: 1.1rem;">Response ID: {id_}</p>
                    <p style="color: #34495e;">
                        <span style='font-weight: 600; color: #555;'>📅 Date:</span> {date_ or '—'}
                    </p>
                    <p style="color: #34495e;">
                        <span style='font-weight: 600; color: #555;'>⏰ Time:</span> {time_ or '—'}
                    </p>
                    <p>
                        <span style='font-weight: 600; color: #555;'>💬 Message:</span> {msg or '—'}
                    </p>
                </div>
                <div class="status-block">
                    <p style="
                        display: inline-block;
                        background-color: {status_color};
                        color: white;
                        padding: 6px 14px;
                        font-weight: 700;
                        border-radius: 20px;
                        font-size: 0.9rem;
                        box-shadow: 0 3px 8px {status_color}80;
                        user-select: none;
                    ">
                        {status_icon} {status.capitalize()}
                    </p>
                    <p style="margin-top: 14px; color: #7f8c8d; font-size: 0.85rem;">Submitted at:<br>{submitted_at}</p>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            # Delete button without confirmation
            if st.button("🗑️ Delete", key=f"delete_{id_}"):
                c.execute("DELETE FROM responses WHERE id = ?", (id_,))
                conn.commit()
                st.success(f"Response ID {id_} deleted.")
                st.rerun()
