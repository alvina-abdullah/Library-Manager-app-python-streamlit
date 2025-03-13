import streamlit as st
import pandas as pd
import os

# File to store library data
LIBRARY_FILE = "library_data.csv"

# Load or initialize library data
if "books" not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        st.session_state.books = pd.read_csv(LIBRARY_FILE)
    else:
        st.session_state.books = pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Status", "Rating", "Reviews"])

# Save function
def save_data():
    st.session_state.books.to_csv(LIBRARY_FILE, index=False)

# App Title
st.title("📚 Library Manager App")

# --- ADD NEW BOOK ---
st.sidebar.header("➕ Add a New Book")
with st.sidebar.form(key="add_book_form"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "History", "Fantasy", "Other"])
    year = st.number_input("Year", min_value=1800, max_value=2100, step=1)
    add_book = st.form_submit_button("📖 Add Book")
    
    if add_book and title and author:
        new_book = pd.DataFrame([[title, author, genre, year, "Available", None, ""]], 
                                columns=["Title", "Author", "Genre", "Year", "Status", "Rating", "Reviews"])
        st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)
        save_data()
        st.sidebar.success(f"✅ '{title}' added successfully!")

# --- SEARCH & FILTER ---
st.header("🔍 Search & Filter Books")
col1, col2 = st.columns(2)
search_query = col1.text_input("Search by Title or Author")
genre_filter = col2.selectbox("Filter by Genre", ["All"] + list(st.session_state.books["Genre"].unique()), index=0)

# Apply filters
filtered_books = st.session_state.books[
    (st.session_state.books["Title"].str.contains(search_query, case=False, na=False) |
     st.session_state.books["Author"].str.contains(search_query, case=False, na=False))
    & ((genre_filter == "All") | (st.session_state.books["Genre"] == genre_filter))
]

st.dataframe(filtered_books)

# --- BORROW & RETURN ---
st.header("📖 Borrow or Return a Book")
borrow_title = st.text_input("Enter the book title")

col1, col2 = st.columns(2)
if col1.button("📕 Borrow Book"):
    if borrow_title in st.session_state.books["Title"].values:
        index = st.session_state.books[st.session_state.books["Title"] == borrow_title].index[0]
        if st.session_state.books.at[index, "Status"] == "Available":
            st.session_state.books.at[index, "Status"] = "Borrowed"
            save_data()
            st.success(f"✅ You borrowed '{borrow_title}'!")
        else:
            st.error("❌ This book is already borrowed!")
    else:
        st.error("❌ Book not found!")

if col2.button("📗 Return Book"):
    if borrow_title in st.session_state.books["Title"].values:
        index = st.session_state.books[st.session_state.books["Title"] == borrow_title].index[0]
        if st.session_state.books.at[index, "Status"] == "Borrowed":
            st.session_state.books.at[index, "Status"] = "Available"
            save_data()
            st.success(f"✅ '{borrow_title}' returned successfully!")
        else:
            st.error("❌ This book is already available!")
    else:
        st.error("❌ Book not found!")

# --- RATE & REVIEW ---
st.header("⭐ Rate & Review a Book")
rate_title = st.text_input("Enter the book title to rate")
rating = st.slider("Rate this book (1-5 Stars)", 1, 5, 3)
review = st.text_area("Write a review")

if st.button("💬 Submit Review"):
    if rate_title in st.session_state.books["Title"].values:
        index = st.session_state.books[st.session_state.books["Title"] == rate_title].index[0]
        st.session_state.books.at[index, "Rating"] = rating
        st.session_state.books.at[index, "Reviews"] = review
        save_data()
        st.success(f"✅ Review submitted for '{rate_title}'!")
    else:
        st.error("❌ Book not found!")

# --- EXPORT LIBRARY DATA ---
st.header("📤 Export Library Data")
if st.button("📥 Download Library Data"):
    st.session_state.books.to_csv("library_export.csv", index=False)
    with open("library_export.csv", "rb") as file:
        st.download_button(label="Download CSV", data=file, file_name="library_export.csv", mime="text/csv")
    st.success("✅ Library data exported successfully!")

# --- REMOVE BOOK ---
st.header("🗑️ Remove a Book")
remove_title = st.text_input("Enter the book title to remove")

if st.button("❌ Remove Book"):
    if remove_title in st.session_state.books["Title"].values:
        st.session_state.books = st.session_state.books[st.session_state.books["Title"] != remove_title]
        save_data()
        st.success(f"✅ '{remove_title}' removed successfully!")
    else:
        st.error("❌ Book not found!")

# --- FOOTER ---
st.markdown("📖 Manage your library with ease! Made with ❤️ using **Streamlit & Python**")
