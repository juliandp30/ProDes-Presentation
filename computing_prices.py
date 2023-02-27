def compute_price_by_weigth(res, bars, price):
    """Updating price by weigth

    Args:
        res (dict): Results of each analysis
        bars (dict): Names of the bars and prices
        price (float): Acummulated price

    Returns:
        float: updated price
    """

    # Computing price by weight
    weigth = res["steel_weight"]

    # For each: stirups and longitudinal
    for bar_type in [weigth["stirrups"], weigth["longitudinal"]]:
        # For each bar size
        for item in bar_type.keys():
            # don't include total weigth
            if item == "total":
                continue
            # price for each item
            item_price = bars[item] * bar_type[item]
            # acummulate price
            price += item_price

    return price


def compute_price_by_splices_and_heads(res, splices, heads, price):
    """Updating price by splices and heads

    Args:
        res (dict): Results of each analysis
        splices (dict): Names of the splices and prices
        heads (dict): Names of the splices and prices
        price (float): Acummulated price

    Returns:
        float: updated price
    """

    # Dicts by splices and heads
    spl = res["quantities"]["mechanical_splices"]
    hds = res["quantities"]["mechanical_heads"]

    # For each: splices and heads
    for ty in [spl, hds]:
        # Prices for each bar size
        data_prices = splices if ty == spl else heads

        # For each bar size
        for item in ty.keys():
            # don't include total weigth
            if item == "total":
                continue
            # price for each item
            item_price = data_prices[item] * ty[item]
            # acummulate price
            price += item_price

    return price


def assign_prices_global(results, bars, splices, heads):
    """Function that computes global prices for each analysis

    Args:
        results (dict): _description_
        bars (dict): Names of the bars and prices
        splices (dict): Names of the splices and prices
        heads (dict): Names of the heads and prices

    Returns:
        Results dictionary updated with prices
    """

    for key, res in results.items():
        # Computing prices for each analysis
        price = 0
        price = compute_price_by_weigth(res, bars, price)
        price = compute_price_by_splices_and_heads(res, splices, heads, price)

        # Assign final price
        res["price"] = int(price)

    return results