import pandas as pd


def prepare_data(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
    )


    if "Profit" not in df.columns:

        df["Profit"] = (
            df["Collective Share"]
        )


    return df



def calculate_kpi(df):

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


    qty = 0


    if "Qty" in df.columns:

        qty = (
            df["Qty"]
            .sum()
        )


    average_spending = (

        customer / qty

        if qty > 0

        else 0

    )


    commission = (

        collective /
        customer *
        100

        if customer > 0

        else 0

    )


    return {

        "customer": customer,

        "collective": collective,

        "profit": profit,

        "qty": qty,

        "average": average_spending,

        "commission": commission

    }




def menu_analysis(df):

    df = prepare_data(df)


    summary = (

        df
        .groupby("Menu")
        .agg({

            "Qty":"sum",

            "Customer Revenue":"sum",

            "Collective Share":"sum"

        })

        .reset_index()

    )


    summary = (

        summary
        .sort_values(

            "Collective Share",

            ascending=False

        )

    )


    return summary




def top_menu(df):

    summary = menu_analysis(df)


    if len(summary) == 0:

        return None


    return summary.iloc[0]["Menu"]