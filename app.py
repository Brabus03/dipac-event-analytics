import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.analytics import (
    calculate_kpi,
    menu_analysis,
    top_menu
)
from utils.forecasting import (
    create_forecast
)

from utils.pdf_report import create_pdf


# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="DIPAC Event Intelligence",
    page_icon="📊",
    layout="wide"
)


# =====================================
# STYLE
# =====================================

st.markdown(
"""
<style>

[data-testid="stMetric"]{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0 5px 15px rgba(0,0,0,0.08);
}

[data-testid="stMetricValue"]{

    font-size:22px !important;

    white-space:nowrap !important;

    overflow:visible !important;

}


[data-testid="stMetric"]{

    min-width:220px !important;

}

</style>
""",
unsafe_allow_html=True
)



# =====================================
# EVENT DATA
# =====================================

EVENTS = {

    "Dentra TNF Semarang":
    "data/events/semarang_dentra_tnf/sales.csv",

    "Midnight In Cell Semarang":
    "data/events/semarang_midnight_cell/sales.csv"

}



# =====================================
# FUNCTIONS
# =====================================

def rupiah(value):

    try:

        return (
            "Rp {:,.0f}"
            .format(float(value))
            .replace(",", ".")
        )

    except:

        return "Rp 0"



def load_data(path):

    if not os.path.exists(path):

        return None


    try:

        df = pd.read_csv(path)

        if df.empty:

            return None

        return df


    except:

        return None



def prepare_data(df):

    df.columns = df.columns.str.strip()


    if "Profit" not in df.columns:

        df["Profit"] = df["Collective Share"]


    return df



def commission_rate(
    collective,
    customer
):

    if customer == 0:

        return 0

    return (
        collective/customer*100
    )



# =====================================
# HEADER
# =====================================

st.title(
"📊 DIPAC Event Intelligence Dashboard"
)


st.write(
"""
Business intelligence dashboard untuk menganalisis
customer spending, collective income, dan performa event.
"""
)



# =====================================
# MENU
# =====================================

menu = st.sidebar.selectbox(

    "Navigation",

    [
        "Event Dashboard",
        "Event Comparison",
        "Menu Performance",
        "Executive Report"
    ]

)



# =====================================
# EVENT DASHBOARD
# =====================================

