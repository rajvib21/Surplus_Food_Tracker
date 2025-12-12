import streamlit as st
from db import get_conn
from datetime import datetime
from blur_detection import is_blurry
from ocr_summary import extract_text, summarize_text
from recommender import recommend
from utils import nearby_places

def user_dashboard(user):
    st.title("User Dashboard")

    conn = get_conn()
    cur = conn.cursor()

    st.subheader("Upload Surplus Food")
    title = st.text_input("Food title")
    desc = st.text_area("Description")
    qty = st.number_input("Quantity", min_value=1)
    unit = st.selectbox("Unit", ["kg", "litre", "pieces"])
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    img = st.file_uploader("Upload Image")

    if st.button("Submit"):
        img_path = None
        if img:
            img_path = f"static/uploads/{img.name}"
            with open(img_path, "wb") as f:
                f.write(img.getbuffer())

            blurry, val = is_blurry(img_path)
            st.write(f"Blur score: {val:.2f}")
            if blurry:
                st.warning("Image is blurry!")

        cur.execute("""
        INSERT INTO donations (user_id,title,description,quantity,unit,latitude,longitude,image_path,posted_at)
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (user["id"], title, desc, qty, unit, lat, lon, img_path, datetime.now()))
        conn.commit()
        st.success("Donation submitted!")

    st.subheader("Nearby Surplus Food")
    cur.execute("SELECT * FROM donations WHERE is_claimed=0")
    donations = cur.fetchall()

    if lat and lon:
        near = nearby_places(lat, lon, [dict(d) for d in donations], max_km=10)
        for d, dist in near:
            st.write(f"{d['title']} — {dist:.1f} km away")

    st.subheader("Search Recommendation")
    q = st.text_input("What food are you looking for?")
    if q:
        results = recommend([dict(d) for d in donations], q)
        for d, score in results:
            st.write(f"Recommended: {d['title']} — Score {score}")

    st.subheader("Image → Text + Summary")
    image2 = st.file_uploader("Upload for OCR")
    if image2:
        img_path2 = f"static/uploads/{image2.name}"
        with open(img_path2, "wb") as f:
            f.write(image2.getbuffer())
        text = extract_text(img_path2)
        st.write("Extracted:", text)
        st.write("Summary:", summarize_text(text))

    conn.close()
