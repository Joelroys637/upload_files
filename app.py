import streamlit as st
import sqlite3
import os
from io import BytesIO

# ------------------ DATABASE SETUP ------------------
def init_db():
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            filetype TEXT,
            data BLOB
        )
    """)
    conn.commit()
    conn.close()

def save_file_to_db(filename, filetype, data):
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("INSERT INTO files (filename, filetype, data) VALUES (?, ?, ?)", 
              (filename, filetype, data))
    conn.commit()
    conn.close()

def get_all_files():
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("SELECT id, filename, filetype FROM files")
    files = c.fetchall()
    conn.close()
    return files

def get_file_by_id(file_id):
    conn = sqlite3.connect("files.db")
    c = conn.cursor()
    c.execute("SELECT filename, filetype, data FROM files WHERE id = ?", (file_id,))
    file = c.fetchone()
    conn.close()
    return file

# ------------------ MAIN APP ------------------
def main():
    st.set_page_config(page_title="File Upload and Admin Viewer", layout="wide")
    st.title("📂 File Upload and Admin Page")

    menu = ["User Upload", "Admin Page","Main Admin"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # ---------- USER UPLOAD ----------
    if choice == "User Upload":
        st.header("📤 Upload File")

        uploaded_file = st.file_uploader(
            "Upload a Word, PDF, or Python file", 
            type=[
        "docx", "doc", "pdf", "txt",
        "py", "java", "cpp", "c", "html", "css", "js",
        "jpg", "jpeg", "png", "gif",
        "xlsx", "xls", "csv",
        "pptx", "ppt",
        "zip", "rar"
    ]
        )

        if uploaded_file is not None:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type
            }
            st.write("**File Details:**")
            st.json(file_details)

            if st.button("Save to Database"):
                data = uploaded_file.getvalue()
                save_file_to_db(uploaded_file.name, uploaded_file.type, data)
                st.success(f"✅ {uploaded_file.name} successfully saved to database!")

    # ---------- ADMIN PAGE ----------
    elif choice == "Admin Page":
        st.header("👨‍💻 Admin: View Mode")

        files = get_all_files()
        if files:
            st.write("### Files in Database:")
            for file in files:
                file_id, filename, filetype = file
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 **{filename}**")
                with col2:
                    st.write(filetype)
                with col3:
                    if st.button("View/Download", key=file_id):
                        file_data = get_file_by_id(file_id)
                        if file_data:
                            fname, ftype, data = file_data
                            st.download_button(
                                label=f"⬇️ Download {fname}",
                                data=BytesIO(data),
                                file_name=fname,
                                mime=ftype
                            )
    elif choice == "Main Admin":
     use = st.text_input("Enter a User Name:")
     pas = st.text_input("Enter a password:", type="password")

     if use == "leo" and pas == "123":

         file_path = "print.docx"

         if os.path.exists(file_path):
             st.success(f"✅ File found: {os.path.basename(file_path)}")

            # 🔘 Button to open file
             if st.button("📂 Open File"):
                 with open(file_path, "rb") as f:
                     file_data = f.read()

                 st.download_button(
                     label="⬇️ Click here to Open / Download",
                     data=file_data,
                     file_name=os.path.basename(file_path),
                     mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                 )

         else:
             st.error("❌ File not found! Please check the path.")

     else:
         st.info("User name and password is wrong pls contact simon...")

 else:
     st.info("No files uploaded yet.")
     else:
         st.info("No files uploaded yet.")

