import re
from io import BytesIO

import pandas as pd
import pdfplumber
import streamlit as st


def extract_student_data_from_bytes(pdf_bytes):
    student_info_all_with_marks = []
    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages[4:]:
                text = page.extract_text()
                if not text:
                    continue

                all_student_data = []
                student_info = {}
                if "College Code: SANG" in text:
                    lines = text.split("\n")
                    for line in lines:
                        if re.match(r"^\d+\.\s+[A-Z\s]+$", line.strip()):
                            student_info["Name"] = line.split(".", 1)[1].strip()

                        if (
                            "Seat No:" in line
                            and "PRN No." in line
                            and "College Code:" in line
                        ):
                            seat_no_match = re.search(r"Seat No:\s*(\d+)", line)
                            if seat_no_match:
                                student_info["Seat No"] = seat_no_match.group(1)

                        if "PRN No." in line:
                            student_info["PRN No"] = (
                                line.split("PRN No.")[-1].split()[0].strip()
                            )

                        if "Status:" in line:
                            student_info["Status"] = (
                                line.split("Status:")[-1].split()[0].strip()
                            )

                        if "Percentage:" in line:
                            percentage_part = (
                                line.split("Percentage:")[-1].split("%")[0].strip()
                            )
                            student_info["Percentage"] = f"{percentage_part}"

                    for line in lines:
                        if any(
                            code in line
                            for code in ["BCA", "ECS", "CC-", "ENG-", "ENS", "SEC"]
                        ):
                            words = line.split()
                            parts = []
                            i = 0

                            while i < len(words):
                                if (
                                    words[i] == "*"
                                    and i + 1 < len(words)
                                    and words[i + 1].isdigit()
                                ):
                                    parts.append(f"* {words[i + 1]}")
                                    i += 2
                                elif (
                                    words[i] == "$"
                                    and i + 3 < len(words)
                                    and words[i + 1].isdigit()
                                    and words[i + 2].startswith("+")
                                    and words[i + 2][1:].isdigit()
                                ):
                                    sum_val = int(words[i + 1]) + int(words[i + 2][1:])
                                    parts.append(str(sum_val))
                                    i += 3
                                elif (
                                    words[i].isdigit()
                                    and i + 2 < len(words)
                                    and words[i + 1] == "+"
                                    and words[i + 2].isdigit()
                                ):
                                    sum_val = int(words[i]) + int(words[i + 2])
                                    parts.append(str(sum_val))
                                    i += 3
                                elif (
                                    words[i].startswith("+") and words[i][1:].isdigit()
                                ):
                                    parts.append(words[i][1:])
                                    i += 1
                                elif words[i] in ["$", "+"]:
                                    i += 1
                                else:
                                    parts.append(words[i])
                                    i += 1

                            try:
                                data = {
                                    "Code": parts[0] if len(parts) > 0 else "",
                                    "UA": parts[3] if len(parts) > 3 else "",
                                    "CA": parts[5] if len(parts) > 5 else "",
                                    "Total": parts[8] if len(parts) > 8 else "",
                                    "Status": parts[-2] if len(parts) > 12 else "",
                                }
                                all_student_data.append(data)
                            except IndexError:
                                continue

                    all_Data = pd.DataFrame(all_student_data)
                    combined_dict = {
                        "Code": all_Data["Code"].tolist(),
                        "UA": all_Data["UA"].tolist(),
                        "CA": all_Data["CA"].tolist(),
                        "Total": all_Data["Total"].tolist(),
                        "Status1": all_Data["Status"].tolist(),
                    }
                    student_info.update(combined_dict)
                    student_info_all_with_marks.append(student_info)

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

    return student_info_all_with_marks


def save_data(path, info):
    st.session_state.stored_data[path] = info


def load_data(path):
    return st.session_state.stored_data.get(path, [])


def store_data(uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a PDF file first.")
        return

    with st.spinner("Processing PDF..."):
        pdf_bytes = uploaded_file.getvalue()
        student_info = extract_student_data_from_bytes(pdf_bytes)

        if not student_info:
            st.error("No student data found in the PDF.")
            return

        data = []
        for record in student_info:
            data.append(
                {
                    "Seat No": record["Seat No"],
                    "Name": record["Name"],
                    "Percentage": record["Percentage"],
                    "Status": record["Status"],
                }
            )

        save_data("Result_dict", student_info)
        save_data("Shoert_data", data)
        st.success("✅ All data saved successfully!")
        st.subheader("Sample Data")
        st.dataframe(pd.DataFrame(data).head())


def show():
    st.header("📤 Upload Result PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if st.button("Process PDF"):
        store_data(uploaded_file)
