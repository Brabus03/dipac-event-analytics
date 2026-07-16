def create_forecast(history):

    result = {}


    total_customer = (
        history["Customer Revenue"]
        .sum()
    )


    total_collective = (
        history["Collective Share"]
        .sum()
    )


    total_qty = (
        history["Qty"]
        .sum()
    )


    total_event = (
        history["Event"]
        .nunique()
    )


    if total_event == 0:
        total_event = 1



    avg_customer = (
        total_customer /
        total_event
    )


    avg_collective = (
        total_collective /
        total_event
    )


    avg_qty = (
        total_qty /
        total_event
    )



    result["customer"] = (
        avg_customer * 1.25
    )


    result["collective"] = (
        avg_collective * 1.25
    )


    result["bottle"] = (
        avg_qty * 1.25
    )


    return result