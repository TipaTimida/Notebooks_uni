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

        # Results of fit
        self.popt = None
        self.perr = None
        self.kappa2 = None
        self.ndof = None
        self.covm = None

    # ------------------ CONSTRUCTORSs ------------------

    @classmethod
    def from_file(cls, path, xlabel, ylabel, ff):
        """Load experiment from a text file with 4 columns."""
        x, Dx, y, Dy = np.loadtxt(path, unpack=True)
        # Shift time so first sample is at t=0
        x -= x[0]
        return cls(x, Dx, y, Dy, xlabel, ylabel, ff)

    @classmethod
    def setup_carica(cls, directory):
        filename = "RC_carica.txt"
        x_label = r"t [$\mu$s]"
        y_label = r"$\Delta V$ [V]"
        def ff(t, Vinf, tau):
            return Vinf * (1 - np.exp(-t/tau))
        return cls.from_file(directory + filename, x_label, y_label, ff)

    @classmethod
    def setup_scarica(cls, directory):
        filename = "RC_scarica.txt"
        x_label = r"t [$\mu$s]"
        y_label = r"$\Delta V$ [V]"
        def ff(t, V0, tau):
            return V0 * np.exp(-t/tau)
        return cls.from_file(directory + filename, x_label, y_label, ff)

    @classmethod
    def setup_oscillazioni(cls, directory):
        filename = "osc.txt"
        x_label = r"t [µs]"
        y_label = r"ΔV [digit]"
        def ff(t, A, tau, omega, phi, B):
            return A * np.exp(-t/tau) * np.cos(omega*t + phi) + B
        return cls.from_file(directory + filename, x_label, y_label, ff)

    # ------------------ PLOTTING METHODS ------------------

    def plot_data(self):
        """Plot experimental data with error bars."""
        plt.rc('font', size=16)
        plt.xlabel(self.xlabel, fontsize=18)
        plt.ylabel(self.ylabel, fontsize=18)
        plt.minorticks_on()
        plt.errorbar(self.x, self.y, self.Dy, self.Dx,
                     linestyle='', color='black', marker='.')
        return

    def plot_model(self, params, color="red"):
        """Overlay model curve with given parameters."""
        self.plot_data()
        xx = np.linspace(min(self.x), max(self.x), 500)
        plt.plot(xx, self.ff(xx, *params), color=color)
        plt.show()

    # ------------------ FITTING ------------------

    def fit(self, init, plot=True, save=False):
        """Fit data with curve_fit and store results."""
        sigma = self.Dy
        w = 1 / sigma**2

        popt, covm = curve_fit(self.ff, self.x, self.y, init, sigma, absolute_sigma=False)
        residuals = self.y - self.ff(self.x, *popt)
        kappa2 = ((w * residuals**2)).sum()
        ndof = len(self.x) - len(init)
        perr = np.sqrt(np.diag(covm))

        # Save results
        self.popt, self.perr, self.kappa2, self.ndof, self.covm = popt, perr, kappa2, ndof, covm

        self.print_results()

        if plot:
            self.plot_model(popt)

        if save:
            plt.savefig("fit.png")

        return popt, perr

    def print_results(self):
        """Print fit results nicely."""
        print("Fit results")
        print("-----------")
        if self.popt is not None:
            for i, (p, e) in enumerate(zip(self.popt, self.perr), start=1):
                print(f"p{i} = {p:.4f} ± {e:.4f}")
            print(f"\nKappa² = {self.kappa2:.3f}")
            print(f"ndof   = {self.ndof}")
        else:
            print("No fit performed yet.")


# ------------------ MAIN SCRIPT ------------------

if __name__ == "__main__":
    directory = "/home/gea/Desktop/notebooks/Notebooks/Year_2/Lab_2/Esperienza_0/"

    # Choose setup
    exp = Experiment.setup_scarica(directory)

    # Initial guess
    '''
    A0 = (np.max(exp.y) - np.min(exp.y)) / 2
    tau0 = 14000.0
    omega0 = 0.0045
    phi0 = np.pi / 2
    B0 = np.mean(exp.y)
    init = (A0, tau0, omega0, phi0, B0)
    '''

    # Carica - Vinf ~ max tensione, tau ~ 50 µs
    # init = (max(exp.y), 1500)      # guess carica: Vinf ~ max tensione, tau ~ 50 µs
    
    # Scarica - Vinf ~ max tensione, tau ~ 50 µs
    init = (exp.y[0], 1500)      # guess scarica: Vinf ~ max tensione, tau ~ 50 µs

    # exp.plot_model(init)

    exp.fit(init)