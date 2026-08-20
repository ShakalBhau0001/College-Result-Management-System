import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def load_data(path):
    return st.session_state.stored_data.get(path, [])


def subject_analysis(detailed_data):
    st.header("📚 Subject-wise Analysis")
    if not detailed_data:
        st.warning("No detailed data available. Please process a PDF first.")
        return

    subject_stats = {}
    for student in detailed_data:
        for i in range(len(student["Code"])):
            code = student["Code"][i]
            total = student["Total"][i]

            if not isinstance(code, str) or not isinstance(total, str):
                continue

            # Initialize subject entry
            if code not in subject_stats:
                subject_stats[code] = {
                    "total_marks": 0,
                    "count": 0,
                    "pass_count": 0,
                    "fail_count": 0,
                }

            try:
                if total.isdigit():
                    mark = int(total)
                    subject_stats[code]["total_marks"] += mark
                    subject_stats[code]["count"] += 1
                    status = student["Status1"][i]
                    if status == "P":
                        subject_stats[code]["pass_count"] += 1
                    else:
                        subject_stats[code]["fail_count"] += 1
            except:
                continue

    analysis_data = []
    for code, stats in subject_stats.items():
        if stats["count"] > 0:
            avg_mark = stats["total_marks"] / stats["count"]
            pass_rate = (stats["pass_count"] / stats["count"]) * 100
            analysis_data.append(
                {
                    "Subject": code,
                    "Avg. Marks": f"{avg_mark:.2f}",
                    "Pass Rate": f"{pass_rate:.2f}%",
                    "Students": stats["count"],
                    "Passed": stats["pass_count"],
                    "Failed": stats["fail_count"],
                }
            )

    if not analysis_data:
        st.warning("No valid subject data found")
        return

    df = pd.DataFrame(analysis_data)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Subject Performance")
        st.dataframe(df)
    with col2:
        st.subheader("Subject Analysis")
        tab1, tab2 = st.tabs(["Average Marks", "Pass Rate"])
        with tab1:
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.bar(
                df["Subject"], df["Avg. Marks"].astype(float), color="skyblue"
            )
            ax.set_ylabel("Average Marks")
            ax.set_title("Average Marks per Subject")
            ax.set_xticklabels(df["Subject"], rotation=45, ha="right")
            ax.bar_label(bars, fmt="%.2f", padding=3)
            st.pyplot(fig)
        with tab2:
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.bar(
                df["Subject"],
                df["Pass Rate"].str.replace("%", "").astype(float),
                color="lightgreen",
            )
            ax.set_ylabel("Pass Rate (%)")
            ax.set_title("Pass Rate per Subject")
            ax.set_ylim(0, 100)
            ax.set_xticklabels(df["Subject"], rotation=45, ha="right")
            ax.bar_label(bars, fmt="%.1f%%", padding=3)
            st.pyplot(fig)


def show():
    detailed_data = load_data("Result_dict")
    subject_analysis(detailed_data)
