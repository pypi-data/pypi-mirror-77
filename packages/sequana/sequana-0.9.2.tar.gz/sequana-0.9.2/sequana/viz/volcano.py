# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
# This is a copy of the biokit.viz.volcano module (from myself) since
# biokit will not be maintained in the future (merging its content
# into sequana.
#
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################


"""Volcano plot"""

import numpy as np
import pylab
import pandas as pd


__all__ = ['Volcano']


class Volcano(object):
    """Volcano plot

    In essence, just a scatter plot with annotations.

    .. plot::
        :width: 80%
        :include-source:

        import numpy as np
        fc = np.random.randn(1000)
        pvalue = np.random.randn(1000)

        from sequana.viz import Volcano
        v = Volcano(fc, -np.log10(pvalue**2))
        v.plot(pvalue_threshold=3)


    """

    def __init__(self, fold_changes=None, pvalues=None, color=None):
        """.. rubric:: constructor


        :param list fold_changes: 1D array or list
        :param list pvalues: 1D array or list
        :param df: a dataframe with those column names:
            fold_changes, pvalues, color (optional)


        """
        # try to compute the FC now
        #if self.fold_change is None:
        #    self.fold_change = pylab.log2(X1/X0)

        #if pvalue is None:
        #    # assume a normal distribution mean 0 and sigma 1
        #    import scipy.stats
        #    self.pvalue = - pylab.log10(scipy.stats.norm.pdf(abs(self.fold_change), 0,1)),

        self.fold_changes = np.array(fold_changes)
        self.pvalues = np.array(pvalues)
        assert len(self.fold_changes) == len(self.pvalues)

        if color is None:
            self.color = ['blue'] * len(self.pvalues)
        elif isinstance(color, str):
            self.color = [color] * len(self.pvalues)
        else:
            self.color = np.array(color)
        # TODO: check that the 3 columns have same length
        assert len(self.fold_changes) == len(self.color)


        self.df = pd.DataFrame({"fold_change": self.fold_changes,
            "pvalue": self.pvalues, 'color': self.color})

    def plot(self, size=10, alpha=0.5, marker='o', fontsize=16,
            xlabel='fold change', logy=False, 
            threshold_lines={"color": "black", 'ls': "--"},
            ylabel='p-value', pvalue_threshold=1.3, fold_change_threshold=1,

            add_broken_axes=False,
            broken_axes={"ylims": ((0,10), (50,100))}
            ):
        """

        :param size: size of the markers
        :param alpha: transparency of the marker
        :param fontsize:
        :param xlabel:
        :param ylabel:
        :param pvalue_threshold: adds an horizontal dashed line at
           the threshold provided.
        :param fold_change_threshold: colors in grey the absolute fold
            changes below a given threshold.

        """
        pylab.clf()
        mask1 = abs(self.fold_changes) < fold_change_threshold
        mask2 = abs(self.fold_changes) >= fold_change_threshold

        colors = self.df.color

        if add_broken_axes: 
            from brokenaxes import brokenaxes
            _ylims = broken_axes.get("ylims", None)
            _xlims = broken_axes.get("xlims", None)
            bax = brokenaxes(ylims=_ylims, xlims=_xlims)
        else:
            bax = pylab
        bax.scatter(self.fold_changes[mask1],
                self.pvalues[mask1],
                s=size,
                alpha=alpha,
                c='grey', marker=marker)
        bax.scatter(self.fold_changes[mask2],
                self.pvalues[mask2],
                s=size,
                alpha=alpha,
                c=colors[mask2])

        bax.grid()
        #pylab.ylim([0, pylab.ylim()[1]])
        #M = max(abs(self.fold_change)) * 1.1
        #pylab.xlim([-M, M])
        try:
            bax.set_xlabel(xlabel, fontsize=fontsize)
            bax.set_ylabel(ylabel, fontsize=fontsize)
        except:
            bax.xlabel(xlabel, fontsize=fontsize)
            bax.ylabel(ylabel, fontsize=fontsize)
    
        bax.axhline(pvalue_threshold, color=threshold_lines['color'], 
                linestyle=threshold_lines["ls"])
        bax.axvline(fold_change_threshold, 
                color=threshold_lines['color'],
                linestyle=threshold_lines["ls"])
        bax.axvline(-1*fold_change_threshold,
                color=threshold_lines['color'],
                linestyle=threshold_lines["ls"])

        if logy is True:
            ax = pylab.gca()
            ax.set(yscale="log")
            



