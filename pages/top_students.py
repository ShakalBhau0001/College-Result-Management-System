import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def load_data(path):
    return st.session_state.stored_data.get(path, [])


def find_top_ten(data):
    if not data:
        st.warning("No data available. Please upload and process a PDF first.")
        return

    top_students = [d for d in data if float(d["Percentage"]) > 89.00]
    top_students.sort(key=lambda x: float(x["Percentage"]), reverse=True)
    st.subheader("🏆 Top 10 Students")
    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(data))
    col2.metric("Students with >89%", len(top_students))
    if top_students:
        df = pd.DataFrame(top_students[:10])
        tab1, tab2 = st.tabs(["Data", "Visualization"])
        with tab1:
            st.dataframe(df)
        with tab2:
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, texts, autotexts = ax.pie(
                df["Percentage"].astype(float),
                labels=df["Name"].str[:15] + "...",
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"linewidth": 1, "edgecolor": "white"},
                textprops={"fontsize": 9},
                colors=plt.colormaps["Pastel1"].colors,
            )
            plt.setp(autotexts, size=8, weight="bold")
            ax.set_title("Top 10 Students Percentage Distribution", pad=20)
            st.pyplot(fig)
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            bars = ax2.barh(
                df["Name"].str[:20] + "...",
                df["Percentage"].astype(float),
                color=plt.cm.viridis(np.linspace(0, 1, len(df))),
            )
            ax2.set_xlabel("Percentage (%)")
            ax2.set_title("Top 10 Students Performance")
            ax2.bar_label(bars, fmt="%.2f%%", padding=3)
            ax2.set_xlim(0, 100)
            st.pyplot(fig2)
    else:
        st.info("No students found with percentage > 89%")


def show():
    data = load_data("Shoert_data")
    find_top_ten(data)
