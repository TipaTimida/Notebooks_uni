import pylab
import numpy
from scipy.optimize import curve_fit

Directory='/home/gea/Desktop/notebooks/Notebooks/Year_2/Lab_2/easy_fit/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
x,Dx,y,Dy=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

# scatter plot with error bars
pylab.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('Delta V  [V]',fontsize=18)
pylab.ylabel('I  [mA]',fontsize=18)
pylab.minorticks_on()

# ----------RICORDA BILOG
pylab.xscale('log')   # if exponential in semi-log, DO NOT PUT THIS LINE
pylab.yscale('log')


# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())
# make the array with initial values (to be carefully adjusted!)
init=(-10, 10)

# set the error (to be modified if effective errors have to be accounted for)
sigma=Dy
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(x, a, b):
    return a/(b+x)

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,x,y,init,sigma,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option

# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*(y-ff(x,*pars))**2)).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print(pars)
print(covm)
print (kappa2, ndof)


# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(x),max(x),500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx,ff(xx,*pars), color='red')

# show the plot
pylab.show()