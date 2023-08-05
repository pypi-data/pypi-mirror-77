# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines functions that can be used in HyperDrive to describe a hyperparameter search space.

These functions are used to specify different types of hyperparameter distributions. The distributions are
defined when you configure sampling for a hyperparameter sweep. For example, when you use the
:class:`azureml.train.hyperdrive.RandomParameterSampling` class, you can
choose to sample from a set of discrete values or a distribution of continuous values. In this
case, you could use the :func:`azureml.train.hyperdrive.parameter_expressions.choice` function to generate
a discrete set of values and :func:`azureml.train.hyperdrive.parameter_expressions.uniform` function to generate
a distribution of continuous values.

For examples of using these functions, see the tutorial:
https://docs.microsoft.com/azure/machine-learning/how-to-tune-hyperparameters.
"""


from azureml.train.hyperdrive.exceptions import HyperDriveConfigException


def choice(*options):
    """Specify a discrete set of options to sample from.

    :param options: The list of options to choose from.
    :type options: list
    :return: The stochastic expression.
    :rtype: list
    """
    if len(options) == 0:
        raise HyperDriveConfigException("Please specify an input for choice.")

    error_msg = ("Choice only accepts non-empty single list, non-empty single range() or a positive "
                 "number of arbitrary comma separated inputs.")
    for item in options:
        if isinstance(item, range):
            if len(options) > 1 or not item:
                raise HyperDriveConfigException(error_msg)
            return ["choice", [list(item)]]
        if isinstance(item, list):
            if len(options) > 1 or not item:
                raise HyperDriveConfigException(error_msg)
            return ["choice", [item]]

    return ["choice", [list(options)]]


def randint(upper):
    """Specify a set of random integers in the range [0, upper).

    The semantics of this distribution is that there is no more correlation in the loss function
    between nearby integer values, as compared with more distant integer values.
    This is an appropriate distribution for describing random seeds for example.
    If the loss function is probably more correlated for nearby integer values,
    then you should probably use one of the "quantized" continuous distributions,
    such as either quniform, qloguniform, qnormal or qlognormal.

    :param upper: The exclusive upper bound for the range of integers.
    :type upper: int
    :return: The stochastic expression.
    :rtype: list
    """
    if upper <= 0:
        raise HyperDriveConfigException("randint expects a positive number as input.")

    return ["randint", [upper]]


def uniform(min_value, max_value):
    """Specify a uniform distribution from which samples are taken.

    :param min_value: The minimum value in the range (inclusive).
    :type min_value: float
    :param max_value: The maximum value in the range (inclusive).
    :type max_value: float
    :return: The stochastic expression.
    :rtype: list
    """
    if min_value >= max_value:
        raise HyperDriveConfigException("uniform requires min_value < max_value")

    return ["uniform", [min_value, max_value]]


def quniform(min_value, max_value, q):
    """Specify a uniform distribution of the form round(uniform(min_value, max_value) / q) * q.

    This is suitable for a discrete value with respect to which the objective is still somewhat "smooth",
    but which should be bounded both above and below.

    :param min_value: The minimum value in the range (inclusive).
    :type min_value: float
    :param max_value: The maximum value in the range (inclusive).
    :type max_value: float
    :param q: The smoothing factor.
    :type q: int
    :return: The stochastic expression.
    :rtype: list
    """
    if min_value >= max_value:
        raise HyperDriveConfigException("quniform requires min_value < max_value")

    return ["quniform", [min_value, max_value, q]]


def loguniform(min_value, max_value):
    """Specify a log uniform distribution.

    A value is drawn according to exp(uniform(min_value, max_value)) so that the logarithm
    of the return value is uniformly distributed.
    When optimizing, this variable is constrained to the interval [exp(min_value), exp(max_value)]

    :param min_value: The minimum value in the range will be exp(min_value)(inclusive).
    :type min_value: float
    :param max_value: The maximum value in the range will be exp(max_value) (inclusive).
    :type max_value: float
    :return: The stochastic expression.
    :rtype: list
    """
    if min_value > max_value:
        raise HyperDriveConfigException("loguniform requires min_value <= max_value")

    return ["loguniform", [min_value, max_value]]


def qloguniform(min_value, max_value, q):
    """Specify a uniform distribution of the form round(exp(uniform(min_value, max_value) / q) * q.

    This is suitable for a discrete variable with respect to which the objective is "smooth",
    and gets smoother with the size of the value, but which should be bounded both above and below.

    :param min_value: The minimum value in the range (inclusive).
    :type min_value: float
    :param max_value: The maximum value in the range (inclusive).
    :type max_value: float
    :param q: The smoothing factor.
    :type q: int
    :return: The stochastic expression.
    :rtype: list
    """
    if min_value > max_value:
        raise HyperDriveConfigException("qloguniform requires min_value <= max_value")

    return ["qloguniform", [min_value, max_value, q]]


def normal(mu, sigma):
    """Specify a real value that is normally-distributed with mean mu and standard deviation sigma.

    When optimizing, this is an unconstrained variable.

    :param mu: The mean of the normal distribution.
    :type mu: float
    :param sigma: the standard deviation of the normal distribution.
    :type sigma: float
    :return: The stochastic expression.
    :rtype: list
    """
    if sigma < 0:
        raise HyperDriveConfigException("Standard deviation should be either zero or positive.")

    return ["normal", [mu, sigma]]


def qnormal(mu, sigma, q):
    """Specify a value like round(normal(mu, sigma) / q) * q.

    Suitable for a discrete variable that probably takes a value around mu, but is fundamentally unbounded.

    :param mu: The mean of the normal distribution.
    :type mu: float
    :param sigma: The standard deviation of the normal distribution.
    :type sigma: float
    :param q: The smoothing factor.
    :type q: int
    :return: The stochastic expression.
    :rtype: list
    """
    if sigma < 0:
        raise HyperDriveConfigException("Standard deviation should be either zero or positive.")

    return ["qnormal", [mu, sigma, q]]


def lognormal(mu, sigma):
    """Specify a value drawn according to exp(normal(mu, sigma)).

    The logarithm of the return value is normally distributed.
    When optimizing, this variable is constrained to be positive.

    :param mu: The mean of the normal distribution.
    :type mu: float
    :param sigma: The standard deviation of the normal distribution.
    :type sigma: float
    :return: The stochastic expression.
    :rtype: list
    """
    if sigma < 0:
        raise HyperDriveConfigException("Standard deviation should be either zero or positive.")

    return ["lognormal", [mu, sigma]]


def qlognormal(mu, sigma, q):
    """Specify a value like round(exp(normal(mu, sigma)) / q) * q.

    Suitable for a discrete variable with respect to which the objective is smooth and gets smoother
    with the size of the variable, which is bounded from one side.

    :param mu: The mean of the normal distribution.
    :type mu: float
    :param sigma: The standard deviation of the normal distribution.
    :type sigma: float
    :param q: The smoothing factor.
    :type q: int
    :return: The stochastic expression.
    :rtype: list
    """
    if sigma < 0:
        raise HyperDriveConfigException("Standard deviation should be either zero or positive.")

    return ["qlognormal", [mu, sigma, q]]
