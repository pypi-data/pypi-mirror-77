#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Functions for generating PR-curve values and calculating average precision
#
import logging
import numpy as np
import pandas as pd
from scipy import interpolate
from ..util import np_col
from ._matchboxes import match_det
from . import coordinates

__all__ = ['pr', 'ap', 'fscore']
log = logging.getLogger(__name__)


def pr(det, anno, threshold=0.5, ignore=None):
    """ Computes PR-curve between detection and annotation dataframe.
    This function will match detections and annotations by computing the IoU.

    Args:
        det (pandas.DataFrame): Dataframe with detections
        anno (pandas.DataFrame): Dataframe with annotations
        threshold (number): Threshold to count a detection as true positive; Default **0.5**
        ignore (boolean, optional): Whether to consider the ignore flag of annotations when matching detections; Default **True**

    Returns:
        pandas.Dataframe: DataFrame with 3 columns **('precision', 'recall', 'confidence')**
        that has the points of the PR-curve and matching detection confidence values.

    Note:
        If ignore is true, this function will match the detections using :func:`~brambox.stat.coordinates.pdollar` and consider ignored annotations as regions
        that can be matched to multiple times,
        otherwise it will use a regular :func:`~brambox.stat.coordinates.iou` and discard the ignored labels.
        If there are no ignored annotations, this boils down to the same.

        By default (`ignore == None`), this function will check whether there are ignored annotations and set the ignore value accordingly.

    Note:
        If you want more control over the parameters to match detections (eg. Change the criteria to something else than IoU),
        you can call the :func:`brambox.stat.match_det` function and provide other arguments. |br|
        This function will first check whether the detection dataframe has tp/fp columns and compute them otherwise.
    """
    if ignore is None:
        ignore = anno.ignore.any()

    # Compute TP/FP
    if not {'tp', 'fp'}.issubset(det.columns):
        crit = coordinates.pdollar if ignore else coordinates.iou
        label = len({*det.class_label.unique(), *anno.class_label.unique()}) > 1
        det = match_det(det, anno, threshold, criteria=crit, class_label=label, ignore=2 if ignore else 0)
    elif not det.confidence.is_monotonic_decreasing:
        det = det.sort_values('confidence', ascending=False)

    # Compute PR
    if ignore:
        num_annos = (~anno.ignore).sum()
    else:
        num_annos = len(anno.index)
    if num_annos == 0:
        log.error(f'Number of {"non-ignored " if ignore else ""}annotations is zero, which does not make sense for a PR-curve.')

    matches = det.loc[(det.tp | det.fp), ['tp', 'fp', 'confidence']]
    if len(matches.index) == 0 and num_annos == 0:
        # No detections, nor annotations means perfect curve ?
        return pd.DataFrame({'precision': [1.0], 'recall': [1.0], 'confidence': [0.0]})

    summed = matches[['tp', 'fp']].cumsum()
    r = summed.tp / num_annos
    p = summed.tp / (summed.tp + summed.fp)

    pr = pd.DataFrame({'precision': p, 'recall': r, 'confidence': matches.confidence}).fillna(0)
    pr = pr.loc[~pr.confidence.duplicated(keep='last')].reset_index(drop=True)      # Only keep last point where detection confidence is the same
    return pr


def ap(pr):
    """ Computes the Average Precision from a PR-curve

    Args:
        pr (pandas.DataFrame): Precision and Recall values

    Returns:
        Number: average precision

    Note:
        The AP value is defined as follows:

        :math:`\\text{AP} = \\sum_n (R_n - R_{n-1}) P_n`

        where :math:`P_n` and :math:`R_n` are the precision and recall at the nth threshold `[1] <scikitap>`_.
        This implementation is not interpolated and is different from computing the area under the precision-recall curve
        with the trapezoidal rule.

    Warning:
        Be sure to use the correct way of computing the AP-value when comparing your results with published values. |br|
        A lot of people approximate the AP by computing the :func:`~brambox.stat.auc`.

    .. _scikitap: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score
    """
    if len(pr) == 0:
        return float('nan')

    if len(pr) == 1:
        pr = pr.loc[0]
        return pr.precision * pr.recall

    if not pr['recall'].is_monotonic_increasing:
        pr = pr.sort_values('recall')

    dr = pr['recall'].diff()
    dr.iat[0] = pr['recall'].iat[0]     # First item: dr = recall[0] - 0 = recall[0]
    return (pr['precision'] * dr).sum()


def fscore(pr, beta=1):
    """ Computes the F-scores of every point on your PR-curve.

    Args:
        pr (pandas.DataFrame): Precision and Recall values
        beta (positive number, optional): Weighing factor for the precision; Default **1**

    Returns:
        pandas.Dataframe: DataFrame with 3 columns **('f{beta}', 'recall', 'confidence')**
        that contains the points of the F-curve and matching detection confidence values.

    Note:
        The F-score is defined as follows:

        :math:`F_{\\beta} = (1 + \\beta^2) * \\frac{P * R}{(\\beta^2 * P) + R}`

        This means the beta factor can be used to weigh the importance of the precision values over the recall.
        Typical values include 0.5, 1 and 2.

    Note:
        The column name of the F-score is computed as follows:

        .. code-block:: python

            f'f{beta.replace(".", "_")}'

    Warning:
        If both precision and recall are equal to zero, the F-score will also be set to zero as well.
    """
    p = np_col(pr, 'precision')
    r = np_col(pr, 'recall')
    b2 = beta * beta

    f = (1 + b2) * (p * r)
    f[f != 0] /= (b2 * p[f != 0] + r[f != 0])
    return pd.DataFrame({f'f{str(beta).replace(".", "_")}': f, 'recall': r, 'confidence': pr.confidence})
