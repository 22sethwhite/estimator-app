import streamlit as st
from fpdf import FPDF
import tempfile

st.title("AI Job Estimator")

# Sidebar for editable material prices
st.sidebar.header("Material Prices (Editable)")
price_2x4 = st.sidebar.number_input("2x4 ($)", value=3.75)
price_drywall = st.sidebar.number_input("Drywall Sheet ($)", value=15.50)
price_nails = st.sidebar.number_input("Nails per lb ($)", value=2.75)
price_paint = st.sidebar.number_input("Paint per gallon ($)", value=35.00)
price_concrete = st.sidebar.number_input("Concrete Bag ($)", value=7.25)

# Smart estimate assistant
st.header("Smart Estimate Assistant")
job_description = st.text_area("Describe the job (e.g., 'Install 500 sq ft drywall, 2 workers')")
if st.button("Generate Estimate from Description"):
    # Simple heuristic to simulate GPT-generated values
    if "drywall" in job_description.lower():
        q_drywall = 25
    else:
        q_drywall = 0
    if "paint" in job_description.lower():
        q_paint = 3
    else:
        q_paint = 0
    if "2x4" in job_description.lower() or "frame" in job_description.lower():
        q_2x4 = 40
    else:
        q_2x4 = 0
    q_nails = 5
    q_concrete = 0
    labor_hours = 16
    st.session_state.update({
        'q_drywall': q_drywall,
        'q_paint': q_paint,
        'q_2x4': q_2x4,
        'q_nails': q_nails,
        'q_concrete': q_concrete,
        'labor_hours': labor_hours
    })

# Materials
st.header("Material Quantities")
q_2x4 = st.number_input("2x4s", value=st.session_state.get('q_2x4', 0))
q_drywall = st.number_input("Drywall Sheets", value=st.session_state.get('q_drywall', 0))
q_nails = st.number_input("Nails (lbs)", value=st.session_state.get('q_nails', 0))
q_paint = st.number_input("Paint (gallons)", value=st.session_state.get('q_paint', 0))
q_concrete = st.number_input("Concrete Bags", value=st.session_state.get('q_concrete', 0))

# Labor
st.header("Labor")
labor_hours = st.number_input("Total Labor Hours", value=st.session_state.get('labor_hours', 0.0))
labor_rate = st.number_input("Labor Rate per Hour ($)", value=50.0)

# Overhead & Profit
st.header("Other Costs")
overhead_pct = st.number_input("Overhead %", value=10.0)
profit_pct = st.number_input("Profit Margin %", value=20.0)

# Estimate calculation
if st.button("Estimate Job"):
    material_cost = (
        q_2x4 * price_2x4 +
        q_drywall * price_drywall +
        q_nails * price_nails +
        q_paint * price_paint +
        q_concrete * price_concrete
    )
    labor_cost = labor_hours * labor_rate
    overhead = (material_cost + labor_cost) * (overhead_pct / 100)
    profit = (material_cost + labor_cost + overhead) * (profit_pct / 100)
    total = material_cost + labor_cost + overhead + profit

    st.subheader("Estimate Summary")
    st.write(f"Materials: ${material_cost:.2f}")
    st.write(f"Labor: ${labor_cost:.2f}")
    st.write(f"Overhead: ${overhead:.2f}")
    st.write(f"Profit: ${profit:.2f}")
    st.markdown(f"### Total Estimate: **${total:.2f}**")

    # Export to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Estimate Summary", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Materials Cost: ${material_cost:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Labor Cost: ${labor_cost:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Overhead: ${overhead:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Profit: ${profit:.2f}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Estimate: ${total:.2f}", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as file:
            btn = st.download_button(
                label="Download Estimate as PDF",
                data=file,
                file_name="estimate_summary.pdf",
                mime="application/pdf"
            )
