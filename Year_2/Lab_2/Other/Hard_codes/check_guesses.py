import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Your damped oscillator model
def osc(t, A, tau, omega, phi, B):
    return A * np.exp(-t/tau) * np.cos(omega*t + phi) + B

# Example synthetic data (replace with your x,y,Dy)
x = np.linspace(0, 50000, 200)
y = 5 * np.exp(-x/15000) * np.cos(0.0045*x + np.pi/2) + 0.3*np.random.randn(len(x))
Dy = 0.3*np.ones_like(x)

# Initial guesses
A0 = (np.max(y)-np.min(y))/2
tau0 = 14000.0
omega0 = 0.0045
phi0 = np.pi/2
B0 = np.mean(y)

# Create figure and axis
fig, ax = plt.subplots(figsize=(8,5))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Plot data
ax.errorbar(x, y, yerr=Dy, fmt='o', ms=3, alpha=0.6, label="Data")

# Plot initial model
xx = np.linspace(min(x), max(x), 500)
[line] = ax.plot(xx, osc(xx, A0, tau0, omega0, phi0, B0), 'r-', lw=2, label="Guess")
ax.legend()
ax.grid(True)

# Define slider axes
axcolor = 'lightgoldenrodyellow'
ax_A     = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_tau   = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_omega = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_phi   = plt.axes([0.1, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_B     = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)

# Create sliders
s_A     = Slider(ax_A,     'A',     0, 10,    valinit=A0)
s_tau   = Slider(ax_tau,   'tau',   1000, 50000, valinit=tau0)
s_omega = Slider(ax_omega, 'omega', 0.0005, 0.01, valinit=omega0)
s_phi   = Slider(ax_phi,   'phi',   0, 2*np.pi, valinit=phi0)
s_B     = Slider(ax_B,     'B',    -5, 5,    valinit=B0)

# Update function
def update(val):
    line.set_ydata(osc(xx, s_A.val, s_tau.val, s_omega.val, s_phi.val, s_B.val))
    fig.canvas.draw_idle()

# Connect sliders to update function
s_A.on_changed(update)
s_tau.on_changed(update)
s_omega.on_changed(update)
s_phi.on_changed(update)
s_B.on_changed(update)

plt.show()
