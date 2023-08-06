import numpy as np
from .constantes import *
#Eq 41
c_matrix = np.array([[0.81096, 1.7888, -37.578, 92.284],
                    [1.0205, -19.341, 151.26, -463.5],
                    [-1.9057, 22.845, -228.14, 973.92],
                    [1.0885, -6.1962, 106.98, -677.64]])

lam_exp = np.array([0, -1, -2, -3])
def c_ctes(lam):
    c_cte = np.matmul(c_matrix, np.power(lam, lam_exp))
    return c_cte

#Eq 28
def I_lam(x0, lam):
    lam3 = 3. - lam
    I = (x0**lam3 - 1.) / lam3
    return I

#Eq 29
def J_lam(x0, lam):
    lam3 = 3. -lam
    lam4 = 4. - lam
    J = (lam3*x0**lam4  - lam4*x0**lam3 + 1.)/ (lam3 * lam4)
    return J


#Derivadas respecto a eta
#Eq 16
def kHS(eta):
    num = (1-eta)**4
    den = 1 +4*eta+4*eta**2-4*eta**3 + eta**4
    return num/den

def dkHS(eta):
    den = 1 +4*eta+4*eta**2-4*eta**3 + eta**4
    num1 = (1-eta)**4
    num2 = -4*(-1 + eta)**3*(-2 + (-5 + eta)*eta)
    
    khs = num1/den 
    dkhs = num2/den**2
    
    return  khs, dkhs 

def d2kHS(eta):
    den = 1 +4*eta+4*eta**2-4*eta**3 + eta**4
    num1 = (1-eta)**4
    num2 = -4*(-1 + eta)**3*(-2 + (-5 + eta)*eta)
    
    num3 = 4*(-1 + eta)**2*(17 + eta*(82 + eta*(39 +
            eta*(-80 + eta*(77 + 3*(-10 + eta)*eta)))))
    khs = num1/den 
    dkhs = num2/den**2
    d2khs = num3/den**3
    return  khs, dkhs,d2khs 

def d3kHS(eta):
    den = 1 +4*eta+4*eta**2-4*eta**3 + eta**4
    
    num1 = (1-eta)**4
    num2 = -4*(-1 + eta)**3*(-2 + (-5 + eta)*eta)
    
    num3 = 4*(-1 + eta)**2*(17 + eta*(82 + eta*(39 +
            eta*(-80 + eta*(77 + 3*(-10 + eta)*eta)))))
    
    num4 = -624 - 4032 * eta - 576 * eta**2 + 16656 * eta**3 - 11424 * eta**4 
    num4 +=     -16896 * eta**5 + 34752 * eta**6 - 27936 * eta**7 + 13776 * eta ** 8
    num4 +=    - 4416 * eta**9 + 768 * eta**10 - 48 * eta**11
    khs = num1/den 
    dkhs = num2/den**2
    d2khs = num3/den**3
    d3khs = num4/den**4
    return   khs, dkhs,d2khs , d3khs


#Derivadas respecto a eta
#Eq 40
def eta_eff(eta, lam):
    eta_vec = np.array([eta, eta**2, eta**3, eta**4])
    ci = c_ctes(lam)
    neff = np.dot(ci, eta_vec)
    return neff


def deta_eff(eta, lam):
    eta_vec = np.array([eta, eta**2, eta**3, eta**4])
    ci = c_ctes(lam)
    neff = np.dot(ci, eta_vec)
    
    deta_vec = np.array([1, 2*eta, 3*eta**2, 4*eta**3])
    dneff = np.dot(ci, deta_vec)

    return neff, dneff


def d2eta_eff(eta, lam):
    eta_vec = np.array([eta, eta**2, eta**3, eta**4])
    ci = c_ctes(lam)
    neff = np.dot(ci, eta_vec)
    
    deta_vec = np.array([1, 2*eta, 3*eta**2, 4*eta**3])
    dneff = np.dot(ci, deta_vec)
    
    d2eta_vec = np.array([0., 2., 6.*eta, 12.*eta**2])
    d2neff = np.dot(ci, d2eta_vec)

    return neff, dneff, d2neff

def d3eta_eff(eta, lam):
    eta_vec = np.array([eta, eta**2, eta**3, eta**4])
    ci = c_ctes(lam)
    neff = np.dot(ci, eta_vec)
    
    deta_vec = np.array([1, 2*eta, 3*eta**2, 4*eta**3])
    dneff = np.dot(ci, deta_vec)
    
    d2eta_vec = np.array([0, 2, 6.*eta, 12.*eta**2])
    d2neff = np.dot(ci, d2eta_vec)

    d3eta_vec = np.array([0, 0, 6, 24.*eta])
    d3neff = np.dot(ci, d3eta_vec)
    
    return neff, dneff, d2neff, d3neff


#Second perturbation
phi16 = np.array([[7.5365557, -37.60463, 71.745953, -46.83552, -2.467982, -0.50272, 8.0956883],
[-359.44, 1825.6, -3168.0, 1884.2, -0.82376, -3.1935, 3.7090],
[1550.9, -5070.1, 6534.6, -3288.7, -2.7171, 2.0883, 0],
[-1.19932, 9.063632, -17.9482, 11.34027, 20.52142, -56.6377, 40.53683],
[-1911.28, 21390.175, -51320.7, 37064.54, 1103.742, -3264.61, 2556.181],
[9236.9, -129430., 357230., -315530., 1390.2, -4518.2, 4241.6]])
phi7 = np.array([10., 10., 0.57, -6.7, -8])

nfi = np.arange(0,7)
nfi_num = nfi[:4]
nfi_den = nfi[4:]
#Eq 20
def fi(alpha, i):
    phi = phi16[i-1]
    num = np.dot(phi[nfi_num], np.power(alpha, nfi_num))
    den = 1 + np.dot(phi[nfi_den], np.power(alpha, nfi_den - 3))
    return num/den

alpha = c*(1/(lambda_a - 3) - 1/(lambda_r - 3))
f1, f2, f3, f4, f5, f6 = fi(alpha, 1), fi(alpha, 2), fi(alpha, 3), fi(alpha, 4), fi(alpha, 5), fi(alpha, 6)

#Eq 17
def Xi(x0, eta):
    etasigma = eta*x0**3
    x = f1*etasigma + f2*etasigma**5 + f3*etasigma**8
    return x

def dXi(x0, eta):
    x03 = x0**3
    etasigma = eta*x03
    x = f1*etasigma + f2*etasigma**5 + f3*etasigma**8
    dx = x03*(f1 + 5* f2 * etasigma**4 + 8*f3*etasigma**7)
    return x, dx

def d2Xi(x0, eta):
    x03 = x0**3
    etasigma = eta*x03
    x = f1*etasigma + f2*etasigma**5 + f3*etasigma**8
    dx = x03*(f1 + 5* f2 * etasigma**4 + 8*f3*etasigma**7)
    d2x = x03**2*(20.* f2 * etasigma**3 + 56.*f3*etasigma**6)
    return x, dx, d2x
