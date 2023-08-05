"""Provides classes that produce differentiation stencil numpy arrays"""

__author__ = "Nikolai Dontschuk and Dan McCloskey"
__copyright__ = "Copyright 2020, Nikolai Dontschuk and Dan McCloskey"
__license__ = "Licensed under the Academic Free License version 3.0"

import numpy as np
from numpy.linalg import solve
from scipy import sparse

# TODO Write a function that handles boundary points in the base class, perhaps decorators for order/precision?

class DifferentiationStencil:
    # Relative and absolute tolerance for comparing floating point numbers
    atol = 1e-9  # default 1e-8
    rtol = 1e-6  # default 1e-5

    def __init__(self, order_d=None, sample_n=None, mesh_x=None):
        self.orderD = int(order_d)
        self.sampleN = int(sample_n)
        if not bool(self.sampleN % 2) or self.orderD >= self.sampleN:
            raise ValueError("The number of sampling points (N) must be odd and greater and the derivative order d.")
        self.mesh_x = mesh_x
        self.stencil = np.zeros((len(mesh_x), len(mesh_x)), dtype=np.dtype('d'))

    def __buildStencil__(self):
        raise NotImplementedError("You must call the derived classes for the stencil you want.")

    def get_stencil(self):
        return self.stencil




class SecondOrderSecondDerivative(DifferentiationStencil):
    def __init__(self, mesh_x, diff_mesh_x=None):
        """Provides a differentiation stencil that estimates the second derivative of a discreet 1D data with
        second order accuracy.  The discretization mesh, mesh_x, can be arbitrary but must be provided.  Optionally
        the spacing differences can also be provided to avoid re-calculation.
        """
        super().__init__(order_d=2, sample_n=3, mesh_x=mesh_x)
        self.__buildStencil__(diff_mesh_x)

    def __buildStencil__(self, diff_mesh_x):
        if diff_mesh_x is None:
            diff_mesh_x = np.diff(self.mesh_x)
        else:
            diff_mesh_x = np.array(diff_mesh_x)

        # Calculate stencil for situation where mesh step size is constant across the three points,i.e. hi=hi+1.
        diff_mesh_x_squared_inverted = 1/diff_mesh_x**2
        self.diff_mesh_x_squared_inverted = diff_mesh_x_squared_inverted
        low_diag = diff_mesh_x_squared_inverted
        upper_diag = np.copy(diff_mesh_x_squared_inverted)

        # Diag is one element short, we can extend it at the beginning or the end, it doesn't matter as it changes
        # if the forward or backwards step size (hi,hi+1) is used.
        diag = np.append(-2*diff_mesh_x_squared_inverted, -2*diff_mesh_x_squared_inverted[-1])

        # modify the indices where the diff_mesh_x changes
        mesh_change_idx = np.where(np.logical_not(np.isclose(diff_mesh_x[:-1], diff_mesh_x[1:], atol=self.atol, rtol=self.rtol)))[0]
        mesh_change_idx = np.unique(np.append(mesh_change_idx, mesh_change_idx + 1))

        for idx in mesh_change_idx:
            hm = diff_mesh_x[idx-1]  # hi-1
            h = diff_mesh_x[idx]     # hi
            s = np.array([[1, 1, 1],
                          [-hm, 0, h],
                          [0.5*hm**2, 0, 0.5*h**2]])
            c = solve(s, np.array([0, 0, 1]))
            low_diag[idx-1] = c[0]
            diag[idx] = c[1]
            try:
                upper_diag[idx] = c[2]
            except IndexError:
                pass  # this could happen at the back boundary.

        # modify the boundaries to do 'forward' and 'backwards' derivatives.

        n = np.shape(self.stencil)[0]

        self.stencil.ravel()[:n**2:n+1] = diag
        self.stencil.ravel()[1:n*(n-1):n+1] = upper_diag
        self.stencil.ravel()[n:n*(n+1):n+1] = low_diag

        h = diff_mesh_x[0]
        h2 = h + diff_mesh_x[1]
        h3 = h2 + diff_mesh_x[2]
        h4 = h3 + diff_mesh_x[3]
        first_row = np.array([0, h, h2, h3, h4])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        diag[0] = c[0]
        upper_diag[0] = c[1]
        self.stencil[0, 2] = c[2]
        self.stencil[0, 3] = c[3]
        self.stencil[0, 4] = c[4]

        h = diff_mesh_x[-1]
        h2 = h + diff_mesh_x[-2]
        h3 = h2 + diff_mesh_x[-3]
        h4 = h3 + diff_mesh_x[-4]
        first_row = np.array([0, -h, -h2, -h3, -h4])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        diag[-1] = c[0]
        low_diag[-1] = c[1]
        self.stencil[-1, -3] = c[2]
        self.stencil[-1, -4] = c[3]
        self.stencil[-1, -5] = c[4]

    def modifyEndPoints(self):
        '''Modifies the endpoints to use central difference approximations under the assumption of zero
        electric field outside of the diamond (ie. points beyond the boundary equal the boundary point)'''
        diff_mesh_x_squared_inverted = self.diff_mesh_x_squared_inverted
        self.stencil[0, 0] = -1*diff_mesh_x_squared_inverted[0]
        self.stencil[0, 1] = 1*diff_mesh_x_squared_inverted[0]
        self.stencil[0, 2:] = 0
        self.stencil[-1, -1] = -1*diff_mesh_x_squared_inverted[-1]
        self.stencil[-1, -2] = 1*diff_mesh_x_squared_inverted[-1]
        self.stencil[-1, :-2] = 0



