import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Event Comparison",
    page_icon="📈",
    layout="wide"
)


# ==========================
# HEADER
# ==========================

st.title("📈 Event Performance Comparison")

st.markdown(
"""
Bandingkan performa seluruh event berdasarkan revenue,
profit, dan profit margin.
"""
)


# ==========================
# DATA EVENT
# ==========================

event_files = {

    "Dentra TNF Semarang":
    "data/events/semarang_dentra_tnf/sales.csv",

    "Midnight In Cell Semarang":
    "data/events/semarang_midnight_cell/sales.csv",

    "White Party STALK Jakarta":
    "data/events/jakarta_stalk_white_party/sales.csv"

}


results = []


for event, file in event_files.items():

    try:

        df = pd.read_csv(file)


        revenue = df["Revenue"].sum()

        profit = df["Profit"].sum()

        margin = (
            profit / revenue * 100
            if revenue > 0 else 0
        )


        best_product = (
            df.groupby("Menu")["Profit"]
            .sum()
            .idxmax()
        )


        results.append({

            "Event": event,
            "Revenue": revenue,
            "Profit": profit,
            "Margin (%)": margin,
            "Best Product": best_product

        })


    except Exception as e:

        st.warning(
            f"{event} gagal dibaca: {e}"
        )



comparison = pd.DataFrame(results)



# ==========================
# TABLE
# ==========================

st.subheader("📊 Executive Comparison")


display_df = comparison.copy()


display_df["Revenue"] = display_df["Revenue"].apply(
    lambda x: f"Rp {x:,.0f}"
)


display_df["Profit"] = display_df["Profit"].apply(
    lambda x: f"Rp {x:,.0f}"
)


display_df["Margin (%)"] = display_df["Margin (%)"].apply(
    lambda x: f"{x:.2f}%"
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)



# ==========================
# CHART REVENUE
# ==========================

st.subheader("💰 Revenue Comparison")


fig_revenue = px.bar(
    comparison,
    x="Event",
    y="Revenue",
    text_auto=".2s",
    title="Revenue per Event"
)


fig_revenue.update_layout(
    height=450
)


st.plotly_chart(
    fig_revenue,
    use_container_width=True
)



# ==========================
# CHART PROFIT
# ==========================

st.subheader("🔥 Profit Comparison")


fig_profit = px.bar(
    comparison,
    x="Event",
    y="Profit",
    text_auto=".2s",
    title="Profit per Event"
)


st.plotly_chart(
    fig_profit,
    use_container_width=True
)



# ==========================
# WINNER INSIGHT
# ==========================

st.subheader("🤖 Business Insight")


best_event = (
    comparison
    .sort_values(
        "Profit",
        ascending=False
    )
    .iloc[0]
)



st.success(
f"""
🏆 Event paling profitable:

**{best_event['Event']}**

Total Profit:

**Rp {best_event['Profit']:,.0f}**

Produk terbaik:

**{best_event['Best Product']}**

Rekomendasi:
Pertahankan produk dengan margin tinggi dan jadikan
event terbaik sebagai benchmark strategi event berikutnya.
"""
)