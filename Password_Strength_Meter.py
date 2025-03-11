import streamlit as st
import re
import random
import string
import pandas as pd
from datetime import datetime, timedelta

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        feedback.append("✅ Strong Password!")
    elif score == 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")

    return score, feedback

# Function to generate a strong password
def generate_strong_password(length=12):
    """Generate a strong password with a mix of uppercase, lowercase, digits, and special characters."""
    if length < 8:
        length = 8  # Ensure minimum length of 8 characters
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to check if the password is common
def is_common_password(password):
    """Check if the password is in a list of common passwords."""
    common_passwords = ["password", "123456", "qwerty", "admin", "letmein", "12345678", "123123", "111111"]
    return password.lower() in common_passwords

# Function to check if the password is already in the last 10 saved passwords
def is_duplicate_password(password, password_history):
    """Check if the password is already in the last 10 saved passwords."""
    last_10_passwords = [entry["password"] for entry in password_history[-10:]]  # Get last 10 passwords
    return password in last_10_passwords

# Function to export passwords to a file
def export_passwords(passwords, filename="generated_passwords.txt"):
    with open(filename, "w") as file:
        for password in passwords:
            file.write(password + "\n")
    st.success(f"✅ Passwords exported to {filename}")

# Streamlit App
def main():
    st.title("🔐 Ultimate Password Strength Meter")
    st.write("Check the strength of your password, generate strong passwords, and manage them securely.")

    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose an option:", ["Check Password Strength", "Generate Password", "Password History", "Export Passwords"])

    # Initialize session state for password history
    if "password_history" not in st.session_state:
        st.session_state.password_history = []

    # Check Password Strength
    if option == "Check Password Strength":
        st.subheader("Check Password Strength")
        password = st.text_input("Enter your password:", type="password")

        if st.button("Check Strength"):
            if is_common_password(password):
                st.error("❌ This password is too common and insecure. Please choose a different one.")
            elif is_duplicate_password(password, st.session_state.password_history):
                st.error("❌ This password has already been used recently. Please choose a different one.")
            else:
                score, feedback = check_password_strength(password)

                # Display scoring dashboard
                st.subheader("Password Strength Score")
                st.progress(score / 4)  # Progress bar (score out of 4)
                st.write(f"**Score:** {score}/4")

                # Display feedback
                st.subheader("Feedback")
                for message in feedback:
                    if "✅" in message:
                        st.success(message)
                    elif "⚠️" in message:
                        st.warning(message)
                    else:
                        st.error(message)

                # Save to password history
                st.session_state.password_history.append({
                    "password": password,
                    "score": score,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    # Generate Password
    elif option == "Generate Password":
        st.subheader("Generate a Strong Password")
        length = st.slider("Password Length", 8, 32, 12)

        if st.button("Generate Password"):
            password = generate_strong_password(length)
            st.success(f"🔐 Here's a strong password: **{password}**")
            st.write("Copy and use this password for better security.")

            # Save to password history
            st.session_state.password_history.append({
                "password": password,
                "score": 4,  # Generated passwords are always strong
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    # Password History
    elif option == "Password History":
        st.subheader("Password History")
        if st.session_state.password_history:
            history_df = pd.DataFrame(st.session_state.password_history)
            st.write(history_df)

            # Download button for password history
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="Download Password History as CSV",
                data=csv,
                file_name="password_history.csv",
                mime="text/csv",
            )
        else:
            st.write("No passwords checked or generated yet.")

    # Export Passwords
    elif option == "Export Passwords":
        st.subheader("Export Passwords")
        if st.session_state.password_history:
            passwords = [entry["password"] for entry in st.session_state.password_history]
            export_passwords(passwords)
        else:
            st.write("No passwords to export.")

if __name__ == "__main__":
    main()