if menu == "Event Dashboard":


    event = st.selectbox(

        "🎟️ Pilih Event",

        list(EVENTS.keys())

    )


    df = load_data(
        EVENTS[event]
    )


    if df is None:

        st.warning(
            "Data event belum tersedia"
        )

        st.stop()



    df = prepare_data(df)



    st.header(
        f"📍 {event}"
    )



    # ==========================
    # KPI
    # ==========================

    customer = df["Customer Revenue"].sum()

    collective = df["Collective Share"].sum()

    profit = df["Profit"].sum()


    commission = commission_rate(
        collective,
        customer
    )


    if "Qty" in df.columns:

        total_bottle = df["Qty"].sum()

    else:

        total_bottle = 0



    avg_spending = (

        customer / total_bottle

        if total_bottle > 0

        else 0

    )



    col1,col2,col3 = st.columns(3)


    col4,col5,col6 = st.columns(3)



    col1.metric(
        "Customer Spending",
        rupiah(customer)
    )


    col2.metric(
        "Collective Income",
        rupiah(collective)
    )


    col3.metric(
        "Bottle Sold",
        f"{int(total_bottle)} Bottle"
    )


    col4.metric(
        "Average Spending",
        rupiah(avg_spending)
    )


    col5.metric(
        "Profit Contribution",
        rupiah(profit)
    )


    col6.metric(
        "Commission Rate",
        f"{commission:.2f}%"
    )



    # ==========================
    # TABLE
    # ==========================

    st.subheader(
        "📋 Transaction Detail"
    )


    table = df.copy()


    for col in [

        "Customer Price",
        "Customer Revenue",
        "Collective Share",
        "Profit"

    ]:

        if col in table.columns:

            table[col] = table[col].apply(rupiah)



    st.dataframe(

        table,

        hide_index=True,

        use_container_width=True

    )



    # ==========================
    # CUSTOMER CHART
    # ==========================

    st.subheader(
        "💰 Customer Spending by Menu"
    )


    customer_chart = (

        df.groupby("Menu")
        ["Customer Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "Customer Revenue",
            ascending=False
        )

    )


    fig1 = px.bar(

        customer_chart,

        x="Menu",

        y="Customer Revenue",

        text="Customer Revenue",

        template="plotly_white"

    )


    fig1.update_traces(

        texttemplate="Rp %{y:,.0f}",

        textposition="outside"

    )


    st.plotly_chart(

        fig1,

        use_container_width=True

    )



    # ==========================
    # COLLECTIVE CHART
    # ==========================

    st.subheader(
        "🤝 Collective Contribution by Menu"
    )


    collective_chart = (

        df.groupby("Menu")
        ["Collective Share"]
        .sum()
        .reset_index()
        .sort_values(
            "Collective Share",
            ascending=False
        )

    )


    fig2 = px.bar(

        collective_chart,

        x="Menu",

        y="Collective Share",

        text="Collective Share",

        template="plotly_white"

    )


    fig2.update_traces(

        texttemplate="Rp %{y:,.0f}",

        textposition="outside"

    )


    st.plotly_chart(

        fig2,

        use_container_width=True

    )

        # ==========================
    # AI INSIGHT
    # ==========================

    st.subheader(
        "🤖 AI Business Insight"
    )


    best_collective = (

        df.groupby("Menu")
        ["Collective Share"]
        .sum()
        .idxmax()

    )


    best_customer = (

        df.groupby("Menu")
        ["Customer Revenue"]
        .sum()
        .idxmax()

    )


    st.success(

f"""
🏆 Menu dengan collective income terbesar:

**{best_collective}**


💰 Menu dengan customer spending terbesar:

**{best_customer}**


Strategi:

- Pertahankan menu dengan collective share tinggi.
- Jadikan menu revenue tinggi sebagai produk utama promosi.
- Gunakan data ini sebagai referensi event berikutnya.

"""

    )




# =====================================
# EVENT COMPARISON
# =====================================


elif menu == "Event Comparison":


    st.header(
        "📈 Event Comparison"
    )


    comparison_data = []


    for event, path in EVENTS.items():


        df = load_data(path)


        if df is None:

            continue



        df = prepare_data(df)



        customer = (
            df["Customer Revenue"]
            .sum()
        )


        collective = (
            df["Collective Share"]
            .sum()
        )


        profit = (
            df["Profit"]
            .sum()
        )


        commission = commission_rate(

            collective,

            customer

        )


        comparison_data.append({

            "Event": event,

            "Customer Spending": customer,

            "Collective Income": collective,

            "Profit": profit,

            "Commission": commission

        })



    comparison = pd.DataFrame(
        comparison_data
    )


    if comparison.empty:


        st.warning(
            "Belum ada data event"
        )

        st.stop()



    # ==========================
    # EXECUTIVE KPI
    # ==========================


    total_customer = (

        comparison["Customer Spending"]
        .sum()

    )


    total_collective = (

        comparison["Collective Income"]
        .sum()

    )


    avg_commission = (

        comparison["Commission"]
        .mean()

    )


    best_event = (

        comparison
        .sort_values(
            "Collective Income",
            ascending=False
        )
        .iloc[0]

    )



    st.subheader(
        "📊 Overall Event Performance"
    )



    k1,k2,k3,k4 = st.columns(4)



    k1.metric(

        "Total Customer Spending",

        rupiah(total_customer)

    )


    k2.metric(

        "Total Collective Income",

        rupiah(total_collective)

    )


    k3.metric(

        "Average Commission",

        f"{avg_commission:.2f}%"

    )


    k4.metric(

        "Best Event",

        best_event["Event"]

    )



    # ==========================
    # TABLE
    # ==========================


    st.subheader(
        "📋 Event Performance Summary"
    )


    display = comparison.copy()


    for col in [

        "Customer Spending",

        "Collective Income",

        "Profit"

    ]:


        display[col] = (

            display[col]
            .apply(rupiah)

        )



    display["Commission"] = (

        display["Commission"]
        .apply(
            lambda x:f"{x:.2f}%"
        )

    )


    st.dataframe(

        display,

        hide_index=True,

        use_container_width=True

    )



    # ==========================
    # COLLECTIVE COMPARISON
    # ==========================


    st.subheader(
        "🤝 Collective Income Comparison"
    )


    fig3 = px.bar(

        comparison,

        x="Event",

        y="Collective Income",

        text="Collective Income",

        template="plotly_white"

    )


    fig3.update_traces(

        texttemplate="Rp %{y:,.0f}",

        textposition="outside"

    )


    fig3.update_layout(

        height=500

    )


    st.plotly_chart(

        fig3,

        use_container_width=True

    )



    # ==========================
    # CUSTOMER COMPARISON
    # ==========================


    st.subheader(
        "💰 Customer Spending Comparison"
    )


    fig4 = px.bar(

        comparison,

        x="Event",

        y="Customer Spending",

        text="Customer Spending",

        template="plotly_white"

    )


    fig4.update_traces(

        texttemplate="Rp %{y:,.0f}",

        textposition="outside"

    )


    fig4.update_layout(

        height=500

    )


    st.plotly_chart(

        fig4,

        use_container_width=True

    )


