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
    init_db()

    st.set_page_config(page_title="File Upload & Admin Panel", layout="wide")
    st.title("📂 File Upload and Admin Page")

    menu = ["User Upload", "Admin Page", "Main Admin"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # ---------- USER UPLOAD ----------
    if choice == "User Upload":
        st.header("📤 Upload File")

        uploaded_file = st.file_uploader(
            "Upload a file",
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
            st.write("**File Details:**")
            st.json({
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type
            })

            if st.button("💾 Save to Database"):
                data = uploaded_file.getvalue()
                save_file_to_db(uploaded_file.name, uploaded_file.type, data)
                st.success(f"✅ {uploaded_file.name} saved successfully!")

    # ---------- ADMIN PAGE ----------
    elif choice == "Admin Page":
        st.header("👨‍💻 Admin: View Files")

        files = get_all_files()

        if files:
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
        else:
            st.info("No files uploaded yet.")

    # ---------- MAIN ADMIN LOGIN ----------
    elif choice == "Main Admin":
        st.header("🔐 Main Admin Login")

        # Session state
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.login_failed = False

        # Login form
        use = st.text_input("Enter Username:")
        pas = st.text_input("Enter Password:", type="password")

        if st.button("🔑 Login"):
            if use == "leo" and pas == "123":
                st.session_state.logged_in = True
                st.session_state.login_failed = False
            else:
                st.session_state.logged_in = False
                st.session_state.login_failed = True

        # After login success
        if st.session_state.logged_in:
            st.success("✅ Login Successful!")

            file_path = "print.docx"

            if os.path.exists(file_path):
                st.success(f"📄 File Ready: {os.path.basename(file_path)}")

                if st.button("📂 Open File"):
                    with open(file_path, "rb") as f:
                        file_data = f.read()

                    st.download_button(
                        label="⬇️ Open / Download File",
                        data=file_data,
                        file_name=os.path.basename(file_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            else:
                st.error("❌ File not found!")

        # Login failed
        elif st.session_state.login_failed:
            st.error("❌ Wrong Username or Password!")

            # GIF display
            st.image(
                "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif",
                caption="Access Denied 🚫",
                use_column_width=True
            )

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    main()
