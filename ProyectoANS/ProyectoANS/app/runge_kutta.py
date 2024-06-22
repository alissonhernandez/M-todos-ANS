# runge_kutta.py
import numpy as np

def runge_kutta(f, y0, t):
    """
    Implementación del método de Runge-Kutta de cuarto orden (RK4).
    f : función
        La función a resolver (dy/dt = f(t, y)).
    y0 : float
        Valor inicial de y.
    t : array_like
        Array de valores de t donde se quiere evaluar y.
    """
    n = len(t)
    y = np.zeros(n)
    y[0] = y0
    for i in range(1, n):
        h = t[i] - t[i - 1]
        k1 = h * f(t[i - 1], y[i - 1])
        k2 = h * f(t[i - 1] + 0.5 * h, y[i - 1] + 0.5 * k1)
        k3 = h * f(t[i - 1] + 0.5 * h, y[i - 1] + 0.5 * k2)
        k4 = h * f(t[i], y[i - 1] + k3)
        y[i] = y[i - 1] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return y