# =====================================
# MENU PERFORMANCE ANALYSIS
# =====================================

# =====================================
# MENU PERFORMANCE ANALYSIS
# =====================================

elif menu == "Menu Performance":


    st.header(
        "📦 Menu Performance Analysis"
    )


    st.write(
        """
        Analisis performa menu berdasarkan jumlah penjualan,
        customer spending, dan kontribusi collective.
        """
    )
    menu_data = []


    for event, path in EVENTS.items():

        df = load_data(path)

        if df is None:
            continue


        df = prepare_data(df)

        df["Event"] = event

        menu_data.append(df)



    if not menu_data:

        st.warning(
            "Data menu belum tersedia"
        )

        st.stop()



    menu_df = pd.concat(
        menu_data,
        ignore_index=True
    )



    menu_summary = (

        menu_df
        .groupby("Menu")
        .agg({

            "Qty":"sum",

            "Customer Revenue":"sum",

            "Collective Share":"sum"

        })

        .reset_index()

        .sort_values(
            "Collective Share",
            ascending=False
        )

    )


    st.subheader(
        "🏆 Menu Ranking"
    )


    display = menu_summary.copy()


    display["Customer Revenue"] = (
        display["Customer Revenue"]
        .apply(rupiah)
    )


    display["Collective Share"] = (
        display["Collective Share"]
        .apply(rupiah)
    )


    st.dataframe(

        display.head(10),

        hide_index=True,

        use_container_width=True

    )



    st.subheader(
        "🤝 Top Menu by Collective Income"
    )


    fig1 = px.bar(

        menu_summary.head(10),

        x="Menu",

        y="Collective Share",

        text="Collective Share",

        template="plotly_white"

    )


    fig1.update_traces(

        texttemplate="Rp %{y:,.0f}",

        textposition="outside"

    )


    fig1.update_layout(
        height=600,
        xaxis_tickangle=-45
    )


    st.plotly_chart(

        fig1,

        use_container_width=True

    )



    st.subheader(
        "🍾 Most Sold Menu"
    )


    qty_rank = (

        menu_summary
        .sort_values(
            "Qty",
            ascending=False
        )
        .head(10)

    )


    fig2 = px.bar(

        qty_rank,

        x="Menu",

        y="Qty",

        text="Qty",

        template="plotly_white"

    )


    fig2.update_layout(
        height=600,
        xaxis_tickangle=-45
    )


    st.plotly_chart(

        fig2,

        use_container_width=True

    )



    best_menu = (
        menu_summary.iloc[0]["Menu"]
    )


    best_qty = (
        qty_rank.iloc[0]["Menu"]
    )


    st.success(

f"""
🤖 Business Insight


🏆 Collective income terbesar:

**{best_menu}**


🍾 Volume penjualan tertinggi:

**{best_qty}**


Strategi:

- Jadikan menu dengan collective share tinggi sebagai prioritas.
- Gunakan menu dengan volume tinggi untuk menarik customer baru.
- Kombinasikan produk premium dan produk cepat terjual.
"""

    )


    menu_data = []


    for event, path in EVENTS.items():

        df_menu = load_data(path)


        if df_menu is None:

            continue


        df_menu = prepare_data(df_menu)

        df_menu["Event"] = event


        menu_data.append(df_menu)



    if len(menu_data) == 0:

        st.warning(
            "Data menu belum tersedia"
        )

        st.stop()



    menu_df = pd.concat(
        menu_data,
        ignore_index=True
    )

