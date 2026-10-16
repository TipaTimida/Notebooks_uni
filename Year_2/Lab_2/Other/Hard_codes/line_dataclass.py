from typing import Callable, Optional
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from dataclasses import dataclass

@dataclass
class Experiment:
    x: np.ndarray
    Dx: np.ndarray
    y: np.ndarray
    Dy: np.ndarray
    xlabel: str
    ylabel: str
    ff: Callable

    # Optional fit results
    popt: Optional[np.ndarray] = None
    perr: Optional[np.ndarray] = None
    kappa2: Optional[float] = None
    ndof: Optional[int] = None
    covm: Optional[np.ndarray] = None


################## CHANGE #######################

def setup():
    """Return directory, file name, labels, and model function."""
    directory = '/home/gea/Desktop/notebooks/Notebooks/Year_2/Lab_2/Esperienza_0/'
    filename = 'data00.txt'
    x_label = r'$\Delta V$ [V]'
    y_label = 'I [mA]'

    def ff(x: np.ndarray, a: float, b: float) -> np.ndarray:
        return a * x + b

    return directory, filename, x_label, y_label, ff

####################################################à


def load_experiment(path, xlabel, ylabel, ff):
    """Load data file and return Experiment object."""
    x, Dx, y, Dy = np.loadtxt(path, unpack=True)  # file must have 4 columns
    return Experiment(x, Dx, y, Dy, xlabel, ylabel, ff)

def myplot(exp: Experiment):
    """Plot data with error bars."""
    plt.rc('font', size=16)
    plt.xlabel(exp.xlabel, fontsize=18)
    plt.ylabel(exp.ylabel, fontsize=18)
    plt.minorticks_on()
    plt.errorbar(exp.x, exp.y, exp.Dy, exp.Dx, linestyle='', color='black', marker='.')
    return

def plot_func(exp, init):
    """Plot data and function."""
    myplot(exp)
    xx = np.linspace(min(exp.x), max(exp.x), 500)
    plt.plot(xx, exp.ff(xx, *init), color='red')
    plt.show()
    return

def fit(exp, init, plot=True, save=False):
    """Fit experiment data with curve_fit and store results in the Experiment."""
    sigma = exp.Dy
    w = 1 / sigma**2
    popt, covm = curve_fit(exp.ff, exp.x, exp.y, init, sigma, absolute_sigma=False)
    kappa2 = ((w * (exp.y - exp.ff(exp.x, *popt))**2)).sum()
    ndof = len(exp.x) - len(init)
    perr = np.sqrt(np.diag(covm))

    # Save results into the Experiment object
    exp.popt = popt
    exp.perr = perr
    exp.kappa2 = kappa2
    exp.ndof = ndof
    exp.covm = covm

    # Print results
    print("Fit results")
    print("-----------")
    for i, (p, e) in enumerate(zip(popt, perr), start=1):
        print(f"p{i} = {p:.4f} ± {e:.4f}")
    print(f"\nKappa² = {kappa2:.3f}")
    print(f"ndof   = {ndof}")

    if plot: plot_func(exp, popt)
    if save: plt.savefig("fit.png")

    return exp


def correlation_matrix(exp):
    """Stampa e ritorna la matrice di correlazione (covarianza normalizzata)."""
    corr = exp.covm / np.outer(exp.perr, exp.perr)
    print("\nMatrice di correlazione (covarianza normalizzata):")
    print(corr.round(3))
    return


def effective_fit_line(exp: Experiment, init: tuple[float, ...]):
    """Riesegue il fit includendo l'incertezza su x (Dx)."""
    a_guess = exp.popt[0]  # pendenza dal primo fit
    sigma_eff = np.sqrt(exp.Dy**2 + (a_guess * exp.Dx)**2)
    pars_eff, covm_eff = curve_fit(exp.ff, exp.x, exp.y, init, sigma_eff, absolute_sigma=True)
    errors_eff = np.sqrt(np.diag(covm_eff))

    print("\nFit con errore efficace (considerando anche δV):")
    for i, (p, e) in enumerate(zip(pars_eff, errors_eff), start=1):
        print(f"  p{i} = {p:.4f} ± {e:.4f}")

    return


def effective_fit(exp: Experiment, init: tuple[float, ...], dx: float = 1e-6):
    """Riesegue il fit includendo l'incertezza su x (Dx), con propagazione automatica."""

    # Derivata numerica ∂f/∂x per ogni punto
    def df_dx(x, pars):
        return (exp.ff(x + dx, *pars) - exp.ff(x - dx, *pars)) / (2 * dx)

    # Usa i parametri già fittati per stimare la derivata locale
    slopes = df_dx(exp.x, exp.popt)

    # Propagazione dell'errore
    sigma_eff = np.sqrt(exp.Dy**2 + (slopes * exp.Dx)**2)

    # Rifai il fit con sigma_eff
    pars_eff, covm_eff = curve_fit(exp.ff, exp.x, exp.y, init, sigma_eff, absolute_sigma=True)
    errors_eff = np.sqrt(np.diag(covm_eff))

    print("\nFit con errore efficace (considerando anche δx):")
    for i, (p, e) in enumerate(zip(pars_eff, errors_eff), start=1):
        print(f"  p{i} = {p:.4f} ± {e:.4f}")

    return pars_eff, errors_eff, covm_eff


def residuals_plot(exp: Experiment):
    """Plotta i residui normalizzati rispetto al primo fit."""
    sigma = exp.Dy
    residui = (exp.y - exp.ff(exp.x, *exp.popt)) / sigma
    plt.figure()
    plt.axhline(0, color='gray', linestyle='--')
    plt.errorbar(exp.x, residui, yerr=1, fmt='o', color='blue')
    plt.xlabel(exp.xlabel)
    plt.ylabel('Residui normalizzati')
    plt.title('Analisi dei residui')
    plt.show()
    return


def prediction(exp, DeltaV_pred):
    """Fa una predizione a un certo ΔV con propagazione dell'errore."""
    I_pred = exp.ff(DeltaV_pred, *exp.popt)  # valore previsto
    J = np.array([DeltaV_pred, 1.0])         # Jacobiano [∂f/∂a, ∂f/∂b]
    var_I = J @ exp.covm @ J.T
    sigma_I = np.sqrt(var_I)

    print(f"\nPrevisione per ΔV' = {DeltaV_pred} V:")
    print(f"  I' = {I_pred:.4f} ± {sigma_I:.4f} mA")

    return


if __name__ == "__main__":
    directory, filename, x_label, y_label, ff = setup()
    exp = load_experiment(directory + filename, x_label, y_label, ff)

    # 1. find guess parameters  
    init = (2.1, 0)
    # plot_func(exp, init)

    # 2. if put False, don't show the graph
    fit(exp, init, plot=False)

    # 3. correlation matrix
    # correlation_matrix(exp)

    # 4. Fit con errore efficace
    # effective_fit_line(exp, init)
    # effective_fit(exp, init)

    # 5. Residui normalizzati
    # residuals_plot(exp)

    # 6. Predizione con propagazione dell'errore
    # prediction(exp, DeltaV_pred=20.0)