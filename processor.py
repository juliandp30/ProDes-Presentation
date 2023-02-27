"""
Module for processing pandas' data frame

"""


def new_analysis_constructor():
    """Function that initiliaze analysisi objects

    Args:
        analysis_name (str): Name of analysis

    Returns:
        dict: initialized object
    """
    data_analysis = {
        "steel_weight": {
            "stirrups": {"total": 0},
            "longitudinal": {"total": 0},
            "total": 0,
            "unit_weight": 0,
        },
        "quantities": {
            "figures": {"total": 0, "stirrups": 0, "longitudinal": 0},
            "pieces": {"total": 0, "stirrups": 0, "longitudinal": 0},
            "mechanical_splices": {"total": 0},
            "mechanical_heads": {"total": 0},
            "blueprints": 0,
        },
        "price": 0,
        "scores": {
            "by_weigth": 0,
            "by_price": 0,
            "by_pieces": 0,
            "by_figures": 0,
            "by_blueprints": 0,
            "total": 0,
        },
    }

    return data_analysis


def assign_values(result, data_heads, data_analysis):
    """Function that assigns analysis data in the dictionary

    Args:
        result (array): anaylisis results from data frame
        data_heads (array): column name from data frame
        data_analysis (dict): initialized dictionary

    Returns:
        dict: data_analysisi dictionary updated
    """

    # For each value of the analysis
    for i, col in enumerate(data_heads):

        # Column name split
        txts_col = col.split()
        # bar size in column name
        calibre = txts_col[-1]
        # bar type in column name
        bar_type = txts_col[-2] if len(txts_col) > 1 else None

        # First column is the name
        if i == 0:
            continue

        # general weights
        if "Peso" in col or "peso" in col:
            # Stirups weigth
            if "Ref.Tran" in col:
                val1 = "stirrups"
                calibre = "total"
            # Longitudinal bars weigth
            if "Ref.Long" in col:
                val1 = "longitudinal"
                calibre = "total"
            # Striups detail for each bar size
            if "Est" in col:
                val1 = "stirrups"
            # Longitudinal bars detail for each bar size
            if "Bar" in col:
                val1 = "longitudinal"
            # Total weigth
            if "TOTAL" in col:
                val1 = "total"
                data_analysis["steel_weight"][val1] = result[i]
                continue

            # Filling information
            data_analysis["steel_weight"][val1][calibre] = result[i]
            continue

        # For mechanical heads
        if "Cabezas" in col or "cabezas" in col:
            # Total heads
            if "Cantidad" in col:
                data_analysis["quantities"]["mechanical_heads"]["total"] = result[i]
                continue

            # Mechanical head detail for each bar size
            data_analysis["quantities"]["mechanical_heads"][calibre] = result[i]
            continue

        # For mechanical splices
        if "Empalmes" in col or "empalmes" in col:
            # Total splices
            if "Cantidad" in col:
                data_analysis["quantities"]["mechanical_splices"]["total"] = result[i]
                continue

            # Mechanical splices detail for each bar size
            data_analysis["quantities"]["mechanical_splices"][calibre] = result[i]
            continue

        # For number of bars
        if (
            "Cantidad Barras" in col
            or "cantidad Bar" in col
            or "cantidad Est" in col
            or "Cantidad Estribos" in col
        ):
            # Total longitudinal bars
            if "Barras" in col:
                data_analysis["quantities"]["pieces"]["total"] += result[i]
                data_analysis["quantities"]["pieces"]["longitudinal"] = result[i]
                continue
            # Total stirrups
            if "Estribos" in col:
                data_analysis["quantities"]["pieces"]["total"] += result[i]
                data_analysis["quantities"]["pieces"]["stirrups"] = result[i]
                continue

            # Total pieces for each bar size and type
            data_analysis["quantities"]["pieces"][bar_type + calibre] = result[i]
            continue

        # For number of figures
        if "Figuras" in col:
            # Total longitudinal bars
            if "RefLong" in col:
                data_analysis["quantities"]["figures"]["longitudinal"] = result[i]
            # Total stirrups
            if "RefTrans" in col:
                data_analysis["quantities"]["figures"]["stirrups"] = result[i]

            # Total of figures
            data_analysis["quantities"]["figures"]["total"] += result[i]
            continue

        # For number of blueprints
        if "Planos" in col or "planos" in col:
            # Total of figures
            data_analysis["quantities"]["blueprints"] += result[i]

    return data_analysis


def results_constructor(data):
    """Function that builds general data

    Args:
        data (pandas dataframe)

    Returns:
        dict: general results compilation
        lists: names of used bars
    """

    # Column namess
    data_heads = data.columns.values
    # Analysisis values
    data_values = data.values

    # Initializing output
    results = {}
    names_for_weight = []
    names_for_splices = []
    names_for_heads = []

    # For each analysis
    for data_i in data_values:
        # Object constructor
        analysis_results = new_analysis_constructor()
        # Values
        analysis_results = assign_values(data_i, data_heads, analysis_results)
        # Updating result dict
        results[data_i[0]] = analysis_results

        # Computing names of used bars
        names_for_weight = list(
            set(
                [
                    name
                    for name in [
                        *names_for_weight,
                        *analysis_results["steel_weight"]["longitudinal"],
                        *analysis_results["steel_weight"]["stirrups"],
                    ]
                    if name != "total"
                ]
            )
        )
        # Computing names of used bars in splices
        names_for_splices = list(
            set(
                [
                    name
                    for name in [
                        *names_for_splices,
                        *analysis_results["quantities"]["mechanical_splices"],
                    ]
                    if name != "total"
                ]
            )
        )
        # Computing names of used bars in heads
        names_for_heads = list(
            set(
                [
                    name
                    for name in [
                        *names_for_heads,
                        *analysis_results["quantities"]["mechanical_heads"],
                    ]
                    if name != "total"
                ]
            )
        )

    return results, names_for_weight, names_for_splices, names_for_heads


def computing_unit_weigths(results, area):
    """Function that computes unit weights

    Args:
        results (dict): analysis results
        area (float): building area

    Returns:
        results: updated dict
    """

    # Computing unit weight for each analysis
    for res in results.values():
        res["steel_weight"]["unit_weight"] = res["steel_weight"]["total"] * 1000 / area

    return results


def get_lists_to_graph(results):
    """Lists for graphical output

    Returns:
        dict: lists
    """

    # Data lists
    keys = []
    list_weigth = []
    list_price = []
    list_npieces = []
    list_nfigures = []
    list_nblueprints = []
    list_score = []

    # For each analysis
    for key, res in results.items():
        keys.append(key)
        list_weigth.append(res["steel_weight"]["total"])
        list_price.append(res["price"])
        list_nfigures.append(res["quantities"]["figures"]["total"])
        list_npieces.append(res["quantities"]["pieces"]["total"])
        list_nblueprints.append(res["quantities"]["blueprints"])
        list_score.append(res["scores"]["total"])

    # Dictionary of lists
    lists = dict(
        keys = keys,
        by_weigth=list_weigth,
        by_price=list_price,
        by_pieces=list_npieces,
        by_figures=list_nfigures,
        by_blueprints=list_nblueprints,
        by_score=list_score,
    )

    return lists
