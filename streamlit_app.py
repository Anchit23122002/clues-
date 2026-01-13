import streamlit as st
from supabase import create_client, Client

# 1. Database Connection
# Replace with your actual Supabase details
URL = "YOUR_SUPABASE_URL"
KEY = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(URL, KEY)

st.set_page_config(page_title="Clue Checker", page_icon="📝")

st.title("📝 Crossword Clue Manager")
st.info("Check if a clue exists before adding it to your website.")

# 2. Search & Verification Section
st.subheader("1. Check for Duplicate")
search_query = st.text_input("Enter clue to search:", placeholder="Type clue here...")

if search_query:
    # Search for exact or partial matches
    response = supabase.table("clues_list").select("clue").ilike("clue", f"%{search_query}%").execute()
    
    if response.data:
        st.error(f"❌ Match Found! This clue (or similar) already exists:")
        for item in response.data:
            st.write(f"• {item['clue']}")
    else:
        st.success("✅ No matches found. You can use this clue!")

st.divider()

# 3. Add New Clue Section
st.subheader("2. Add New Clue")
with st.form("add_form", clear_on_submit=True):
    new_clue = st.text_area("Write your new clue here:", height=100)
    submit_button = st.form_submit_button("Save Clue to Database")

    if submit_button:
        if new_clue.strip():
            # Clean the string (remove extra whitespace)
            clean_clue = new_clue.strip()
            
            try:
                # Attempt to insert into Supabase
                supabase.table("clues_list").insert({"clue": clean_clue}).execute()
                st.success(f"Successfully saved: '{clean_clue}'")
            except Exception:
                # If 'clue' is a Unique Primary Key, it will fail if it exists
                st.error("This exact clue is already in the database!")
        else:
            st.warning("Please enter a clue before saving.")
