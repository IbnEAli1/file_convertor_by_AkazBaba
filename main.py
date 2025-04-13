import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="📂File Converter & Cleaner By AkazBaba", page_icon="📂", layout="wide")
st.title("📂 File Converter & Cleaner by AkazBaba")
st.markdown("""
    <div style="background-color:#f9f9f9;border-left:5px solid #ff4b4b;padding:15px 25px;margin:20px 0;border-radius:8px;">
        <h2 style="color:#ff4b4b;">🚀 Upload and Convert with Style!</h2>
        <p style="color:#444;">
            This tool helps you clean missing values, select columns, and download data in CSV, Excel, or PDF formats with ease.<br>
            Brought to you by <a href="https://www.youtube.com/@AkazBaba" target="_blank" style="color:#ff4b4b;text-decoration:none;"><b>AkazBaba</b></a>.
        </p>
    </div>
""", unsafe_allow_html=True)
st.write("Upload your CSV and Excel Files to clean the data convert formats effortlessly🚀🚀")

# ✅ PDF main convert karne ka function
def dataframe_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_width = pdf.w / (len(df.columns) + 1)

    # Header
    for col in df.columns:
        pdf.cell(col_width, 10, str(col), border=1)
    pdf.ln()

    # Rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(item), border=1)
        pdf.ln()

    pdf_bytes = pdf.output(dest='S').encode('latin1')  # ✅ Fixed here
    return BytesIO(pdf_bytes)

files = st.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for idx, file in enumerate(files):
        ext = file.name.split(".")[-1].lower()

        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader(f"🔎 {file.name} Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing Values filled successfully!")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=list(df.columns))
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel", "PDF"], key=f"format_{idx}")

        if st.button(f"⬇️ Download {file.name} as {format_choice}", key=f"btn_{idx}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            elif format_choice == "Excel":
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"
            else:  # PDF
                output = dataframe_to_pdf(df)
                mime = "application/pdf"
                new_name = file.name.rsplit(".", 1)[0] + ".pdf"

            output.seek(0)
            st.download_button(
                "⬇️ Download File ⬇️",
                file_name=new_name,
                data=output,
                mime=mime,
                key=f"download_{idx}"
            )

        st.success("Processing Completed 👍👍👍✌️✌️✌️🥳🥳🥳🥳")
