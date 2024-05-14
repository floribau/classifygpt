import pandas
from sklearn.metrics import f1_score
from statsmodels.stats.contingency_tables import mcnemar


def micro_f1_score(y_true: pandas.Series, y_pred: pandas.Series) -> float:
    """
    Calculates the micro f1 score for the given predictions.

    :param y_true: the correct labels
    :param y_pred: the predicted labels
    :return: micro f1 score
    """
    return f1_score(y_true, y_pred, average='micro')


def macro_f1_score(y_true: pandas.Series, y_pred: pandas.Series) -> float:
    """
    Calculates the macro f1 score for the given predictions.

    :param y_true: the correct labels
    :param y_pred: the predicted labels
    :return: macro f1 score
    """
    return f1_score(y_true, y_pred, average='macro')


def eval_f1_scores(paths_true: pandas.Series, paths_pred: pandas.Series) -> dict[str: float]:
    """
    Calculates micro and macro f1 scores for the category paths, second-level categories, and third-level categories.

    :param paths_true: the correct paths
    :param paths_pred: the predicted paths
    :return: Results for all six f1 scores. Keys: Paths Micro F1, Paths Macro F1, Second-Level Micro F1,
    Second-Level Macro F1, Third-Level Micro F1, Third-Level Macro F1
    """
    try:
        paths_micro_f1 = micro_f1_score(paths_true, paths_pred)
        paths_macro_f1 = macro_f1_score(paths_true, paths_pred)

        second_level_true = paths_true.apply(lambda x: x.split('>')[1])
        second_level_pred = paths_pred.apply(lambda x: x.split('>')[1])
        second_level_micro_f1 = micro_f1_score(second_level_true, second_level_pred)
        second_level_macro_f1 = macro_f1_score(second_level_true, second_level_pred)

        third_level_true = paths_true.apply(lambda x: x.split('>')[2])
        third_level_pred = paths_pred.apply(lambda x: x.split('>')[2])
        third_level_micro_f1 = micro_f1_score(third_level_true, third_level_pred)
        third_level_macro_f1 = macro_f1_score(third_level_true, third_level_pred)

        result_dict = {'Paths Micro F1': paths_micro_f1,
                       'Paths Macro F1': paths_macro_f1,
                       'Second-Level Micro F1': second_level_micro_f1,
                       'Second-Level Macro F1': second_level_macro_f1,
                       'Third-Level Micro F1': third_level_micro_f1,
                       'Third-Level Macro F1': third_level_macro_f1}
        return result_dict
    except IndexError as e:
        raise Exception(f"Incorrect path format: {e}")


def mcnemar_test(predictions1: list[str], predictions2: list[str]) -> float:
    """
    Performs a McNemar test on two given list of predictions. Used to test whether there's a difference in performance between the different approaches

    :param predictions1: the first list of category (or category path) predictions
    :param predictions2: the second list of category (or category path) predictions
    :return: the p-value calculated by the McNemar test
    """
    table = [[0, 0], [0, 0]]
    for pred1, pred2 in zip(predictions1, predictions2):
        if pred1 and pred2:
            table[0][0] += 1
        elif pred1 and not pred2:
            table[0][1] += 1
        elif not pred1 and pred2:
            table[1][0] += 1
        else:
            table[1][1] += 1
    result = mcnemar(table, exact=False)
    return result.pvalue
