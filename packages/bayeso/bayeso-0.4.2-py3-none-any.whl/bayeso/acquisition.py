# acquisition
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: February 01, 2020

import numpy as np
import scipy.stats

from bayeso import constants


def pi(pred_mean, pred_std, Y_train, jitter=constants.JITTER_ACQ):
    """
    It is a probability improvement criterion.

    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ).
    :type pred_mean: numpy.ndarray
    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ).
    :type pred_std: numpy.ndarray
    :param Y_train: outputs of `X_train`. Shape: (n, 1).
    :type Y_train: numpy.ndarray
    :param jitter: jitter for `pred_std`.
    :type jitter: float, optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray)
    assert isinstance(pred_std, np.ndarray)
    assert isinstance(Y_train, np.ndarray)
    assert isinstance(jitter, float)
    assert len(pred_mean.shape) == 1
    assert len(pred_std.shape) == 1
    assert len(Y_train.shape) == 2
    assert pred_mean.shape[0] == pred_std.shape[0]

    with np.errstate(divide='ignore'):
        val_z = (np.min(Y_train) - pred_mean) / (pred_std + jitter)
    return scipy.stats.norm.cdf(val_z)

def ei(pred_mean, pred_std, Y_train, jitter=constants.JITTER_ACQ):
    """
    It is an expected improvement criterion.

    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ).
    :type pred_mean: numpy.ndarray
    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ).
    :type pred_std: numpy.ndarray
    :param Y_train: outputs of `X_train`. Shape: (n, 1).
    :type Y_train: numpy.ndarray
    :param jitter: jitter for `pred_std`.
    :type jitter: float, optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray)
    assert isinstance(pred_std, np.ndarray)
    assert isinstance(Y_train, np.ndarray)
    assert isinstance(jitter, float)
    assert len(pred_mean.shape) == 1
    assert len(pred_std.shape) == 1
    assert len(Y_train.shape) == 2
    assert pred_mean.shape[0] == pred_std.shape[0]

    with np.errstate(divide='ignore'):
        val_z = (np.min(Y_train) - pred_mean) / (pred_std + jitter)
    return (np.min(Y_train) - pred_mean) * scipy.stats.norm.cdf(val_z) + pred_std * scipy.stats.norm.pdf(val_z)

def ucb(pred_mean, pred_std, Y_train=None, kappa=2.0, is_increased=True):
    """
    It is a Gaussian process upper confidence bound criterion.

    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ).
    :type pred_mean: numpy.ndarray
    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ).
    :type pred_std: numpy.ndarray
    :param Y_train: outputs of `X_train`. Shape: (n, 1).
    :type Y_train: numpy.ndarray, optional
    :param kappa: trade-off hyperparameter between exploration and exploitation.
    :type kappa: float, optional
    :param is_increased: flag for increasing a kappa value as `Y_train` grows. If `Y_train` is None, it is ignored, which means `kappa` is fixed.
    :type is_increased: bool., optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray)
    assert isinstance(pred_std, np.ndarray)
    assert isinstance(Y_train, np.ndarray) or Y_train is None
    assert isinstance(kappa, float)
    assert isinstance(is_increased, bool)
    assert len(pred_mean.shape) == 1
    assert len(pred_std.shape) == 1
    if Y_train is not None:
        assert len(Y_train.shape) == 2
    assert pred_mean.shape[0] == pred_std.shape[0]

    if is_increased and Y_train is not None:
        kappa_ = kappa * np.log(Y_train.shape[0])
    else:
        kappa_ = kappa
    return -pred_mean + kappa_ * pred_std

def aei(pred_mean, pred_std, Y_train, noise,
    jitter=constants.JITTER_ACQ
):
    """
    It is an augmented expected improvement criterion.

    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ).
    :type pred_mean: numpy.ndarray
    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ).
    :type pred_std: numpy.ndarray
    :param Y_train: outputs of `X_train`. Shape: (n, 1).
    :type Y_train: numpy.ndarray
    :param noise: noise for augmenting exploration.
    :type noise: float
    :param jitter: jitter for `pred_std`.
    :type jitter: float, optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray)
    assert isinstance(pred_std, np.ndarray)
    assert isinstance(Y_train, np.ndarray)
    assert isinstance(noise, float)
    assert isinstance(jitter, float)
    assert len(pred_mean.shape) == 1
    assert len(pred_std.shape) == 1
    assert len(Y_train.shape) == 2
    assert pred_mean.shape[0] == pred_std.shape[0]

    with np.errstate(divide='ignore'):
        val_z = (np.min(Y_train) - pred_mean) / (pred_std + jitter)
    ei = (np.min(Y_train) - pred_mean) * scipy.stats.norm.cdf(val_z) + pred_std * scipy.stats.norm.pdf(val_z)
    aei = ei * (1.0 - noise / np.sqrt(pred_std**2 + noise**2))
    return aei

# pred_std and Y_train are ignored.
def pure_exploit(pred_mean, pred_std=None, Y_train=None):
    """
    It is a pure exploitation criterion.

    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ).
    :type pred_mean: numpy.ndarray
    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ). It can be given, but it is ignored when it works.
    :type pred_std: numpy.ndarray, optional
    :param Y_train: outputs of `X_train`. Shape: (n, 1). It can be given, but it is ignored when it works.
    :type Y_train: numpy.ndarray, optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray)
    assert isinstance(pred_std, np.ndarray) or pred_std is None
    assert isinstance(Y_train, np.ndarray) or Y_train is None
    assert len(pred_mean.shape) == 1
    if pred_std is not None:
        assert len(pred_std.shape) == 1
        assert pred_mean.shape[0] == pred_std.shape[0]
    if Y_train is not None:
        assert len(Y_train.shape) == 2

    return -pred_mean

# pred_mean and Y_train are ignored.
def pure_explore(pred_std, pred_mean=None, Y_train=None):
    """
    It is a pure exploration criterion.

    :param pred_std: posterior predictive standard deviation function over `X_test`. Shape: (l, ).
    :type pred_std: numpy.ndarray
    :param pred_mean: posterior predictive mean function over `X_test`. Shape: (l, ). It can be given, but it is ignored when it works.
    :type pred_mean: numpy.ndarray, optional
    :param Y_train: outputs of `X_train`. Shape: (n, 1). It can be given, but it is ignored when it works.
    :type Y_train: numpy.ndarray, optional

    :returns: acquisition function values. Shape: (l, ).
    :rtype: numpy.ndarray

    :raises: AssertionError

    """

    assert isinstance(pred_mean, np.ndarray) or pred_mean is None
    assert isinstance(pred_std, np.ndarray)
    assert isinstance(Y_train, np.ndarray) or Y_train is None
    assert len(pred_std.shape) == 1
    if pred_mean is not None:
        assert len(pred_mean.shape) == 1
        assert pred_mean.shape[0] == pred_std.shape[0]
    if Y_train is not None:
        assert len(Y_train.shape) == 2

    return pred_std
