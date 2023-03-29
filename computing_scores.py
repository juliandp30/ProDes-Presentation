def score_1Dmodel(data, value, min_score=1, max_score=10):
    """1D model for computing scores

    Returns:
        score (float)
    """

    # Data info for 1D model
    Y1, Y2, X1, X2 = max_score, min_score, min(data), max(data)
    # Line-Slope
    m = (Y2 - Y1) / (X2 - X1) if (X2 - X1) != 0 else 0

    # New Y
    score = m * (value - X1) + Y1 if m != 0 else Y1

    return score


def get_lists(results):
    """Computes lists of data

    Returns:
        dict: lists of eah item to evaluate
    """

    # Data lists
    list_weigth = []
    list_price = []
    list_npieces = []
    list_nfigures = []
    list_nblueprints = []

    # For each analysis
    for res in results.values():
        list_weigth.append(res["steel_weight"]["total"])
        list_price.append(res["price"])
        list_nfigures.append(res["quantities"]["figures"]["total"])
        list_npieces.append(res["quantities"]["pieces"]["total"])
        list_nblueprints.append(res["quantities"]["blueprints"])

    # Dictionary that will be returned
    lists = dict(
        by_weigth=list_weigth,
        by_price=list_price,
        by_pieces=list_npieces,
        by_figures=list_nfigures,
        by_blueprints=list_nblueprints,
    )

    return lists


def assign_scores(results, scores_data):
    """Funtion that computed the scores

    Args:
        results (dict): Analysisis results
        scores_data (dict): maximum scores for each item

    Returns:
        results: updated
    """

    # Getting list of data
    lists = get_lists(results)

    # For each result, it is computed the scores
    for res in results.values():
        # Values of the results
        values = dict(
            by_weigth=res["steel_weight"]["total"],
            by_pieces=res["quantities"]["pieces"]["total"],
            by_figures=res["quantities"]["figures"]["total"],
            by_blueprints=res["quantities"]["blueprints"],
        )

        # For each result it is computed the score
        for li in lists.keys():
            # For each item to evaluate
            res["scores"][li] = score_1Dmodel(
                lists[li], values[li], max_score=scores_data[li]
            )
            # Total acummulated score
            res["scores"]["total"] += res["scores"][li]

    return results
