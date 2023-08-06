# -*- coding: utf-8 -*-

"""
himmelblau_seb.py:
Booth function

Authors: Sander van Rijn, Leiden University


THERE IS NO WARRANTY, EXPRESS OR IMPLIED. WE DO NOT ASSUME ANY LIABILITY
FOR THE USE OF THIS SOFTWARE.  If software is modified to produce
derivative works, such modified software should be clearly marked.
Additionally, this program is free software you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation version 2.0 of the License.
Accordingly, this program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
"""

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction


def himmelblau_seb_hf(xx):
    """
    HIMMELBLAU FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx

    term1 = (x1**2 + x2 - 11)**2
    term2 = (x2**2 + x1 - 7)**2

    return term1 + term2


def himmelblau_seb_mf(xx):
    """
    HIMMELBLAU FUNCTION, MEDIUM FIDELITY CODE

    Proposed by Sebastian Schmitt, Honda Research Institute Europe (2019)

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx
    return himmelblau_seb_hf([0.75 * x1, 0.9 * x2]) + (0.9 * 0.75 * x1 * x2) ** 2 - 1


def himmelblau_seb_lf(xx):
    """
    HIMMELBLAU FUNCTION, LOWER FIDELITY CODE
    Calls: himmelblau_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function himmelblau_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx
    return himmelblau_seb_hf([0.7 * x1, 0.8 * x2]) + (x1 * x2) ** 2 - 1


#: Lower bound for Himmelblau function
l_bound = [-4, -4]
#: Upper bound for Himmelblau function
u_bound = [ 4,  4]

#: 2D Himmelblau function (Seb's version) with fidelities 'high', 'medium' and 'low'
himmelblau_seb = MultiFidelityFunction(
    "himmelblau sebastian",
    u_bound, l_bound,
    [himmelblau_seb_hf, himmelblau_seb_mf, himmelblau_seb_lf],
    fidelity_names=['high', 'medium', 'low']
)
