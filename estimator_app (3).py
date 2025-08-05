
import streamlit as st

st.title("AI Job Estimator")

# Materials
st.header("Material Quantities")
q_2x4 = st.number_input("2x4s", 0)
q_drywall = st.number_input("Drywall Sheets", 0)
q_nails = st.number_input("Nails (lbs)", 0)
q_paint = st.number_input("Paint (gallons)", 0)
q_concrete = st.number_input("Concrete Bags", 0)

# Labor
st.header("Labor")
labor_hours = st.number_input("Total Labor Hours", 0.0)
labor_rate = st.number_input("Labor Rate per Hour ($)", 0.0)

# Overhead & Profit
st.header("Other Costs")
overhead_pct = st.number_input("Overhead %", 0.0)
profit_pct = st.number_input("Profit Margin %", 0.0)

# Prices
price_2x4 = 3.75
price_drywall = 15.50
price_nails = 2.75
price_paint = 35.00
price_concrete = 7.25

# Calculate
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
