import re
import streamlit as st

# Mapping of Bengali numerals to English numerals
bengali_to_english_numerals = {
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
}

def convert_bengali_numerals(num_str):
    # Convert Bengali numeral string to English numeral string
    return ''.join(bengali_to_english_numerals.get(digit, digit) for digit in num_str)

def escape_special_characters(text):
    # Escape single quotes and semicolons with a backslash
    return text.replace("'", "\\'").replace(";", "\\;")

def extract_and_split_text(text):
    # Regex pattern to match ayat numbers and their associated text
    pattern = r'\(([০-৯]+)\)\s*(.*?)(?=\(\d+\)|$)'

    # Find all matches of ayat numbers and associated text
    matches = re.findall(pattern, text, re.DOTALL)

    # Extract text parts and convert Bengali numerals to English if needed
    ayat_texts = [escape_special_characters(match[1].strip()) for match in matches]
    ayat_numbers = [convert_bengali_numerals(match[0]) for match in matches]

    return ayat_texts, ayat_numbers

# Streamlit UI
st.title("Ayat Extractor")

# Initialize page number and other parameters
if "page_number" not in st.session_state:
    st.session_state.page_number = 141
if "surah" not in st.session_state:
    st.session_state.surah = "Baqarah"
if "para" not in st.session_state:
    st.session_state.para = 10

st.write(f"Current Page Number: {st.session_state.page_number}")

# Input for text
text = st.text_area("Enter Text:", height=200)

# Button to extract ayat
if st.button("Extract Ayat"):
    ayat_texts, ayat_numbers = extract_and_split_text(text)

    output_text = ""
    for ayat_text, ayat_number in zip(ayat_texts, ayat_numbers):
        line = f"('{ayat_text}', '{st.session_state.surah}', '{ayat_number}', '{st.session_state.para}', '{st.session_state.page_number}'),"
        output_text += line + "\n"

    # Display the output
    st.text_area("Extracted Ayat", output_text, height=200)

    # Increment page number
    st.session_state.page_number += 1
    st.write(f"Next Page Number: {st.session_state.page_number}")