class FourthOrderSecondDerivative(DifferentiationStencil):
    def __init__(self, mesh_x, diff_mesh_x=None):
        """Provides a differentiation stencil that estimates the second derivative of a discreet 1D data with
        second order accuracy.  The discretization mesh, mesh_x, can be arbitrary but must be provided.  Optionally
        the spacing differences can also be provided to avoid re-calculation.
        """
        super().__init__(order_d=2, sample_n=5, mesh_x=mesh_x)
        self.__buildStencil__(diff_mesh_x)

    def __buildStencil__(self, diff_mesh_x):
        if diff_mesh_x is None:
            diff_mesh_x = np.diff(self.mesh_x)
        else:
            diff_mesh_x = np.array(diff_mesh_x)

        # Calculate stencil for situation where mesh step size is constant across the three points,i.e. hi=hi+1.
        diff_mesh_x_squared_inverted = 1/(12*diff_mesh_x**2)
        self.diff_mesh_x_squared_inverted = diff_mesh_x_squared_inverted
        low_1_diag = 16*diff_mesh_x_squared_inverted

        upper_1_diag = np.copy(low_1_diag)
        low_2_diag = -1*diff_mesh_x_squared_inverted[:-1]  # Trim it
        upper_2_diag = np.copy(low_2_diag)
        # Diag is one element short, we can extend it at the beginning or the end, i  don't think it matters as it only
        # effects the specifically corrected boundaries.
        diag = np.append(-30*diff_mesh_x_squared_inverted, -30*diff_mesh_x_squared_inverted[-1])

        # modify the indices where the diff_mesh_x changes
        mesh_change_idx = np.where(np.logical_not(np.isclose(diff_mesh_x[:-1], diff_mesh_x[1:],
                                                             atol=self.atol, rtol=self.rtol)))[0]
        mesh_change_idx = np.unique(np.append(mesh_change_idx,
                                              [mesh_change_idx - 1, mesh_change_idx + 1, mesh_change_idx + 2]))
        # Don't do full solves for boundary points, they are handled explicitly.
        mesh_change_idx = mesh_change_idx[(mesh_change_idx < len(diag)) & (mesh_change_idx > 1)]

        for idx in mesh_change_idx:
            hm = diff_mesh_x[idx-1]
            hm2 = hm + diff_mesh_x[idx-2]
            try:
                h = diff_mesh_x[idx]
            except IndexError:
                h = hm  # We don't care, boundary problem gets specified later
            try:
                h2 = h + diff_mesh_x[idx+1]
            except IndexError:
                h2 = 2*h  # still don't care
            first_row = np.array([-hm2, -hm, 0, h, h2])
            s = np.array([[1, 1, 1, 1, 1],
                          first_row,
                          np.power(first_row, 2)/2,
                          np.power(first_row, 3)/6,
                          np.power(first_row, 4)/24])
            c = solve(s, np.array([0, 0, 1, 0, 0]))
            low_2_diag[idx-2] = c[0]
            low_1_diag[idx-1] = c[1]
            diag[idx] = c[2]
            try:
                upper_1_diag[idx] = c[3]
                upper_2_diag[idx] = c[4]
            except IndexError:
                pass  # this could happen at the back boundary.

        # modify the boundaries to do 'forward' and 'backwards' derivatives.
        # 4th order forward, first point
        h = diff_mesh_x[0]
        h2 = h + diff_mesh_x[1]
        h3 = h2 + diff_mesh_x[2]
        h4 = h3 + diff_mesh_x[3]
        first_row = np.array([0, h, h2, h3, h4])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        diag[0] = c[0]
        upper_1_diag[0] = c[1]
        upper_2_diag[0] = c[2]
        self.stencil[0, 3] = c[3]
        self.stencil[0, 4] = c[4]

        # 4th order forward, 2nd point
        hm = diff_mesh_x[0]
        h = diff_mesh_x[1]
        h2 = h + diff_mesh_x[2]
        h3 = h2 + diff_mesh_x[3]
        first_row = np.array([-hm, 0, h, h2, h3])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        low_1_diag[0] = c[0]
        diag[1] = c[1]
        upper_1_diag[1] = c[2]
        upper_2_diag[1] = c[3]
        self.stencil[1, 4] = c[4]

        # 4th order backwards, 2nd last point
        hm = diff_mesh_x[-2]
        hm2 = hm + diff_mesh_x[-3]
        hm3 = hm2 + diff_mesh_x[-4]
        h = diff_mesh_x[-1]
        first_row = np.array([-hm3, -hm2, -hm, 0, h])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        self.stencil[-2, -5] = c[0]
        low_2_diag[-2] = c[1]
        low_1_diag[-2] = c[2]
        diag[-2] = c[3]
        upper_1_diag[-1] = c[4]

        # 4th order backwards last point
        hm = diff_mesh_x[-1]
        hm2 = hm + diff_mesh_x[-2]
        hm3 = hm2 + diff_mesh_x[-3]
        hm4 = hm3 + diff_mesh_x[-4]
        first_row = np.array([-hm4, -hm3, -hm2, -hm, 0])
        s = np.array([[1, 1, 1, 1, 1],
                      first_row,
                      np.power(first_row, 2) / 2,
                      np.power(first_row, 3) / 6,
                      np.power(first_row, 4) / 24])
        c = solve(s, np.array([0, 0, 1, 0, 0]))
        self.stencil[-1, -5] = c[0]
        self.stencil[-1, -4] = c[1]
        low_2_diag[-1] = c[2]
        low_1_diag[-1] = c[3]
        diag[-1] = c[4]

        n = np.shape(self.stencil)[0]

        self.stencil.ravel()[:n**2:n+1] = diag
        self.stencil.ravel()[1:n*(n-1):n+1] = upper_1_diag
        self.stencil.ravel()[n:n*(n+1):n+1] = low_1_diag
        self.stencil.ravel()[2:n*(n-2):n+1] = upper_2_diag
        self.stencil.ravel()[n*2:n*(n+2):n+1] = low_2_diag

    def modifyEndPoints(self):
        '''Modifies the endpoints to use central difference approximations under the assumption of zero
        electric field outside of the diamond (ie. points beyond the boundary equal the boundary point)'''
        diff_mesh_x_squared_inverted = self.diff_mesh_x_squared_inverted
        #First and last points
        self.stencil[0, 0] = (-15)*diff_mesh_x_squared_inverted[0]
        self.stencil[0, 1] = (16)*diff_mesh_x_squared_inverted[0]
        self.stencil[0, 2] = (-1)*diff_mesh_x_squared_inverted[1]
        self.stencil[0, 3:] = 0
        self.stencil[-1, -1] = (-15)*diff_mesh_x_squared_inverted[-1]
        self.stencil[-1, -2] = (16)*diff_mesh_x_squared_inverted[-1]
        self.stencil[-1, -3] = (-1)*diff_mesh_x_squared_inverted[-2]
        self.stencil[-1, :-3] = 0
        #Second and second-last points
        self.stencil[1, 0] = (15)*diff_mesh_x_squared_inverted[0]
        self.stencil[1, 1] = (-30)*diff_mesh_x_squared_inverted[0]
        self.stencil[1, 2] = (16)*diff_mesh_x_squared_inverted[1]
        self.stencil[1, 3] = (-1)*diff_mesh_x_squared_inverted[2]
        self.stencil[1, 4:] = 0
        self.stencil[-2, -1] = (15)*diff_mesh_x_squared_inverted[-1]
        self.stencil[-2, -2] = (-30)*diff_mesh_x_squared_inverted[-1]
        self.stencil[-2, -3] = (16)*diff_mesh_x_squared_inverted[-2]
        self.stencil[-2, -4] = (-1) * diff_mesh_x_squared_inverted[-3]
        self.stencil[-2, :-4] = 0

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    """Testing stencils, if you don't want to do this don't run the module as main."""
    x = np.array([])
    for an_array in ([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1], np.linspace(2, 10, 30), [10.1, 10.2, 10.3, 10.4], np.linspace(10.5, 22, 30), [22.1, 22.2, 22.3, 22.4]):
        x = np.append(x, an_array)

    ex = np.exp(x)
    d2o2 = SecondOrderSecondDerivative(x).get_stencil()
    d2o4 = FourthOrderSecondDerivative(x).get_stencil()
    with np.printoptions(precision=3, suppress=True, linewidth=1000, threshold=100000):
        print(d2o4)
        print("\n****************\n")
    d2o2 = sparse.csr_matrix(d2o2)
    d2o4 = sparse.csr_matrix(d2o4)
    d2o2ex = d2o2.dot(ex)
    d2o4ex = d2o4.dot(ex)
    plt.plot(1 - ex/d2o2ex)
    plt.plot(1 - ex / d2o4ex)
    plt.show()
