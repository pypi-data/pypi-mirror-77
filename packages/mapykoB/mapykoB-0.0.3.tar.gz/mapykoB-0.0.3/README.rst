***********
Description
***********

Mapykob is a Python application that provides an easy way to experiment with Markov models. While built for educational purposes, it can both be used for educational or commercial purposes.PyPI hosting

*****
State
*****

|travis| |coverage| |format| |version| |license| |pyversions| |implementation| |status|


************
Installation
************

To install mapykoB simply run the following command in a terminal window::

    $  pip install mapykoB

If you would rather install from source, run the following commands in a terminal window::

    $  git clone https://github.com/octoandzl/mapykoB.git
    $  cd mapykob
    $  python setup.py install

*****
Usage
*****

An example would be::

    $  sample_data = np.array([
    $    [1, 1, 1, 0, 0, 0, 0, 0],
    $    [0, 1, 0, 0, 0, 1, 0, 0],
    $    [0, 0, 0, 0, 0, 1, 0, 1],
    $    [0, 0, 1, 0, 1, 1, 1, 1],
    $    [0, 0, 0, 0, 1, 0, 1, 0],
    $    [0, 1, 0, 0, 1, 1, 0, 1],
    $    [0, 0, 0, 1, 1, 1, 0, 0]])

    $  possible_observations = Counter(sample_data[i][j] for i in range(len(sample_data)) for j in range(len(sample_data[i])))
    $  M = 2
    $  V = len(possible_observations)
    $  hmm_discreet = hmm_discreet(M,sample_data,V)
    $  hmm_discreet.pi = np.array([0.5, 0.5])
    $  hmm_discreet.A = np.array([[0.7, 0.3], [0.4, 0.6]])
    $  hmm_discreet.B = np.array([[0.6, 0.4], [0.3, 0.7]])
    $  hmm_discreet.compute_alpha(0)
    $  p = hmm_discreet.compute_p_from_alpha(0)



.. |travis| image:: https://img.shields.io/travis/octoandzl/mapykoB?style=flat-square
    :target: https://travis-ci.org/octoandzl/mapykoB
.. |coverage| image:: https://coveralls.io/repos/github/octoandzl/mapykoB/badge.svg
    :target: https://coveralls.io/github/octoandzl/mapykoB
.. |version| image:: https://img.shields.io/pypi/v/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
.. |implementation| image:: https://img.shields.io/pypi/implementation/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
.. |status| image:: https://img.shields.io/pypi/status/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
.. |format| image:: https://img.shields.io/pypi/format/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
.. |license| image:: https://img.shields.io/pypi/l/mapykoB?style=flat-square
    :target: https://pypi.python.org/pypi/mapykoB