# =====================================
# EXECUTIVE REPORT
# =====================================

elif menu == "Executive Report":

    st.header(
        "📄 Executive Event Report"
    )


    event = st.selectbox(
        "Pilih Event",
        list(EVENTS.keys())
    )


    df = load_data(
        EVENTS[event]
    )


    if df is None:

        st.warning(
            "Data event belum tersedia"
        )

        st.stop()


    df = prepare_data(df)

kpi = calculate_kpi(df)

best = top_menu(df)

customer = kpi["customer"]
collective = kpi["collective"]
profit = kpi["profit"]
commission = kpi["commission"]
best_menu = best

    # lanjut isi report

st.subheader(
    f"📊 Performance Summary - {event}"
)


st.info(
f"""
## {event}

💰 Customer Spending:

{rupiah(customer)}


🤝 Collective Income:

{rupiah(collective)}


📈 Profit Contribution:

{rupiah(profit)}


📊 Commission Rate:

{commission:.2f}%


🏆 Best Performing Menu:

{best_menu}


Rekomendasi:

- Pertahankan menu dengan kontribusi collective terbesar.
- Gunakan produk terbaik sebagai benchmark event berikutnya.
- Evaluasi strategi penjualan berdasarkan customer spending.

"""
)


# ==========================
# AI BUSINESS INSIGHT
# ==========================

st.subheader(
    "🤖 AI Business Insight"
)


collective_ratio = (
    collective / customer * 100
    if customer > 0
    else 0
)


if collective_ratio >= 30:

    insight = f"""
🚀 Event {event} menunjukkan performa collective yang kuat.

Collective contribution mencapai {collective_ratio:.2f}% 
dari total customer spending.

Strategi bundling dan menu dengan collective share tinggi
dapat dipertahankan untuk event berikutnya.
"""


elif collective_ratio >= 15:

    insight = f"""
📊 Event {event} memiliki performa collective yang cukup baik.

Kontribusi collective berada pada level {collective_ratio:.2f}% 
terhadap total transaksi.

Optimasi dapat dilakukan melalui peningkatan bundling,
promosi menu unggulan, dan strategi upselling.
"""

else:

    insight = f"""
⚠️ Event {event} memiliki kontribusi collective yang rendah.

Collective contribution hanya {collective_ratio:.2f}% 
dari total customer spending.

Perlu evaluasi pricing, paket penjualan, dan product placement.
"""


st.success(
    insight
)

st.subheader(
    "📋 Transaction Summary"
)
st.subheader(
    "🏆 Menu Performance Ranking"
)


menu_rank = (
    df.groupby("Menu")
    ["Collective Share"]
    .sum()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


menu_rank["Collective Share"] = (
    menu_rank["Collective Share"]
    .apply(rupiah)
)


st.dataframe(
    menu_rank,
    hide_index=True,
    use_container_width=True
)

report_table = df.copy()


for col in [
        "Customer Price",
        "Customer Revenue",
        "Collective Share",
        "Profit"
    ]:

        if col in report_table.columns:

            report_table[col] = (
                report_table[col]
                .apply(rupiah)
            )


st.dataframe(
        report_table,
        hide_index=True,
        use_container_width=True
    )
st.divider()

if st.button("📄 Generate PDF Report"):

    file = create_pdf(
        event,
        kpi["customer"],
        kpi["collective"],
        kpi["profit"],
        kpi["commission"],
        best
    )

    st.success(
        f"PDF berhasil dibuat: {file}"
    )
