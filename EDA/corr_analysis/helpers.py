import pandas as _pd
import numpy as _np

from matplotlib import pyplot as plt
from matplotlib.collections import EllipseCollection
def plot_corr_ellipses(data, ax=None, **kwargs):

    M = _np.array(data)
    if not M.ndim == 2:
        raise ValueError('data must be a 2D array')
    if ax is None:
        fig, ax = plt.subplots(1, 1, subplot_kw={'aspect':'equal'})
        ax.set_xlim(-0.5, M.shape[1] - 0.5)
        ax.set_ylim(-0.5, M.shape[0] - 0.5)

    # xy locations of each ellipse center
    xy = _np.indices(M.shape)[::-1].reshape(2, -1).T

    # set the relative sizes of the major/minor axes according to the strength of
    # the positive/negative correlation
    w = _np.ones_like(M).ravel()
    h = 1 - _np.abs(M).ravel()
    a = 45 * _np.sign(M).ravel()

    ec = EllipseCollection(widths=w, heights=h, angles=a, units='x', offsets=xy,
                           transOffset=ax.transData, array=M.ravel(), **kwargs)
    ax.add_collection(ec)

    # if data is a DataFrame, use the row/column names as tick labels
    if isinstance(data, _pd.DataFrame):
        ax.set_xticks(_np.arange(M.shape[1]))
        ax.set_xticklabels(data.columns, rotation=90)
        ax.set_yticks(_np.arange(M.shape[0]))
        ax.set_yticklabels(data.index)

    return ec


def corr_partial(df):
    S = df.cov()
    S_1 = _np.linalg.inv(S)
    diag_matrix_s_1_sqrt = _np.diag(1/_np.sqrt(_np.diag(S_1)))
    ones_mask=-_np.ones((len(S),len(S)))
    _np.fill_diagonal(ones_mask,_np.ones(len(S)))
    almost_P = diag_matrix_s_1_sqrt@S_1@diag_matrix_s_1_sqrt
    return _pd.DataFrame(_np.multiply(ones_mask,almost_P), columns = df.columns, index = df.columns)

def R_2(df):
  if isinstance(df, _pd.DataFrame):
    df = df.to_numpy()
  S = _np.cov(df, rowvar=False)
  S_inv = _np.linalg.inv(S)
  return 1 - (1/(_np.diag(S)*_np.diag(S_inv)))
