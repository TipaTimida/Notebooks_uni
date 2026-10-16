import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class Experiment:
    def __init__(self, x, Dx, y, Dy, xlabel, ylabel, ff):
        self.x = x
        self.Dx = Dx
        self.y = y
        self.Dy = Dy
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ff = ff

        # Risultati fit
        self.popt = None
        self.perr = None
        self.kappa2 = None
        self.ndof = None
        self.covm = None

    # ------------------ CONSTRUCTORS ------------------

    @classmethod
    def from_file(cls, path, xlabel, ylabel, ff):
        x, Dx, y, Dy = np.loadtxt(path, unpack=True)
        return cls(x, Dx, y, Dy, xlabel, ylabel, ff)

    # ------------------ PLOT ------------------

    def plot_data(self):
        plt.rc('font', size=16)
        plt.xlabel(self.xlabel, fontsize=18)
        plt.ylabel(self.ylabel, fontsize=18)
        plt.minorticks_on()
        plt.errorbar(self.x, self.y, self.Dy, self.Dx,
                     linestyle='', color='black', marker='.')
        return

    def plot_func(self, params, color="red"):
        self.plot_data()
        xx = np.linspace(min(self.x), max(self.x), 500)
        plt.plot(xx, self.ff(xx, *params), color=color)
        plt.show()

    def residuals_plot(self):
        """Plotta i residui normalizzati rispetto al fit."""
        if self.popt is None:
            raise RuntimeError("Devi eseguire il fit prima di plottare i residui.")
        sigma = self.Dy
        residui = (self.y - self.ff(self.x, *self.popt)) / sigma
        plt.figure()
        plt.axhline(0, color='gray', linestyle='--')
        plt.errorbar(self.x, residui, yerr=1, fmt='o', color='blue')
        plt.xlabel(self.xlabel)
        plt.ylabel('Residui normalizzati')
        plt.title('Analisi dei residui')
        plt.show()

    # ------------------ FIT ------------------

    def fit(self, init, plot=True, save=False):
        """Fit con curve_fit e salvataggio risultati."""
        sigma = self.Dy
        w = 1 / sigma**2

        popt, covm = curve_fit(self.ff, self.x, self.y, init, sigma, absolute_sigma=False)
        residuals = self.y - self.ff(self.x, *popt)
        kappa2 = ((w * residuals**2)).sum()
        ndof = len(self.x) - len(init)
        perr = np.sqrt(np.diag(covm))

        # salva
        self.popt, self.perr, self.kappa2, self.ndof, self.covm = popt, perr, kappa2, ndof, covm

        # stampa
        print("Fit results")
        for i, (p, e) in enumerate(zip(popt, perr), start=1):
            print(f"p{i} = {p:.4f} ± {e:.4f}")
        print(f"\nKappa² = {kappa2:.3f}")
        print(f"ndof   = {ndof}")

        if plot:
            self.plot_func(popt)
        if save:
            plt.savefig("fit.png")

        return popt, perr

    def correlation_matrix(self):
        """Stampa la matrice di correlazione."""
        if self.covm is None:
            raise RuntimeError("Fit non ancora eseguito.")
        corr = self.covm / np.outer(self.perr, self.perr)
        print("\nMatrice di correlazione:")
        print(corr.round(3))
        return corr

    def effective_fit_line(self, init):
        """Fit con errore efficace: Dy² + (a*Dx)²"""
        if self.popt is None:
            raise RuntimeError("Devi prima fare il fit semplice.")
        a_guess = self.popt[0]
        sigma_eff = np.sqrt(self.Dy**2 + (a_guess * self.Dx)**2)
        pars_eff, covm_eff = curve_fit(self.ff, self.x, self.y, init,
                                       sigma_eff, absolute_sigma=True)
        errors_eff = np.sqrt(np.diag(covm_eff))
        print("\nFit con errore efficace (δV incluso):")
        for i, (p, e) in enumerate(zip(pars_eff, errors_eff), start=1):
            print(f"  p{i} = {p:.4f} ± {e:.4f}")
        return pars_eff, errors_eff, covm_eff

    def effective_fit(self, init, dx=1e-6):
        """Fit con errore efficace e propagazione automatica δx."""

        def df_dx(x, pars):
            return (self.ff(x + dx, *pars) - self.ff(x - dx, *pars)) / (2*dx)

        if self.popt is None:
            raise RuntimeError("Devi prima fare il fit semplice.")
        slopes = df_dx(self.x, self.popt)
        sigma_eff = np.sqrt(self.Dy**2 + (slopes * self.Dx)**2)

        pars_eff, covm_eff = curve_fit(self.ff, self.x, self.y, init,
                                       sigma_eff, absolute_sigma=True)
        errors_eff = np.sqrt(np.diag(covm_eff))
        print("\nFit con errore efficace (δx propagato):")
        for i, (p, e) in enumerate(zip(pars_eff, errors_eff), start=1):
            print(f"  p{i} = {p:.4f} ± {e:.4f}")
        return pars_eff, errors_eff, covm_eff

    def prediction(self, x_pred):
        """Predizione a un certo x con propagazione errore."""
        if self.popt is None:
            raise RuntimeError("Fit non ancora eseguito.")
        y_pred = self.ff(x_pred, *self.popt)
        # Jacobiano rispetto ai parametri (lineare: [x, 1])
        J = np.array([x_pred, 1.0])
        var_y = J @ self.covm @ J.T
        sigma_y = np.sqrt(var_y)
        print(f"\nPrevisione per x' = {x_pred}:")
        print(f"  y' = {y_pred:.4f} ± {sigma_y:.4f}")
        return y_pred, sigma_y


# ---------------- MAIN ----------------

if __name__ == "__main__":

    directory = '/home/gea/Desktop/notebooks/Notebooks/Year_2/Lab_2/Esperienza_0/'
    filename = 'data00.txt'
    labelx=  r'$\Delta V$ [V]'
    labely = "I [mA]"
    def ff(x, a, b): return a*x + b

    exp = Experiment.from_file(directory+filename, labelx, labely, ff)

    init = (2.1, 0.0)
    exp.fit(init, plot=False)
    exp.correlation_matrix()
    exp.effective_fit(init)
    exp.residuals_plot()
    exp.prediction(20.0)
