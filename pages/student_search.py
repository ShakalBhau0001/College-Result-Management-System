import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def load_data(path):
    """Load data from session state"""
    return st.session_state.stored_data.get(path, [])


def student_search(data, detailed_data):
    st.header("🔍 Student Search")

    if not data:
        st.warning("No data available. Please upload and process a PDF first.")
        return

    search_term = (
        st.text_input("Search by Seat No or Name", key="search_input").strip().lower()
    )

    if not search_term:
        st.info("Enter a seat number or name to search")
        return

    results = []
    for student in data:
        if (
            search_term in student["Seat No"].lower()
            or search_term in student["Name"].lower()
        ):
            results.append(student)

    if not results:
        st.warning("No matching students found")
        return

    st.success(f"Found {len(results)} matching student(s)")
    df = pd.DataFrame(results)
    st.dataframe(df[["Seat No", "Name", "Percentage", "Status"]])
    options = [f"{res['Seat No']} - {res['Name']}" for res in results]
    if len(results) > 1:
        # Create a select box for multiple results
        selected_option = st.selectbox(
            "Select a student to view detailed marks:", options, key="student_select"
        )
        selected_seat_no = selected_option.split(" - ")[0]
    else:
        selected_seat_no = results[0]["Seat No"]

    # Display detailed marks for the selected student
    st.subheader("📝 Detailed Marks")
    for detailed in detailed_data:
        if detailed["Seat No"] == selected_seat_no:
            # Create marks table
            marks_data = []
            for i in range(len(detailed["Code"])):
                marks_data.append(
                    {
                        "Subject": detailed["Code"][i],
                        "UA": detailed["UA"][i],
                        "CA": detailed["CA"][i],
                        "Total": detailed["Total"][i],
                        "Status": detailed["Status1"][i],
                    }
                )

            marks_df = pd.DataFrame(marks_data)
            st.dataframe(marks_df)
            col1, col2 = st.columns(2)

            with col1:
                # Create subject performance chart
                fig, ax = plt.subplots(figsize=(8, 4))
                bars = ax.bar(
                    marks_df["Subject"],
                    marks_df["Total"].apply(lambda x: int(x) if x.isdigit() else 0),
                    color="skyblue",
                )
                ax.set_ylabel("Marks")
                ax.set_title("Subject-wise Marks")
                ax.set_xticklabels(marks_df["Subject"], rotation=45, ha="right")
                ax.set_ylim(0, 100)
                ax.bar_label(bars, fmt="%d", padding=3)
                st.pyplot(fig)

            with col2:
                # Calculate summary stats
                total_marks = sum(
                    [int(x) if x.isdigit() else 0 for x in detailed["Total"]]
                )
                passed_subjects = sum(
                    1 for status in detailed["Status1"] if status == "P"
                )

                st.metric("Total Marks", total_marks)
                st.metric(
                    f"Passed Subjects", f"{passed_subjects}/{len(detailed['Status1'])}"
                )
                st.metric("Overall Percentage", detailed["Percentage"] + "%")
            break


def show():
    data = load_data("Shoert_data")
    detailed_data = load_data("Result_dict")
    student_search(data, detailed_data)
