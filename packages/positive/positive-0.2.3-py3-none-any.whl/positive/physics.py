#
from __future__ import print_function
from positive import *
from positive.plotting import *
from positive.learning import *

#
def rISCO_14067295(a):
    """
    Calculate the ISCO radius of a Kerr BH as a function of the Kerr parameter using eqns. 2.5 and 2.8 from Ori and Thorne, Phys Rev D 62, 24022 (2000)

    Parameters
    ----------
    a : Kerr parameter

    Returns
    -------
    ISCO radius
    """

    import numpy as np
    a = np.array(a)

    # Ref. Eq. (2.5) of Ori, Thorne Phys Rev D 62 124022 (2000)
    z1 = 1.0+(1.0-a**2.0)**(1.0/3)*((1.0+a)**(1.0/3) + (1.0-a)**(1.0/3))
    z2 = np.sqrt(3 * a**2 + z1**2)
    a_sign = np.sign(a)
    return 3+z2 - np.sqrt((3.0-z1)*(3.0+z1+2.0*z2))*a_sign


# Calculate Kerr ISCO Radius
def rKerr_ISCO_Bardeen(j,M=1):
    '''

    Calculate Kerr ISCO Radius

    USAGE:
    rKerr_ISCO_Bardeen(Dimensionless_BH_Spin,BH_Mass)

    ~ londonl@mit.edu

    '''

    #
    from numpy import sign,sqrt

    #
    a = M*j

    #
    p13 = 1.0/3
    jj = j*j

    #
    Z1 = 1 + ( 1-jj )**p13 * ( (1+j)**p13 + (1-j)**p13 )
    Z2 = sqrt( 3*jj + Z1*Z1 )

    #
    rKerr_ISCO = M * (  3 + Z2 - sign(j) * sqrt( (3-Z1)*(3+Z1+2*Z2) )  )

    #
    return rKerr_ISCO


# Calculate Kerr ISCO Angular Frequency
def wKerr_ISCO_Bardeen(j,M=1):
    '''

    Calculate Kerr ISCO Angular Frequency

    USAGE:
    wKerr_ISCO_Bardeen(Dimensionless_BH_Spin,BH_Mass=1)

    ~ londonl@mit.edu

    '''

    #
    from numpy import sin,sign,sqrt

    #
    a = M*j

    # Bardeen et al 2.21, Ori Thorn 2.5
    r = M * rKerr_ISCO_Bardeen(j,M=M) # rISCO_14067295(j)

    # 2.16 of Bardeen et al, ( 2.1 of Ori Thorn misses physics )
    wKerr_ISCO = sqrt(M) / ( r**(3.0/2) + a*sqrt(M) )

    # Return Answer
    return wKerr_ISCO


# Calculate Kerr Light-Ring Radius
def rKerr_LR_Bardeen(j,M=1,branch=0):
    '''

    Calculate Kerr Light-Ring Radius

    USAGE:
    rKerr_LR_Bardeen(Dimensionless_BH_Spin,BH_Mass)

    ~ londonl@mit.edu

    '''

    #
    from numpy import cos,arccos,sqrt
    from positive import acos

    # Bardeen et al 2.18
    rKerr_LR = 2*M*(   1 + cos( (2.0/3)*acos(-j,branch=branch) )   )
    # rKerr_LR = 2*M*(   1 + cos( (2.0/3)*arccos(-j) )   )

    #
    return rKerr_LR


# Calculate Kerr ISCO Angular Frequency
def wKerr_LR_Bardeen(j,M=1,branch=0):
    '''

    Calculate Kerr Light-Ring (aka PH for Photon) Angular Frequency

    USAGE:
    wKerr_LR_Bardeen(Dimensionless_BH_Spin,BH_Mass=1)

    ~ londonl@mit.edu

    '''

    #
    from numpy import sin,sign,sqrt

    #
    a = M*j

    # Bardeen et al 2.18
    r = M * rKerr_LR_Bardeen(j,M=M,branch=branch)

    # 2.16 of Bardeen et al
    wKerr_LR = sqrt(M) / ( r**(3.0/2) + a*sqrt(M) )

    # Return Answer
    return wKerr_LR


# https://arxiv.org/pdf/1406.7295.pdf
def Mf14067295( m1,m2,chi1,chi2,chif=None ):

    import numpy as np

    if np.any(abs(chi1>1)):
      raise ValueError("chi1 has to be in [-1, 1]")
    if np.any(abs(chi2>1)):
      raise ValueError("chi2 has to be in [-1, 1]")


    # Swapping inputs to conform to fit conventions
    # NOTE: See page 2 of https://arxiv.org/pdf/1406.7295.pdf
    m2,m1,chi1,chi2 = mass_ratio_convention_sort(m2,m1,chi1,chi2)
    # if m1>m2:
    #     #
    #     m1_,m2_ = m1,m2
    #     chi1_,chi2_ = chi1,chi2
    #     #
    #     m1,m2 = m2_,m1_
    #     chi1,chi2 = chi2_,chi1_

    # binary parameters
    m = m1+m2
    q = m1/m2
    eta = q/(1.+q)**2.
    delta_m = (m1-m2)/m
    S1 = chi1*m1**2 # spin angular momentum 1
    S2 = chi2*m2**2 # spin angular momentum 2
    S = (S1+S2)/m**2 # symmetric spin (dimensionless -- called \tilde{S} in the paper)
    Delta = (S2/m2-S1/m1)/m # antisymmetric spin (dimensionless -- called tilde{Delta} in the paper

    #
    if chif is None:
        chif = jf14067295(m1, m2, chi1, chi2)
    r_isco = rISCO_14067295(chif)

    # fitting coefficients - Table XI of Healy et al Phys Rev D 90, 104004 (2014)
    # [fourth order fits]
    M0  = 0.951507
    K1  = -0.051379
    K2a = -0.004804
    K2b = -0.054522
    K2c = -0.000022
    K2d = 1.995246
    K3a = 0.007064
    K3b = -0.017599
    K3c = -0.119175
    K3d = 0.025000
    K4a = -0.068981
    K4b = -0.011383
    K4c = -0.002284
    K4d = -0.165658
    K4e = 0.019403
    K4f = 2.980990
    K4g = 0.020250
    K4h = -0.004091
    K4i = 0.078441

    # binding energy at ISCO -- Eq.(2.7) of Ori, Thorne Phys Rev D 62 124022 (2000)
    E_isco = (1. - 2./r_isco + chif/r_isco**1.5)/np.sqrt(1. - 3./r_isco + 2.*chif/r_isco**1.5)

    # final mass -- Eq. (14) of Healy et al Phys Rev D 90, 104004 (2014)
    mf = (4.*eta)**2*(M0 + K1*S + K2a*Delta*delta_m + K2b*S**2 + K2c*Delta**2 + K2d*delta_m**2 \
        + K3a*Delta*S*delta_m + K3b*S*Delta**2 + K3c*S**3 + K3d*S*delta_m**2 \
        + K4a*Delta*S**2*delta_m + K4b*Delta**3*delta_m + K4c*Delta**4 + K4d*S**4 \
        + K4e*Delta**2*S**2 + K4f*delta_m**4 + K4g*Delta*delta_m**3 + K4h*Delta**2*delta_m**2 \
        + K4i*S**2*delta_m**2) + (1+eta*(E_isco+11.))*delta_m**6.

    return mf*m

#
def jf14067295_diff(a_f,eta,delta_m,S,Delta):
    """ Internal function: the final spin is determined by minimizing this function """

    #
    import numpy as np

    # calculate ISCO radius
    r_isco = rISCO_14067295(a_f)

    # angular momentum at ISCO -- Eq.(2.8) of Ori, Thorne Phys Rev D 62 124022 (2000)
    J_isco = (3*np.sqrt(r_isco)-2*a_f)*2./np.sqrt(3*r_isco)

    # fitting coefficients - Table XI of Healy et al Phys Rev D 90, 104004 (2014)
    # [fourth order fits]
    L0  = 0.686710
    L1  = 0.613247
    L2a = -0.145427
    L2b = -0.115689
    L2c = -0.005254
    L2d = 0.801838
    L3a = -0.073839
    L3b = 0.004759
    L3c = -0.078377
    L3d = 1.585809
    L4a = -0.003050
    L4b = -0.002968
    L4c = 0.004364
    L4d = -0.047204
    L4e = -0.053099
    L4f = 0.953458
    L4g = -0.067998
    L4h = 0.001629
    L4i = -0.066693

    a_f_new = (4.*eta)**2.*(L0  +  L1*S +  L2a*Delta*delta_m + L2b*S**2. + L2c*Delta**2 \
        + L2d*delta_m**2. + L3a*Delta*S*delta_m + L3b*S*Delta**2. + L3c*S**3. \
        + L3d*S*delta_m**2. + L4a*Delta*S**2*delta_m + L4b*Delta**3.*delta_m \
        + L4c*Delta**4. + L4d*S**4. + L4e*Delta**2.*S**2. + L4f*delta_m**4 + L4g*Delta*delta_m**3. \
        + L4h*Delta**2.*delta_m**2. + L4i*S**2.*delta_m**2.) \
        + S*(1. + 8.*eta)*delta_m**4. + eta*J_isco*delta_m**6.

    daf = a_f-a_f_new
    return daf*daf

#
def jf14067295(m1, m2, chi1, chi2):
    """
    Calculate the spin of the final BH resulting from the merger of two black holes with non-precessing spins using fit from Healy et al Phys Rev D 90, 104004 (2014)

    Parameters
    ----------
    m1, m2 : component masses
    chi1, chi2 : dimensionless spins of two BHs

    Returns
    -------
    dimensionless final spin, chif
    """
    import numpy as np
    import scipy.optimize as so

    if np.any(abs(chi1>1)):
      raise ValueError("chi1 has to be in [-1, 1]")
    if np.any(abs(chi2>1)):
      raise ValueError("chi2 has to be in [-1, 1]")

    # Vectorize the function if arrays are provided as input
    if np.size(m1) * np.size(m2) * np.size(chi1) * np.size(chi2) > 1:
        return np.vectorize(bbh_final_spin_non_precessing_Healyetal)(m1, m2, chi1, chi2)

    # binary parameters
    m = m1+m2
    q = m1/m2
    eta = q/(1.+q)**2.
    delta_m = (m1-m2)/m

    S1 = chi1*m1**2 # spin angular momentum 1
    S2 = chi2*m2**2 # spin angular momentum 2
    S = (S1+S2)/m**2 # symmetric spin (dimensionless -- called \tilde{S} in the paper)
    Delta = (S2/m2-S1/m1)/m # antisymmetric spin (dimensionless -- called tilde{Delta} in the paper

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # compute the final spin
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    x, cov_x = so.leastsq(jf14067295_diff, 0., args=(eta, delta_m, S, Delta))
    chif = x[0]

    return chif

# Energy Radiated
# https://arxiv.org/abs/1611.00332
# Xisco Jimenez-Forteza, David Keitel, Sascha Husa, Mark Hannam, Sebastian Khan, Michael Purrer
def Erad161100332(m1,m2,chi1,chi2):
    '''
    Final mass fit from: https://arxiv.org/abs/1611.00332
    By Xisco Jimenez-Forteza, David Keitel, Sascha Husa, Mark Hannam, Sebastian Khan, Michael Purrer
    '''
    # Import usefuls
    from numpy import sqrt
    # Test for m1>m2 convention
    m1,m2,chi1,chi2 = mass_ratio_convention_sort(m1,m2,chi1,chi2)
    # if m1<m2:
    #     # Swap everything
    #     m1_,m2_ = m2 ,m1 ;  chi1_,chi2_ =  chi2,chi1
    #     m1,m2   = m1_,m2_;  chi1,chi2   = chi1_,chi2_
    #
    M = m1+m2
    eta = m1*m2/(M*M)
    # Caclulate effective spin
    S = (chi1*m1 + chi2*m2) / M
    # Calculate fitting formula
    E = -0.12282038851475935*(chi1 - chi2)*(1 - 4*eta)**0.5*(1 - 3.499874117528558*eta)*eta**2 +\
        0.014200036099065607*(chi1 - chi2)**2*eta**3 - 0.018737203870440332*(chi1 - chi2)*(1 -\
        5.1830734412467425*eta)*(1 - 4*eta)**0.5*eta*S + (((1 - (2*sqrt(2))/3.)*eta +\
        0.5635376058169301*eta**2 - 0.8661680065959905*eta**3 + 3.181941595301784*eta**4)*(1 +\
        (-0.13084395473958504 - 1.1075070900466686*eta + 5.292389861792881*eta**2)*S + \
        (-0.17762804636455634 + 2.095538044244076*eta**2)*S**2 + (-0.6320190570187046 + \
        5.645908914996172*eta - 12.860272122009997*eta**2)*S**3))/(1 + (-0.9919475320287884 +\
        0.5383449788171806*eta + 3.497637161730149*eta**2)*S)
    # Return answer
    return E

# Remnant mass
# https://arxiv.org/abs/1611.00332
# Xisco Jimenez-Forteza, David Keitel, Sascha Husa, Mark Hannam, Sebastian Khan, Michael Purrer
def Mf161100332(m1,m2,chi1,chi2):
    return m1+m2-Erad161100332(m1,m2,chi1,chi2)

# Remnant Spin
# https://arxiv.org/abs/1611.00332
# Xisco Jimenez-Forteza, David Keitel, Sascha Husa, Mark Hannam, Sebastian Khan, Michael Purrer
def jf161100332(m1,m2,chi1,chi2):
    '''
    Final mass fit from: https://arxiv.org/abs/1611.00332
    By Xisco Jimenez-Forteza, David Keitel, Sascha Husa, Mark Hannam, Sebastian Khan, Michael Purrer
    '''
    # Import usefuls
    from numpy import sqrt
    # Test for m1>m2 convention
    m1,m2,chi1,chi2 = mass_ratio_convention_sort(m1,m2,chi1,chi2)
    # if m1<m2:
    #     # Swap everything
    #     m1_,m2_ = m2 ,m1 ;  chi1_,chi2_ =  chi2,chi1
    #     m1,m2   = m1_,m2_;  chi1,chi2   = chi1_,chi2_
    #
    M = m1+m2
    eta = m1*m2/(M*M)
    # Caclulate effective spin
    S = (chi1*m1 + chi2*m2) / M
    # Calculate fitting formula
    jf = -0.05975750218477118*(chi1 - chi2)**2*eta**3 + 0.2762804043166152*(chi1 - chi2)*(1 -\
         4*eta)**0.5*eta**2*(1 + 11.56198469592321*eta) + (2*sqrt(3)*eta + 19.918074038061683*eta**2 -\
         12.22732181584642*eta**3)/(1 + 7.18860345017744*eta) + chi1*m1**2 + chi2*m2**2 +\
         2.7296903488918436*(chi1 - chi2)*(1 - 4*eta)**0.5*(1 - 3.388285154747212*eta)*eta**3*S + ((0. -\
         0.8561951311936387*eta - 0.07069570626523915*eta**2 + 1.5593312504283474*eta**3)*S + (0. +\
         0.5881660365859452*eta - 2.670431392084654*eta**2 + 5.506319841591054*eta**3)*S**2 + (0. +\
         0.14244324510486703*eta - 1.0643244353754102*eta**2 + 2.3592117077532433*eta**3)*S**3)/(1 +\
         (-0.9142232696116447 + 2.6764257152659883*eta - 15.137168414785732*eta**3)*S)
    # Return answer
    return jf


# Remnant Spin
# https://arxiv.org/abs/1605.01938
# Fabian Hofmann, Enrico Barausse, Luciano Rezzolla
def jf160501938(m1,m2,chi1_vec,chi2_vec,L_vec=None):

    '''
    Remnant Spin
    https://arxiv.org/abs/1605.01938
    Fabian Hofmann, Enrico Barausse, Luciano Rezzolla
    '''

    # Import usefuls
    from numpy import sqrt,dot,array,cos,tan,arccos,arctan,zeros,sign
    from numpy.linalg import norm

    # Handle inputs
    if L_vec is None:
        warning('No initial orbital angular momentum vevtor given. We will assume it is z-ligned.')
        L_vec = array([0,0,1])
    #
    m1 = float(m1); m2 = float(m2)

    # Table 1 (numbers copied from arxiv tex file: https://arxiv.org/format/1605.01938)

    # # bottom block -- doesnt work
    # n_M = 3; n_J = 4
    # k = zeros( (n_M+1,n_J+1) )
    # k[0,1] = 3.39221;   k[0,2] = 4.48865;  k[0,3] = -5.77101
    # k[0,4] = -13.0459;  k[1,0] = 35.1278;  k[1,1] = -72.9336
    # k[1,2] = -86.0036;  k[1,3] = 93.7371;  k[1,4] = 200.975
    # k[2,0] = -146.822;  k[2,1] = 387.184;  k[2,2] = 447.009
    # k[2,3] = -467.383;  k[2,4] = -884.339; k[3,0] = 223.911
    # k[3,1] = -648.502;  k[3,2] = -697.177; k[3,3] = 753.738
    # k[3,4] = 1166.89;   xi = 0.474046
    # k[0,0] = -3.82

    # top block -- works
    n_M = 1; n_J = 2
    k = zeros( (n_M+1,n_J+1) )
    k[0,1] = -1.2019; k[0,2] = -1.20764; k[1,0] = 3.79245; k[1,1] = 1.18385
    k[1,2] = 4.90494; xi = 0.41616
    k[0,0] = -3.82

    # Eq. 5
    p = 1.0/3
    Z1 = lambda a: 1 + (1-a*a)**p * (  (1+a)**p + (1-a)**p  )

    # Eq. 6
    Z2 = lambda a: sqrt( 3*a*a + Z1(a)**2 )

    # Eq. 4
    r_ISCO = lambda a: 3.0 + Z2(a) - sign(a) * sqrt( (3-Z1(a))*(3+Z1(a)+2*Z2(a)) )
    # r_ISCO = lambda a: 3.0 + Z2(a) - ( a / abs(a) ) * sqrt( (3-Z1(a))*(3+Z1(a)+2*Z2(a)) )

    # Eq. 2
    E_ISCO = lambda a: sqrt( 1 - 2.0 / ( 3 * r_ISCO(a) ) )

    # Eq. 3
    p = 0.38490017945975052 # this is 2.0 / (3*sqrt(3))
    L_ISCO = lambda a: p * (  1 + 2*sqrt( 3*r_ISCO(a)-2 )  )

    ## Amplitude of final spin

    # Define low level physical parameters
    L_hat = L_vec / norm(L_vec)
    a1z = dot(L_hat,chi1_vec) # chi1_vec[-1]
    a2z = dot(L_hat,chi2_vec) # chi2_vec[-1]
    a1 = norm(chi1_vec)
    a2 = norm(chi2_vec)
    eta = m1*m2 / (m1+m2)**2
    q = m2/m1 if m2<m1 else m1/m2 # convention as seen above Eq 1

    # Eq. 17
    x1 = (chi1_vec / norm(chi1_vec)) if norm(chi1_vec) else zeros(3)
    x2 = (chi2_vec / norm(chi2_vec)) if norm(chi2_vec) else zeros(3)
    __alpha__ = arccos( dot(x1, x2) )
    __beta__  = arccos( dot(L_hat, x1) )
    __gamma__ = arccos( dot(L_hat, x2) )

    # Eq. 18 for alpha
    eps_alpha = 0
    alpha = 2 * arctan( (1+eps_alpha)     *tan(__alpha__/2) )

    # Eq. 18 for beta
    eps_beta_gamma = 0.024
    beta  = 2 * arctan( (1+eps_beta_gamma)*tan( __beta__/2) )

    # Eq. 18 for gamma
    gamma = 2 * arctan( (1+eps_beta_gamma)*tan(__gamma__/2) )

    # alpha = __alpha__
    # beta = __beta__
    # gamma = __gamma__

    # Eq. 14
    a_tot = (  a1*cos(beta) + a2*cos(gamma)*q  ) / (1.0+q)**2
    a_eff = a_tot + xi*eta*( a1z*cos(beta) + a2z*cos(gamma) )

    # Eq. 13 -- Double sum part
    double_sum_part = 0
    for i in range(n_M+1):
        for j in range(n_J+1):
            double_sum_part += (k[i,j] * eta**(1+i) * a_eff ** j) if k[i,j] else 0

    # Eq. 13
    absl = abs( L_ISCO(a_eff) - 2*a_tot*(E_ISCO(a_eff)-1) + double_sum_part )

    # Eq. 16
    afin = (1.0/(1+q)**2) * sqrt(  a1**2 + a2**2 * q**4 + 2*a1*a2*q*q*cos(alpha) + 2*(a1*cos(beta)+a2*q*q*cos(gamma))*absl*q + absl*absl*q*q  )

    #
    # b = dir()
    # for k in b:
    #     print k+'\t=\t',eval(k)
    return afin

# High level function for calculating remant mass and spin
def remnant(m1,m2,chi1,chi2,arxiv=None,verbose=False,L_vec=None):
    '''
    High level function for calculating remant mass and spin for nonprecessing BBH systems.

    Available arxiv ids are:
    * 1611.00332 by Jimenez et. al.
    * 1406.7295 by Healy et. al.

    This function automatically imposes m1,m2 conventions.

    spxll'17
    '''

    #
    if not isinstance(chi1,(float,int)):
        arxiv = '1605.01938'
        warning('spin vectors found; we will use a precessing spin formula from 1605.01938 for the final spin and a non-precessing formula from 1611.00332')

    #
    if arxiv in ('1611.00332',161100332,None):
        if verbose: alert('Using method from arxiv:1611.00332 by Jimenez et. al.')
        Mf = Mf161100332(m1,m2,chi1,chi2)
        jf = jf161100332(m1,m2,chi1,chi2)
    elif arxiv in ('1605.01938',160501938,'precessing','p'):
        Mf = Mf161100332(m1,m2,chi1[-1],chi2[-1])
        jf = jf160501938(m1,m2,chi1,chi2,L_vec=L_vec)
    else:
        if verbose:
            alert('Using method from arxiv:1406.7295 by Healy et. al.')
            warning('This method is slow [af]. Please consider using another one.')
        Mf = Mf14067295(m1,m2,chi1,chi2)
        jf = jf14067295(m1,m2,chi1,chi2)

    # Return answer
    ans = (Mf,jf)
    return ans

#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#
# Post-Newtonian methods
#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#


# PN estimate for orbital frequency
def pnw0(m1,m2,D=10.0):
    # https://arxiv.org/pdf/1310.1528v4.pdf
    # Equation 228
    # 2nd Reference: arxiv:0710.0614v1
    # NOTE: this outputs orbital frequency
    from numpy import sqrt,zeros,pi,array,sum
    #
    G = 1.0
    c = 1.0
    r = float(D)
    M = float( m1+m2 )
    v = m1*m2/( M**2 )
    gamma = G*M/(r*c*c)     # Eqn. 225
    #
    trm = zeros((4,))
    #
    trm[0] = 1.0
    trm[1] = v - 3.0
    trm[2] = 6 + v*41.0/4.0 + v*v
    trm[3] = -10.0 + v*( -75707.0/840.0 + pi*pi*41.0/64.0 ) + 19.0*0.5*v*v + v*v*v
    #
    w0 = sqrt( (G*M/(r*r*r)) * sum( array([ term*(gamma**k) for k,term in enumerate(trm) ]) ) )

    #
    return w0


#
def mishra( f, m1,m2, X1,X2, lm,    # Intrensic parameters and l,m
            lnhat   = None,         # unit direction of orbital angular momentum
            vmax    = 10,           # maximum power (integer) allwed for V parameter
            leading_order = False,  # Toggle for using only leading order behavior
            verbose = False ):      # toggle for letting the people know
    '''
    PN formulas from "Ready-to-use post-Newtonian gravitational waveforms for binary black holes with non-precessing spins: An update"
    *   https://arxiv.org/pdf/1601.05588.pdf
    *   https://arxiv.org/pdf/0810.5336.pdf
    '''

    # Import usefuls
    from numpy import pi,array,dot,sqrt,log,inf,ones

    # Handle zero values
    f[f==0] = 1e-5 * min(abs(f))

    #
    l,m = lm

    #
    M = m1+m2

    # Normalied mass difference
    delta = (m1-m2)/(m1+m2)

    # Symmetric mass ratio
    eta = float(m1)*m2/(M*M)

    # Frequency parameter (note that this is the same as the paper's \nu)
    V = lambda m: pow(2.0*pi*M*f/m,1.0/3)

    # Here we handle the vmax input using a lambda function
    if vmax is None: vmax = inf
    e = ones(12)        # This identifier will be used to turn off terms
    e[(vmax+1):] = 0    # NOTE that e will effectively be indexed starting
                        # from 1 not 0, so it must have more elements than needed.


    # Handle default behavior for
    lnhat = array([0,0,1]) if lnhat is None else lnhat

    # Symmetric and Anti-symmettric spins
    Xs = 0.5 * ( X1+X2 )
    Xa = 0.5 * ( X1-X2 )

    #
    U = not leading_order

    # Dictionary for FD multipole terms (eq. 12)
    H = {}

    #
    H[2,2] = lambda v: -1 + U*( v**2  * e[2] *  ( (323.0/224.0)-(eta*451.0/168.0) ) \
                          + v**3  * e[3] *  ( -(27.0/8)*delta*dot(Xa,lnhat) + dot(Xs,lnhat)*((-27.0/8)+(eta*11.0/6)) ) \
                          + v**4  * e[4] *  ( (27312085.0/8128512)+(eta*1975055.0/338688) - (105271.0/24192)*eta*eta + dot(Xa,lnhat)**2 * ((113.0/32)-eta*14) + delta*(113.0/16)*dot(Xa,lnhat)*dot(Xs,lnhat) + dot(Xs,lnhat)**2 * ((113.0/32) - (eta/8)) ) )

    #
    H[2,1] = lambda v: -(sqrt(2)/3) * ( v    * delta \
                                      + U*(- v**2 * e[2] * 1.5*( dot(Xa,lnhat)+delta*dot(Xs,lnhat) ) \
                                      + v**3 * e[3] * delta*( (335.0/672)+(eta*117.0/56) ) \
                                      + v**4 * e[4] * ( dot(Xa,lnhat)*(4771.0/1344 - eta*11941.0/336) + delta*dot(Xs,lnhat)*(4771.0/1344 - eta*2549.0/336) + delta*(-1j*0.5-pi-2*1j*log(2)) ) \
                                      ))

    #
    H[3,3] = lambda v: -0.75*sqrt(5.0/7) \
                        *(v           * delta \
                        + U*( v**3 * e[3] * delta * ( -(1945.0/672) + eta*(27.0/8) )\
                        + v**4 * e[4] * ( dot(Xa,lnhat)*( (161.0/24) - eta*(85.0/3) ) + delta*dot(Xs,lnhat)*( (161.0/24) - eta*(17.0/3) ) + delta*(-1j*21.0/5 + pi + 6j*log(3.0/2)) ) \
                        ))

    #
    H[3,2] = lambda v: -(1.0/3)*sqrt(5.0/7) * (\
                        v**2   * e[2] * (1-3*eta) \
                        + U*( v**3 * e[3] * 4*eta*dot(Xs,lnhat) \
                        + v**4 * e[4] * (-10471.0/10080 + eta*12325.0/2016 - eta*eta*589.0/72) \
                        ))

    #
    H[4,4] = lambda v: -(4.0/9)*sqrt(10.0/7) \
                        * ( v**2 * e[2] * (1-3*eta) \
                        +   U*(v**4 * e[4] * (-158383.0/36960 + eta*128221.0/7392 - eta*eta*1063.0/88) \
                        ))

    #
    H[4,3] = lambda v: -(3.0/4)*sqrt(3.0/35) * (
                        v**3 * e[3] * delta*(1-2*eta) \
                        + U*v**4 * e[4] * (5.0/2)*eta*( dot(Xa,lnhat) - delta*dot(Xs,lnhat) )\
                        )

    #
    hlm_amp = M*M*pi * sqrt(eta*2.0/3)*(V(m)**-3.5) * H[l,m]( V(m) )

    #
    return abs(hlm_amp)


# leading order amplitudes in freq fd strain via spa
def lamp_spa(f,eta,lm=(2,2)):
    # freq domain amplitude from leading order in f SPA
    # made using ll-LeadingOrderAmplitudes.nb in PhenomHM repo
    from numpy import pi,sqrt

    #
    warning('This function has a bug related the a MMA bug of unknown origin -- ampliutdes are off by order 1 factors!!')

    # Handle zero values
    f[f==0] = 1e-5 * min(abs(f))

    #
    hf = {}
    #
    hf[2,2] = (sqrt(0.6666666666666666)*sqrt(eta))/(f**1.1666666666666667*pi**0.16666666666666666)
    #
    hf[2,1] = (sqrt(0.6666666666666666)*sqrt(eta - 4*eta**2)*pi**0.16666666666666666)/(3.*f**0.8333333333333334)
    #
    hf[3,3] = (3*sqrt(0.7142857142857143)*sqrt(eta - 4*eta**2)*pi**0.16666666666666666)/(4.*f**0.8333333333333334)
    #
    hf[3,2] = (sqrt(0.47619047619047616)*eta*sqrt(pi))/(3.*sqrt(eta*f)) - (sqrt(0.47619047619047616)*eta**2*sqrt(pi))/sqrt(eta*f)
    #
    hf[3,1] = (sqrt(eta - 4*eta**2)*pi**0.16666666666666666)/(12.*sqrt(21)*f**0.8333333333333334)
    #
    hf[4,4] = (8*sqrt(0.47619047619047616)*eta*sqrt(pi))/(9.*sqrt(eta*f)) - (8*sqrt(0.47619047619047616)*eta**2*sqrt(pi))/(3.*sqrt(eta*f))
    #
    hf[4,3] = (3*sqrt(0.08571428571428572)*sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(4.*f**0.16666666666666666) - (3*sqrt(0.08571428571428572)*eta*sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(2.*f**0.16666666666666666)
    #
    hf[4,2] = (sqrt(3.3333333333333335)*eta*sqrt(pi))/(63.*sqrt(eta*f)) - (sqrt(3.3333333333333335)*eta**2*sqrt(pi))/(21.*sqrt(eta*f))
    #
    hf[4,1] = (sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(84.*sqrt(15)*f**0.16666666666666666) - (eta*sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(42.*sqrt(15)*f**0.16666666666666666)
    #
    hf[5,5] = (625*sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(288.*sqrt(11)*f**0.16666666666666666) - (625*eta*sqrt(eta - 4*eta**2)*pi**0.8333333333333334)/(144.*sqrt(11)*f**0.16666666666666666)
    #
    hf[6,6] = 3.6
    #
    return hf[lm]


# Calculate the Center of Mass Energy for a Binary Source
def pn_com_energy(f,m1,m2,X1,X2,L=None):
    '''
    Calculate the Center of Mass Energy for a Binary Source

    Primary Refernce: https://arxiv.org/pdf/0810.5336.pdf
        * Eq. 6.18, C1-C6
    '''

    # Import usefuls
    from numpy import pi,array,dot,ndarray,sqrt

    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Validate inputs
    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    if L is None: L = array([0,0,1.0])
    # Handle Spin 1
    if not isinstance(X1,ndarray):
        error('X1 input must be array')
    elif len(X1)<3:
        error('X1 must be array of length 3; the length is %i'%len(X1))
    else:
        X1 = array(X1)
    # Handle Xpin 2
    if not isinstance(X2,ndarray):
        error('X2 input must be array')
    elif len(X2)<3:
        error('X2 must be array of length 3; the length is %i'%len(X2))
    else:
        X2 = array(X2)

    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Define low level parameters
    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

    # Total mass
    M = m1+m2
    # Symmetric Mass ratio
    eta = m1*m2 / (M**2)
    delta = sqrt(1-4*eta)
    #
    Xs = 0.5 * ( X1+X2 )
    Xa = 0.5 * ( X1-X2 )
    #
    xs = dot(Xs,L)
    xa = dot(Xa,L)
    # PN frequency parameter
    v = ( 2*pi*M*f ) ** 1.0/3
    #
    Enewt = - 0.5 * M * eta

    # List term coefficients
    e2 = - 0.75 - (1.0/12)*eta
    e3 = (8.0/3 - 4.0/3*eta) * xs + (8.0/3)*delta*xa
    e4 = -27.0/8 + 19.0/8*eta - eta*eta/24 \
         + eta* ( (dot(Xs,Xs)-dot(Xa,Xa))-3*(xs*xs-xa*xa) ) \
         + (0.5-eta)*( dot(Xs,Xs)+dot(Xa,Xa)-3*(xs*xs+xa*xa) ) \
         + delta*( dot(Xs,Xa)-3*( xs*xa ) )
    e5 = xs*(8-eta*121.0/9 + eta*eta*2.0/9) + delta*xa*(8-eta*31.0/9)
    e6 = -675.0/64 + (34445.0/576 - pi*pi*205.0/96)*eta - eta*eta*155.0/96 - 35.0*eta*eta*eta/5184
    e = [e2,e3,e4,e5,e6]

    #
    E = Enewt * v * v * ( 1.0 + sum( [ ek*(v**(k+2)) for k,ek in enumerate(e) ] ) )

    #
    ans = E
    return ans


# Calculate the Center of Mass Energy for a Binary Source
def pn_com_energy_flux(f,m1,m2,X1,X2,L=None):
    '''
    Calculate the Energy Flux for a Binary Source

    Primary Refernce: https://arxiv.org/pdf/0810.5336.pdf
        * Eq. 6.19, C7-C13
    '''

    # Import usefuls
    from numpy import pi,pow,array,dot,ndarray,log

    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Validate inputs
    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    if L is None: L = array([0,0,1.0])
    # Handle Spin 1
    if not isinstance(X1,ndarray):
        error('X1 input must be array')
    elif len(X1)<3:
        error('X1 must be array of length 3; the length is %i'%len(X1))
    else:
        X1 = array(X1)
    # Handle Xpin 2
    if not isinstance(X2,ndarray):
        error('X2 input must be array')
    elif len(X2)<3:
        error('X2 must be array of length 3; the length is %i'%len(X2))
    else:
        X2 = array(X2)

    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
    # Define low level parameters
    #~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

    # Total mass
    M = m1+m2
    # Symmetric Mass ratio
    eta = m1*m2 / (M**2)
    delta = sqrt(1-4*eta)
    #
    Xs = 0.5 * ( X1+X2 )
    Xa = 0.5 * ( X1-X2 )
    #
    xs = dot(Xs,L)
    xa = dot(Xa,L)
    # PN frequency parameter
    v = ( 2*pi*M*f ) ** (1.0/3)
    #
    Fnewt = (32.0/5)*eta*eta

    # List term coefficients
    f2 = -(1247.0/336)-eta*35/12
    f3 = 4*pi - ( (11.0/4-3*eta)*xs + 11.0*delta*xa/4 )
    f4 = -44711.0/9072 + eta*9271.0/504 + eta*eta*65.0/18 + (287.0/96 + eta/24)*xs*xs \
         - dot(Xs,Xs)*(89.0/96 + eta*7/24) + xa*xa*(287.0/96-12*eta) + (4*eta-89.0/96)*dot(Xa,Xa) \
         + delta*287.0*xs*xa/48 - delta*dot(Xs,Xa)*89.0/48
    f5 = -pi*( eta*583.0/24 + 8191.0/672 ) + ( xs*(-59.0/16 + eta*227.0/9 - eta*eta*157.0/9) + delta*xa*(eta*701.0/36 - 59.0/16) )
    f6 = 6643739519.0/69854400 + pi*pi*16.0/3 - 1712.0*GammaE/105 - log(16*v*v)*856.0/105 + ( -134543.0/7776 + 41.0*pi*pi/48 )*eta - eta*eta*94403.0/3024 - eta*eta*eta*775.0/324
    f7 = pi*( -16285/504 + eta*214745.0/1728 + eta*eta*193385.0/3024 )
    f = [f2,f3,f4,f5,f6,f7]

    #
    F = Fnewt * (v**10) * ( 1.0 + sum( [ ek*(v**(k+2)) for k,fk in enumerate(f) ] ) )

    #
    ans = F
    return ans


#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#
# Class for TalyorT4 + Spin Post-Newtonian
#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#

#
class pn:

    '''

    High-level class for evaluation of PN waveforms.

    Key references:
    * https://arxiv.org/pdf/0810.5336.pdf

    '''

    # Class constructor
    def __init__( this,             # The current object
                  m1,               # The mass of the larger object
                  m2,               # The mass of the smaller object
                  X1,               # The dimensionless spin of the larger object
                  X2,               # The dimensionless spin of the smaller object
                  wM_min = 0.003,
                  wM_max = 0.18,
                  sceo = None,        # scentry object for gwylm conversion
                  Lhat = None,      # Unit direction of initial orbital angular momentum
                  verbose=True):    # Be verbose toggle

        # Let the people know that we are here
        if verbose: alert('Now constructing instance of the pn class.','pn')

        # Apply the validative constructor to the inputs and the current object
        this.__validative_constructor__(m1,m2,X1,X2,wM_min,wM_max,Lhat,verbose)

        # Calculate the orbital frequency
        this.__calc_orbital_frequency__()

        # Calculate COM energy
        this.__calc_com_binding_energy__()

        # Calculate system total angular momentum
        this.__calc_total_angular_momentum__()

        # Calculate time domain waveforms
        this.__calc_h_of_t__()

        # Use strain waveforms to calculate psi4 waveforms
        alert('Calculating psi4 and news from strain.')
        this.__calc_psi4_and_news_of_t__()

        # Make gwylm representation
        if sceo: this.__to_gwylmo__(sceo)

        # Let the people know
        # warning('Note that the calculation of waveforms has not been implemented.','pn')

        #
        return None


    # Convert waveform information into gwylmo
    def __to_gwylmo__(this,
                      sceo): # instance of scentry class from nrutils

        '''
        This function takes in an instance of nrutils' scentry class
        '''

        # Let the people know
        if this.verbose: alert('Making gwylm represenation.')

        # Import useful things
        from nrutils import gwylm,gwf
        from scipy.interpolate import InterpolatedUnivariateSpline as spline
        from copy import deepcopy as copy
        from numpy import arange,linspace,exp,array,angle,unwrap,ones_like,zeros_like

        # Initial gwylm object
        sceo = copy(sceo)
        sceo.config = False
        y = gwylm(sceo,load=False,calcnews=False,calcstrain=False,load_dynamics=False)
        y.__lmlist__ = this.lmlist
        y.__input_lmlist__ = this.lmlist

        # Store useful remnant stuff
        y.remnant = this.remnant
        y.remnant['Mw'] = this.wM
        y.radiated = {}
        y.radiated['time_used'] = this.t
        y.radiated['mask'] = ones_like(this.t,dtype=bool)
        y.remnant['mask'] = y.radiated['mask']
        y.remnant['X'] = array( [zeros_like(this.t),zeros_like(this.t),this.remnant['J']/(this.remnant['M']**2)] ).T

        # Make equispace strain pn td and store to y
        alert('Interpolating time domain waveforms for equispacing.')
        dt = 0.5
        t = arange( min(this.t), max(this.t), dt )
        y.t = t
        for l,m in this.lmlist:

            #
            t_ = this.t

            # Store Strain
            hlm_ = this.h[l,m]
            amp_ = abs(hlm_); phi_ = unwrap(angle(hlm_))
            amp = spline(t_,amp_)(t)
            phi = spline(t_,phi_)(t)
            hlm = amp * exp( -1j*phi )
            wfarr = array([ t, hlm.real, hlm.imag ]).T
            y.hlm.append(  gwf( wfarr,l=l,m=m,kind='$rh_{%i%i}/M$'%(l,m) )  )

            # Store Psi4
            ylm_ = this.psi4[l,m]
            amp_ = abs(ylm_); phi_ = unwrap(angle(ylm_))
            amp = spline(t_,amp_)(t)
            phi = spline(t_,phi_)(t)
            ylm = amp * exp( -1j*phi )
            wfarr = array([ t, ylm.real, ylm.imag ]).T
            y.ylm.append(  gwf( wfarr,l=l,m=m,kind='$rM\psi_{%i%i}$'%(l,m) )  )

        #
        y.__curate__()
        y.pad( len(y.t)+500 )

        # Store the gwylmo represenation
        this.pn_gwylmo = y

    # Calculate all implemented strain time domain waveforms
    def __calc_h_of_t__(this):

        #
        this.h = {}
        #
        for l,m in this.lmlist:
            this.h[l,m] = this.__calc_hlm_of_t__(l,m)
        # Calculte m<0 multipoles using symmetry relationship
        alert('Calculating m<0 multipoles using symmetry relation.')
        for l,m in this.lmlist:
            this.h[l,-m] = (-1)**l * this.h[l,m].conj()
        #
        alert('Updating lmlist to inlcude m<0 multipoles.')
        this.lmlist = list(this.h.keys())


    # Use previously calculated strain waveforms to calculate psi4
    def __calc_psi4_and_news_of_t__(this):

        #
        this.news = {}
        this.psi4 = {}
        for l,m in this.h:
            h = this.h[l,m]
            this.news[l,m] = spline_diff( this.t, h, n=1 )
            this.psi4[l,m] = spline_diff( this.t, h, n=2 )


    # Calcilate a single implmented time domain waveform
    def __calc_hlm_of_t__(this,l,m):

        #
        from numpy import pi,log,sqrt,exp

        # Short-hand
        x = this.x
        eta = this.eta

        # Let the people know
        if this.verbose:
            alert('Calculating the (l,m)=(%i,%i) spherical multipole.'%(l,m))

        #
        if (l,m) == (2,2):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (2,2)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

            #
            part2 = 1 + \
                    x      * (-107.0/42 + 55.0/42*eta) + \
                    x**1.5 * (2*pi) + \
                    x**2   * (-2173.0/1512 - 1069.0/216*eta + 2047.0/1512*eta**2) + \
                    x**2.5 * ((-107.0/21+34.0/21*eta)*pi - 24*1j*eta) + \
                    x**3   * (27027409.0/646800 + 2.0/3*pi**2 + \
                              -856.0/105*this.__gamma_E__ - 1712.0/105*log(2) - 428.0/105*log(x) + \
                              -(278185.0/33264-41.0/96*pi**2)*eta - 20261.0/2772*eta**2 + \
                              114635.0/99792*eta**3 + 428.0*1j*pi/105)
            #
            spin   = x**(1.5) * (-4*this.delta*this.xa/3 + 4/3*(eta-1)*this.xs - 2*eta*x**(0.5)*(this.xa**2 - this.xs**2))
            #
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x
            #
            h = part1 * exp(-1j*m*this.phi)*(part2 + spin)

        elif (l,m) == (2,1):

            #
            part2 = (x**0.5 + \
        	       + x**1.5 * (-17.0/28+5*eta/7) + \
        	       + x**2.0 * (pi - 1.0j/2 - 2*1j*log(2)) + \
        	       + x**2.5 * (-43.0/126 - 509*eta/126 + 79.0*eta**2 / 168)) + \
        	       + x**3.0 * (-17.0*pi/28 + 3.0*pi*eta/14 + 1j*(17.0/56 + \
        			eta*(-995.0/84 - 3.0*log(2)/7) + 17.0*log(2)/14))
            #
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x * 1j/3*this.delta
            #
            h = part1 * exp(-1j*m*this.phi) * part2 + 4*1j*sqrt(pi/5)*exp(-1j*m*this.phi) * x**2 * eta*(this.xa+this.delta*this.xs)

        elif (l,m) == (2,0):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (2,0)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

            #
            part2 = 1.0
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x * (-5.0/(14*sqrt(6)))
            #
            h = part1*part2

        elif (l,m) == (3,3):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (3,3)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

            #
            part2 =  x**0.5	 					+ \
                	+x**1.5 * (-4 + 2*eta)					+ \
                	+x**2.0 * (3*pi - 21*1j/5 + 6*1j*log(1.5))		+ \
                	+x**2.5 * (123.0/110 - 1838.0*eta/165 + (887.0*eta**2)/330)	+ \
                	+x**3.0 * (-12*pi + 9.0*pi*eta/2 + 1j*(84.0/5 -24*log(1.5)   + \
                	eta*(-48103.0/1215+9*log(1.5))))
            #
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x * (-3.0/4*1j*this.delta*sqrt(15.0/14))
            #
            h = part1 * exp(-1j*m*this.phi) * part2

        elif (l,m) == (3,2):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (3,2)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

            #
            part2 =  x     *(1- 3*eta) + \
            x**2.0*(-193.0/90 + 145.0*eta/18 - (73.0*eta**2)/18) + \
            x**2.5*(2*pi*(1-3*eta) - 3*1j + 66*1j*eta/5) + \
            x**3.0*(-1451.0/3960 - 17387.0*eta/3960 + (5557.0*eta**2)/220 - (5341.0*eta**3)/1320)

            part1 = sqrt(16*pi/5) * 2*eta*this.M*x * 1.0/3*sqrt(5.0/7)

            #
            h = exp(-1j*m*this.phi)* ( part1*part2 + 32.0/3*sqrt(pi/7)*(eta**2)*this.xs*(x**2.5) )

        elif (l,m) == (3,1):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (3,1)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#

            #
            part2 =  x**0.5 + \
            	     x**1.5 * (-8.0/3 - 2*eta/3) + \
            	     x**2.0 * (pi - 7.0*1j/5 - 2.0*1j*log(2)) + \
            	     x**2.5 * (607.0/198 - 136.0*eta/99 + 247.0*eta**2/198) + \
            	     x**3.0 * ( -8.0*pi/3 - 7.0*pi*eta/6 + 1j*(56.0/15 + 16*log(2)/3 + \
            		 eta*(-1.0/15 + 7.0*log(2)/3)))
            #
            part1 =  sqrt(16.0*pi/5) * 2*eta*this.M*x * 1j*this.delta/(12*sqrt(14))
            #
            h = part1 * exp(-1j*m*this.phi) * part2

        elif (l,m) == (3,0):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (3,0)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            part2 = 1
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M * x * (-2.0/5*1j*sqrt(6.0/7)*x**2.5*eta)
            h = part1*part2

        elif (l,m) == (4,4):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (4,4)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            part2 =  x    *(1 - 3*eta)							+ \
                	 x**2.0*(-593.0/110 + 1273.0/66*eta - 175*eta**2/22)			+ \
                	 x**2.5*(4*pi*(1-3*eta) - 42*1j/5 + 1193*1j*eta/40 + 8*1j*(1-3*eta)*log(2)) + \
                	 x**3.0*(1068671.0/200200 - 1088119*eta/28600 +146879*eta**2/2340 + \
                		  -226097*eta**3/17160)
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x * (-8.0/9*sqrt(5.0/7));
            h = part1 * exp(-1j*m*this.phi) * part2

        elif (l,m) == (4,3):

            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            # (l,m) = (4,3)
            #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-#
            part2 = x**1.5 * (1 - 2*eta)                                        + \
                	x**2.5 * (-39.0/11 + 1267*eta/132 - 131*eta**2/33)			+ \
                	x**3.0 * (3*pi - 6*pi*eta + 1j*(-32/5 + eta*(16301.0/810 - 12*log(1.5)) + 6*log(1.5)))
            part1 = sqrt(16.0*pi/5) * 2*eta*this.M*x * (-9*1j*this.delta/(4*sqrt(70)))
            h = part1 * exp(-1j*m*this.phi) * part2

        else:
            #
            error( '(l,m) = (%i,%i) not implemented'%(l,m) )

        #
        return h


    # Calculate the orbital frequency of the binary source
    def __calc_orbital_frequency__(this):

        # Import usefuls
        from numpy import mod, array, pi

        # Let the people know
        if this.verbose:
            alert('Calculating evolution of orbital phase using RK4 steps.')

        #
        _wM = this.wM[-1]  # NOTE that M referes to intial system mass
        k = 0
        while _wM < this.wM_max :  # NOTE that M referes to intial system mass

            # NOTE that rk4_step is defined positive.learning
            this.state = rk4_step( this.state, this.t[-1], this.dt, this.__taylort4rhs__ )

            #
            this.t.append( this.t[-1]+this.dt )
            this.phi.append( this.state[0] )
            this.x.append(   this.state[1] )
            _wM = this.state[1] ** 1.5  # NOTE that M referes to intial system mass
            this.dt = 0.00009 * this.dtfac * this.M / ( _wM ** 3 )  # NOTE that M referes to intial system mass
            this.wM.append( _wM )

        # Convert quantities to array
        this.wM = array( this.wM )
        this.x = array( this.x )
        this.phi = array( this.phi )
        this.t = array( this.t )
        # Calculate related quantities
        this.w = this.wM / this.M
        this.fM = this.wM / ( 2*pi )
        this.f = this.w / ( 2*pi )
        this.v = this.wM ** (1.0/3)

        #
        return None


    # Calculate COM binding energy
    def __calc_com_binding_energy__(this):
        #
        alert('Calculating COM binding energy')
        this.E = pn_com_energy(this.f,this.m1,this.m2,this.X1,this.X2,this.Lhat)
        this.remnant['M'] = this.M+this.E


    # Calculate system angular momentum
    def __calc_total_angular_momentum__(this):
        '''
        Non-precessing
        '''

        # Import usefuls
        from numpy import sqrt,pi,log

        #
        if abs(this.x1)+abs(this.x2) > 0:
            warning('This function currently only works with non-spinning systems. See 1310.1528.')

        # Short-hand
        x = this.x
        eta = this.eta

        # Equation 234 of https://arxiv.org/pdf/1310.1528.pdf
        mu = this.eta * this.M
        e4 = -123671.0/5760 + pi*pi*9037.0/1536 + 1792*log(2)/15 + 896*this.__gamma_E__/15 \
             + eta*( pi*pi*3157.0/576 - 498449.0/3456 ) \
             + eta**2 * 301.0/1728 \
             + eta**3 * 77.0/31104
        j4 = -e4*5.0/7 + 64.9/35
        L = ( mu   * this.M / sqrt(x) ) * ( 1 \
            + x    * (1.5 + eta/6)
            + x*x  * ( 27.0/8 - eta*19.0/8 + eta*eta/24 ) \
            + x**3 * ( 135.0/16 + eta*( 41*pi*pi/24 - 6889.0/144 ) + eta*eta*31.0/24 + eta**3 * 7.0/1296 ) \
            + x**4 * ( 2835.0/128 + eta*j4 - 64.0*eta*log(x)/3 ) \
            )

        #
        S1 = this.x1*(this.m1**2)
        S2 = this.x2*(this.m2**2)
        Jz = L + S1 + S2

        # Store the information to the current object
        this.remnant['J'] = Jz


    # Method for calculating the RHS of the TaylorT4 first order ODEs for pn parameter x and frequency
    def __taylort4rhs__(this,state,time,**kwargs):

        # Import usefuls
        from numpy import array, pi, log, array

        # Unpack the state
        phi,x = state
        # * phi, Phase with 2*pi*f = dphi/dt where phi is the GW phase
        # *   x, PN parameter, function of frequency; v = (2*pi*M*f/m)**1.0/3 = x**0.5 (see e.g. https://arxiv.org/pdf/1601.05588.pdf)

        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#
        # Calculate useful parameters from current object
        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#

        # Mass ratio
        eta = this.eta
        # Mass difference
        delta = this.delta
        # Total INITIAL mass
        M = this.M
        # Get Euler Gamma
        gamma_E = this.__gamma_E__

        # Spins
        # NOTE that components along angular momentum are used below; see validative constructor
        X1 = this.x1
        X2 = this.x2
        Xs = 0.5 * ( X1+X2 )
        Xa = 0.5 * ( X1-X2 )

        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#
        # Calculate PN terms for x RHS
        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#

        # Nonspinning terms from 0907.0700 Eqn. 3.6
        Non_SpinningTerms = 1 - (743.0/336 + 11.0/4*eta)*x + 4*pi*x**1.5 \
                           + (34103.0/18144 + 13661.0/2016*eta + 59.0/18*eta**2)*x**2 \
                           + (4159.0/672 + 189.0/8*eta)*pi*x**2.5 + (16447322263.0/139708800 \
                           - 1712.0/105*gamma_E - 56198689.0/217728*eta +  541.0/896*eta**2 \
                           - 5605.0/2592*eta**3 + pi*pi/48*(256+451*eta) \
                           - 856.0/105*log(16*x))*x**3 + (-4415.0/4032 + 358675.0/6048*eta \
                           + 91495.0/1512*eta**2)*pi*x**3.5

        # Spinning terms from 0810.5336 and 0605140v4 using T4 expansion of dx/dt = -F(v)/E'(v)
        S3  = 4.0/3*(2-eta)*Xs + 8.0/3*delta*Xa
        S4  = eta*(2*Xa**2 - 2*Xs**2) + (1.0/2 - eta)*(-2*Xs**2 \
             - 2*Xa**2) + delta*(-2*Xs*Xa)
        S5  = (8 -121*eta/9 + 2*eta**2/9)*Xs + (8-31*eta/9)*delta*Xa
        SF3 = (-11.0/4 + 3*eta)*Xs - 11.0/4*delta*Xa
        SF4 = (33.0/16 -eta/4)*Xs**2 + (33.0/16 - 8*eta)*Xa**2 + 33*delta*Xs*Xa/8
        SF5 = (-59.0/16 + 227.0*eta/9 - 157.0*eta**2/9)*Xs + (-59.0/16 + 701.0*eta/36)*delta*Xa
        SpinningTerms = (-5.0*S3/2 + SF3) *x**1.5 + (-3*S4+ SF4)*x**2.0 \
                        + ( 5.0/672*(239+868*eta)*S3 - 7*S5/2 + (3.0/2 + eta/6)*SF3 \
                        + SF5 )*x**2.5	+ ( (239.0/112 + 31*eta/4)*S4 \
                        + 5*S3/4*(-8*pi+5*S3-2*SF3) + (3/2 + eta/6)*SF4) *x**3.0 \
                        + ( -3*S4*(4*pi+SF3) - 5*S3/18144*(99226+9*eta*(-4377	\
                        + 2966*eta)	+ -54432*S4 + 9072*SF4 ) \
                        + 1.0/288*( 3*(239+868*eta)*S5+4*(891+eta*(-477+11*eta))*SF3\
                        + 48*(9+eta)*SF5))*x**3.5

        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#
        # Calculate derivatives
        #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~#

        # Invert the definition of x( f = dphi_dt )
        dphi_dt = x**(1.5) / M
        # e.g. Equation 36 of https://arxiv.org/pdf/0907.0700.pdf
        # NOTE the differing conventions used here vs the ref above
        dx_dt   = (64 * eta / 5*M) * (x**5) * (Non_SpinningTerms+SpinningTerms)
        # Compile the state's derivative
        state_derivative = array( [ dphi_dt, dx_dt ] )

        # Return derivatives
        return state_derivative


    # Validate constructor inputs
    def __validative_constructor__(this,m1,m2,X1,X2,wM_min,wM_max,Lhat,verbose):

        # Import usefuls
        from numpy import ndarray,dot,array,sqrt
        from mpmath import euler as gamma_E

        # Masses must be float
        if not isinstance(m1,(float,int)):
            error('m1 input must be float or double, instead it is %s'%yellow(type(m1).__name__))
        if not isinstance(m2,(float,int)):
            error('m2 input must be float or double, instead it is %s'%yellow(type(m2).__name__))

        # Spins must be iterable of floats
        if len(X1) != 3:
            error( 'Length of X1 must be 3, but it is %i'%len(X1) )
        if len(X2) != 3:
            error( 'Length of X2 must be 3, but it is %i'%len(X2) )

        # Spins must be numpy arrays
        if not isinstance(X1,ndarray):
            X1 = array(X1)
        if not isinstance(X2,ndarray):
            X2 = array(X2)

        # By default it will be assumed that Lhat is in the z direction
        if Lhat is None: Lhat = array([0,0,1.0])

        # Let the people know
        this.verbose = verbose
        if this.verbose:
            alert('Defining the initial binary state based on inputs.','pn')

        # Rescale masses to unit total
        M = float(m1+m2); m1 = float(m1)/M; m2 = float(m2)/M
        if this.verbose: alert('Rescaling masses so that %s'%green('m1+m2=1'))

        # Store core inputs as well as simply derived quantities to the current object
        this.m1 = m1
        this.m2 = m2
        this.M = m1+m2  # Here M referes to intial system mass
        this.eta = m1*m2 / this.M
        this.delta = sqrt( 1-4*this.eta )
        this.X1 = X1
        this.X2 = X2
        this.Lhat = Lhat
        this.x1 = dot(X1,Lhat)
        this.x2 = dot(X2,Lhat)
        this.xs = (this.x1+this.x2)*0.5
        this.xa = (this.x1-this.x2)*0.5
        this.__gamma_E__ = float(gamma_E)
        # Bag for internal system quantities (remnant after radiated, not final)
        this.remnant = {}

        # Define initial binary state based on inputs
        this.t = [0]
        this.phi = [0]
        this.x  = [ wM_min**(2.0/3) ]
        this.wM = [ wM_min ]  # Orbital Frequency; NOTE that M referes to intial system mass
        this.wM_max = wM_max  # Here M referes to intial system mass
        this.wM_min = wM_min  # Here M referes to intial system mass
        this.initial_state = array([this.phi[-1],this.x[-1]])
        this.state = this.initial_state
        this.dtfac = 0.5
        this.dt = 0.00009*this.dtfac*this.M/(wM_min**3)

        # Binding energy
        this.E = [0]

        # Store a list of implemented l,m cases for waveform generation
        this.lmlist = [ (2,2), (2,1), (2,0), (3,3), (3,2), (3,1), (3,0), (4,4) ]




#####

# Convert phenom frequency domain waveform to time domain
def phenom2td( fstart, N, dt, model_data, plot=False, verbose=False, force_t=False, time_shift=None, fmax=0.5, ringdown_pad=600 ):
    '''
    INPUTS
    ---
    fstart,             Units: M*omega/(2*pi)
    N,                  Number of samples for output (use an NR waveform for reference!). NOTE that this input may be overwrridden by an internal check on waveform length.
    dt,                 Time step of output (use an NR waveform for reference!)
    model_data,         [Mx3] shaped numpy array in GEOMETRIC UNITS
    plot=False,         Toggle for plotting output
    verbose=False,      Toggle for verbose
    force_t=False       Force the total time duration of the output based on inputs

    OUTPUTS
    ---
    ht,                 Waveform time series (complex)
    t,                  time values
    time_shift          Location od waveform peak
    '''
    # The idea here is to perform the formatting in a parameterized rather than mimicked way.
    '''
    NOTE that the model's phase must be well resolved in order for us to get reasonable results.
    '''

    # Setup plotting backend
    __plot__ = True if plot else False
    if __plot__:
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import axes3d
        mpl.rcParams['lines.linewidth'] = 0.8
        mpl.rcParams['font.family'] = 'serif'
        mpl.rcParams['font.size'] = 12
        mpl.rcParams['axes.labelsize'] = 20
        mpl.rcParams['axes.titlesize'] = 20
        from matplotlib.pyplot import plot,xlabel,ylabel,figure,xlim,ylim,axhline
        from matplotlib.pyplot import yscale,xscale,axvline,axhline,subplot
        import matplotlib.gridspec as gridspec
    #
    from scipy.fftpack import fft,fftshift,ifft,fftfreq,ifftshift
    from scipy.stats import mode
    from numpy import array,arange,zeros,ones,unwrap,histogram,zeros_like
    from numpy import argmax,angle,linspace,exp,diff,pi,floor,convolve
    from scipy.interpolate import CubicSpline as spline

    ##%% Construct the model on this domain

    # Copy input data
    model_f   = array( model_data[0] )
    model_amp = array( model_data[1] )
    model_pha = array( model_data[2] )

    # NOTE: Using the regular diff here would result in
    # unpredictable results due to round-off error

    #-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-#
    ''' Determine the index location of the desired time shift.
    The idea here is that the fd phase derivative has units of time
    and is directly proportional to the map between time and frquency '''
    #-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-#
    dmodel_pha = spline_diff(2*pi*model_f,model_pha)
    # dmodel_pha = intrp_diff(2*pi*model_f,model_pha)
    # Define mask over which to consider derivative
    mask = (abs(model_f)<0.4) & (abs(model_f)>0.01)
    # NOTE:
    # * "sum(mask)-1" -- Using the last value places the peak of
    #   the time domain waveform at the end of the vector
    # * "argmax( dmodel_pha[ mask ] )" -- Using this value
    #   places the peak of the time domain waveform just before
    #   the end of the vector
    # #%% Use last value
    # argmax_shift = sum(mask)-1
    # time_shift = dmodel_pha[ mask ][ argmax_shift ]
    #%% Use mode // histogram better than mode funcion for continuus sets
    # This method is likely the most robust
    if time_shift is None:
        hist,edges = histogram( dmodel_pha[mask],50 )
        time_shift = edges[ 1+argmax( hist ) ]
    # #%% Use peak of phase derivative
    # argmax_shift = argmax( dmodel_pha[ mask ] )
    # time_shift = dmodel_pha[ mask ][ argmax_shift ]

    # #
    # figure()
    # plot( model_f[mask], dmodel_pha[ mask ]  )
    # axhline( time_shift, linestyle='--' )
    # axhline( max(dmodel_pha[ mask ]), color='r', alpha=0.5 )
    # # axvline( model_f[kstart], linestyle=':' )

    #
    ringdown_pad = ringdown_pad     # Time units not index; TD padding for ringdown
    td_window_width = 3.0/fstart    # Used for determining the TD window function
    fmax = fmax                     # Used for tapering the FD ampliutde
    fstart_eff = fstart#/(pi-2)     # Effective starting frequency for taper generation


    #-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-#
    ''' -- DETERMINE WHETHER THE GIVEN N IS LARGE ENOUGH -- '''
    ''' The method below works becuase the stationary phase approximation
    can be applied from the time to frequency domain as well as from the frequency
    domain to the time domain. '''
    #-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-%%-#
    # Estimate the total time needed for the waveform
    # Here the 4 is a safety factor -- techincally the total
    # time needed depends on the window that will be applied in the frequency domain
    # The point is that the total time should be sufficiently long to avoid the waveform
    # overlapping with itself in the time domain.
    T = 4*sum( abs( diff(dmodel_pha[(abs(model_f)<0.4) & (abs(model_f)>fstart_eff)]) ) )
    T += ringdown_pad+td_window_width
    input_T = N*dt
    if verbose:
        print('>> The total time needed for the waveform is %g'%T)
        print('>> The total time provided for the waveform is %g'%input_T)
        if force_t: print('>> The time provided for the waveform will not be adjusted according to the internal estimate becuase teh force_t=True input has been given.')
    if (input_T < T) and (not force_t):
        input_N = N
        N = int( float(N*T)/input_T )
        if verbose:
            print('>> The number of samples is being changed from %i to %i.'%(input_N,N))
    ## INPUTS: N, dt (in some form)
    # Given dt and N (double sided), Create the new frequency domain
    N = int(N)
    _f_ = fftfreq( N, dt )
    t = dt*arange(N)
    df = 1.0/(N*dt)

    # Apply the time shift
    model_pha -= 2*pi*(time_shift+ringdown_pad)*model_f

    if verbose: print('>> shift = %f'%time_shift)
    # figure()
    # plot( model_f[mask],  intrp_diff(2*pi*model_f,model_pha)[mask] )
    # axhline(0,color='k',alpha=0.5)

    '''
    Make the time domain window
    '''
    fd_k_start = find( model_f > fstart )[0]
    t_start = dmodel_pha[ fd_k_start ] - time_shift
    if t_start > 0: t_start -= (N-1)*dt
    if verbose: print('t_start = %f'%t_start)
    # Define the index end of the window; here we take use of the point that
    # dmodel_pha=0 corresponds to the end of the time vector as to corroborate
    # with the application of time_shift
    k_start = find( (t-t[-1]+ringdown_pad)>=(t_start) )[0]-1
    #
    b = k_start
    a = b - int(td_window_width/dt)
    window = maketaper( t, [a,b] )
    window *= maketaper( t, [len(t)-1,len(t)-1-int(0.5*ringdown_pad/dt)] )


    # 1st try hard windowing around fstart and fend

    ##%% Work on positive side for m>0
    f_ = _f_[ _f_ > 0 ]

    # Interpolate model over this subdomain
    amp_,pha_ = zeros_like(f_),zeros_like(f_)
    mask = (f_>=min(model_f)) & (f_<=max(model_f))
    amp_[mask] = spline( model_f,model_amp )(f_[mask])
    pha_[mask] = spline( model_f,model_pha )(f_[mask])

    # figure( figsize=2*array([6,2]) )
    # subplot(1,2,1)
    # plot( model_f, model_amp )
    # plot( f_, amp_, '--k' )
    # yscale('log'); xscale('log')
    # subplot(1,2,2)
    # plot( model_f, model_pha )
    # plot( f_, pha_, '--k' )
    # xscale('log')

    ## Work on negative side for m>0
    _f = _f_[ _f_ < 0 ]
    # Make zero
    _amp = zeros( _f.shape )
    _pha = zeros( _f.shape )

    ## Combine positive and negative sides
    _amp_ = zeros( _f_.shape )
    _pha_ = zeros( _f_.shape )
    _amp_[ _f_<0 ] = _amp; _amp_[ _f_>0 ] = amp_
    _pha_[ _f_<0 ] = _pha; _pha_[ _f_>0 ] = pha_

    # Switch FFT convention (or not)
    amp = _amp_
    pha = _pha_
    f = _f_
    # Construct complex waveform
    hf_raw = amp * exp( -1j*pha )

    window = maketaper(f,[ find(f>0)[0], find(f>fstart_eff)[0] ],window_type='exp')
    hf_raw *= window
    # hf_raw *= maketaper(f,[ find(f>fmax)[0], find(f>(fmax-0.1))[0] ],window_type='parzen')

    #
    fd_window = fft( window )

    # hf = fftshift( convolve(fftshift(fd_window),fftshift(hf_raw),mode='same')/N )
    hf = hf_raw

    #----------------------------------------------#
    # Calculate Time Domain Waveform
    #----------------------------------------------#
    ht = ifft( hf ) * df*N
    # ht *= window

    #----------------------------------------------#
    # Center waveform in time series and set peak
    # time to zero.
    #----------------------------------------------#
    # ind_shift = -argmax(abs(ht))+len(ht)/2
    # ht = ishift( ht, ind_shift )
    if verbose: print('>> The time domain waveform has a peak at index %i of %i'%(argmax(abs(ht)),len(t)))
    t -= t[ argmax(abs(ht)) ]

    if __plot__:

        figure( figsize=2*array([10,2]) )

        gs = gridspec.GridSpec(1,7)
        # figure( figsize=2*array([2.2,2]) )
        # subplot(1,2,1)
        ax1 = subplot( gs[0,0] )
        subplot(1,4,1)
        plot( abs(f), abs(hf) )
        plot( abs(f), abs(hf_raw), '--' )
        plot( abs(f), amp, ':m' )
        plot( abs(f), abs(fd_window),'k',alpha=0.3 )
        axvline( fstart, color='k', alpha=0.5, linestyle=':' )
        yscale('log'); xscale('log')
        xlim( [ fstart/10,fmax*2 ] )
        xlabel('$fM$')
        ylabel(r'$|\tilde{h}(f)|$')
        # subplot(1,2,2)
        # plot( abs(f), unwrap(angle(hf)) )
        # xscale('log')

        # figure( figsize=2*array([6,2]) )
        ax2 = subplot( gs[0,2:-1] )
        axhline( 0, color='k', linestyle='-', alpha=0.5 )
        clr = rgb(3); white = ones( (3,) )
        plot( t, ht.real, color=0.8*white )
        plot( t, ht.imag, color=0.4*white )
        plot( t,abs(ht), color=clr[0] )
        plot( t,-abs(ht), color=clr[0] )
        axvline( t[k_start], color='k', alpha=0.5, linestyle=':' )
        plot( t, window*0.9*max(ylim()),':k',alpha=0.5 )
        xlim(lim(t))
        xlabel('$t/M$')
        ylabel(r'$h(t)$')

    #
    return ht,t,time_shift


###


def leaver_dev( a, l, m, n, s, M=1.0, verbose=False, solve=False ):

    # Import usefuls
    from numpy import ndarray,array

    # Validate inputs


    # construct string for loading data

    # Define function to handle single spin and mass values
    def helper( a, l, m, n, s, M, verbose, solve ):

        # If requested, use loaded data as guess for full solver

        # Return answer for single spin value
        return (cw,sc)

    #
    if isinstance(jf,(tuple,list,ndarray)):
        #
        cw,sc = array( [ helper(a_, l, m, n, s, M, verbose, solve) for a_ in a ] )[:,:,0].T
        return cw,sc
    else:
        #
        return helper( a, l, m, n, s, M, verbose, solve )


'''
Method to load tabulated QNM data, interpolate and then output for input final spin
'''
def leaver( jf,                     # Dimensionless BH Spin
            l,                      # Polar Index
            m,                      # Azimuthal index
            n =  0,                 # Overtone Number
            p = None,               # Parity Number for explicit selection of prograde (p=1) or retrograde (p=-1) solutions.
            s = -2,                 # Spin weight
            Mf = 1.0,               # BH mass. NOTE that the default value of 1 is consistent with the tabulated data. (Geometric units ~ M_bare / M_ADM )
            verbose = False ):      # Toggle to be verbose

    #
    from numpy import ndarray,array

    #
    if isinstance(jf,(tuple,list,ndarray)):
        #
        cw,sc = array( [ __leaver_helper__(jf_, l, m, n, p , s, Mf, verbose) for jf_ in jf ] )[:,:,0].T
        return cw,sc

    else:
        #
        return __leaver_helper__(jf, l, m, n, p , s, Mf, verbose)


def __leaver_helper__( jf, l, m, n =  0, p = None, s = -2, Mf = 1.0, verbose = False):


    # Import useful things
    import os
    from scipy.interpolate import InterpolatedUnivariateSpline as spline
    from numpy import loadtxt,exp,sign,abs,ndarray,array
    from numpy.linalg import norm

    # Validate jf input: case of int given, make float. NOTE that there is further validation below.
    if isinstance(jf,(int,float)): jf = [float(jf)]
    if not isinstance(jf,ndarray): jf = array(jf)
    # Valudate s input
    if abs(s) != 2: raise ValueError('This function currently handles on cases with |s|=2, but s=%i was given.'%s)
    # Validate l input
    # Validate m input

    #%%%%%%%%%%%%%%%%%%%%%%%%%# NEGATIVE SPIN HANDLING #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    # Define a parity value to be used later:
    # NOTE that is p>0, then the corotating branch will be loaded, else if p<0, then the counter-rotating solution branch will be loaded.
    if p is None:
        p = sign(jf) + ( jf==0 )
    # NOTE that the norm of the spin input will be used to interpolate the data as the numerical data was mapped according to jf>=0
    # Given l,m,n,sign(jf) create a RELATIVE file string from which to load the data
    cmd = parent(os.path.realpath(__file__))
    #********************************************************************************#
    m_label = 'm%i'%abs(m) if (p>=0) or (abs(m)==0) else 'mm%i'%abs(m)
    #********************************************************************************#
    data_location = '%s/data/kerr/l%i/n%il%i%s.dat' % (cmd,l,n,l,m_label)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

    # Validate data location
    if not os.path.isfile(data_location): raise ValueError('The OS reports that "%s" is not a file or does not exist. Either the input QNM data is out of bounds (not currently stored in this repo), or there was an input error by the user.' % green(data_location) )

    # Load the QNM data
    data = loadtxt( data_location )

    # Extract spin, frequencies and separation constants
    JF = data[:,0]
    CW = data[:,1] - 1j*data[:,2] # NOTE: The minus sign here sets a phase convention
                          # where exp(+1j*cw*t) rather than exp(-1j*cw*t)
    CS = data[:,3] - 1j*data[:,4] # NOTE: There is a minus sign here to be consistent with the line above

    # Validate the jf input
    njf = abs(jf) # NOTE that the calculations were done using the jf>=0 convention
    if min(njf)<min(JF) or max(njf)>max(JF):
        warning('The input value of |jf|=%1.4f is outside the domain of numerical values [%1.4f,%1.4f]. Note that the tabulated values were computed on jf>0.' % (njf,min(JF),max(JF)) )

    # Here we rescale to a unit mass. This is needed because leaver's convention was used to perform the initial calculations.
    M_leaver = 0.5
    CW *= M_leaver

    # Interpolate/Extrapolate to estimate outputs
    cw = spline( JF, CW.real )(njf) + 1j*spline( JF, CW.imag )( njf )
    cs = spline( JF, CS.real )(njf) + 1j*spline( JF, CS.imag )( njf )

    # If needed, use symmetry relationships to get correct output.
    def qnmflip(CW,CS):
        return -cw.conj(),cs.conj()
    if m<0:
        cw,cs =  qnmflip(cw,cs)
    if p<0:
        cw,cs =  qnmflip(cw,cs)

    # NOTE that the signs must be flipped one last time so that output is
    # directly consistent with the argmin of leaver's equations at the requested spin values
    cw = cw.conj()
    cs = cs.conj()

    # Here we scale the frequency by the BH mass according to the optional Mf input
    cw /= Mf

    # Handle positive spin weight
    if s>0:
        cs = cs - 2*abs(s)

    #
    return cw,cs


# Fit for spherica-sphoidal harmonic inner-product from Berti et al
def ysprod14081860(j,ll,mm,lmn):
    import positive
    from numpy import loadtxt,array,ndarray
    '''
    Fits for sherical-spheroidal mixing coefficients from arxiv:1408.1860 -- Berti, Klein

    * The refer to mixing coefficients as mu_mll'n'
    * their fits are parameterized by dimensionless BH spin j=a/M
    * They model the real and imaginary parts separately as seen in Eq. 11
    * Fitting coefficients are listed in table I

    NOTE that the input format of this function is designed to be consistent with ysprod(...)
    NOTE that tis function explicitely loads their full fit inpf from an external file

    LondonL@mit.edu 2019
    '''
    tbl = loadtxt(parent(os.path.realpath(__file__))+'/data/berti_swsh_fits.dat')

    def lowlevel(J,__mm__):
        MM,LL,L,N,P1,P2,P3,P4,Q1,Q2,Q3,Q4,_,_,_,_ = tbl.T
        l,m,n = lmn
        flip = False
        if J<0:
            J = abs(J)
            __mm__ *= -1
            flip = True
        k = (ll==LL) & (__mm__==MM) & (l==L) & (n==N)
        if sum(k)!=1:
            error('cannot find fit from Berti+ for (L,M,l,m,n) = (%i,%i,%i,%i,%)'%(L,M,l,m,n))
        lowlevel_ans = (1.0 if ll==l else 0) + P1[k]*J**P2[k] + P3[k]*J**P4[k] + 1j * ( Q1[k]*J**Q2[k] + Q3[k]*J**Q4[k] )
        return (lowlevel_ans if not flip else lowlevel_ans.conj()).conj()

    #
    if isinstance(j,(list,tuple,ndarray)):
        return array( [ lowlevel(j_,mm) for j_ in j ] )
    else:
        return lowlevel(j,mm)


# Fit for spherica-sphoidal harmonic inner-product from Berti et al
def ysprod14081860_from_paper_is_broken(j,L,M,lmn):

    '''
    Fits for sherical-spheroidal mixing coefficients from arxiv:1408.1860 -- Berti, Klein

    * The refer to mixing coefficients as mu_mll'n'
    * their fits are parameterized by dimensionless BH spin j=a/M
    * They model the real and imaginary parts separately as seen in Eq. 11
    * Fitting coefficients are listed in table I

    NOTE that the input format of this function is designed to be consistent with ysprod(...)
    NOTE that the values listed in the table are so large as they are susceptible to severe error due to truncation yielding this function fucked

    LondonL@mit.edu 2019
    '''

    # Warn the user
    warning('This function uses values listed in the paper\'s table. These values are so large as they are susceptible to severe error due to truncation yielding this function fucked.')

    # Unpack spheroidal indeces
    l,m,n = lmn

    # A represenation of their Table I. NOTE that the original tex from the arxiv was used here; find-replace and multi-select was performed for dictionary formatting
    TBL = {}
    TBL[2,2,2,0] = {'p1':-740,'p2':2.889,'p3':-661,'p4':17.129,'q1':1530,'q2':1.219,'q3':-934,'q4':24.992}
    TBL[2,2,2,1] = {'p1':-873,'p2':2.655,'p3':-539,'p4':15.665,'q1':4573,'q2':1.209,'q3':-2801,'q4':25.451}
    TBL[2,2,3,0] = {'p1':14095,'p2':1.112,'p3':4395,'p4':6.144,'q1':1323,'q2':0.854,'q3':-852,'q4':7.042}
    TBL[2,3,2,0] = {'p1':-10351,'p2':1.223,'p3':-5750,'p4':8.705,'q1':-1600,'q2':0.953,'q3':1003,'q4':14.755}
    TBL[-2,2,2,0] = {'p1': -1437,'p2':2.118,'p3':1035,'p4':2.229,'q1':-7015,'q2':1.005,'q3':67,'q4':3.527}
    TBL[-2,2,2,1] = {'p1': -2659,'p2':2.007,'p3':53,'p4':4.245,'q1':-21809,'q2':1.008,'q3':221,'q4':4.248}
    TBL[-2,2,3,0] = {'p1': 14971,'p2':1.048,'p3':-5463,'p4':1.358,'q1':18467,'q2':1.015,'q3':-10753,'q4':1.876}
    TBL[-2,3,2,0] = {'p1': -13475,'p2':1.088,'p3':7963,'p4':1.279,'q1':-1744,'q2':1.011,'q3':516,'q4':1.821}


    if (M,L,l,n) in TBL:

        # Extract relevant data from model dictionary using inputs
        p1 = TBL[M,L,l,n]['p1']
        p2 = TBL[M,L,l,n]['p2']
        p3 = TBL[M,L,l,n]['p3']
        p4 = TBL[M,L,l,n]['p4']
        q1 = TBL[M,L,l,n]['q1']
        q2 = TBL[M,L,l,n]['q2']
        q3 = TBL[M,L,l,n]['q3']
        q4 = TBL[M,L,l,n]['q4']

        #
        delta_llp = 1.0 if L==l else 0

        # Evaluate Equation 11
        if m==M:
            re_mu = delta_llp + (p1 * (j ** (p2*1e5))) + (p3 * (j ** (p4*1e5)))
            im_mu = (q1 * (j ** (q2*1e5))) + (q3 * (j ** (q4*1e5)))
            ans = re_mu + 1j*im_mu
        else:
            ans = 0

    else:

        warning('Berti\'s model does not include (L,M)(l,m,n) = %s%s'%(str((L,M)),str((l,m,n))) )
        ans = j/0

    # Return answer
    return ans


#
def CookZalutskiy14107698(jf,l,m,n):

    '''
    Fir for Kerr s=-2 QNM frequencies from Cook+Zalutskiy arxiv:1410.7698
    '''

    #
    from numpy import sqrt

    #
    eps = 1-jf

    # TABLE I
    TBL1 = {}
    TBL1[2,2] = { 'delta':2.05093, 'a1':2.05084, 'a2':1.64, 'a3':-0.032, 'a4':1.343 }
    TBL1[3,3] = { 'delta':2.79361, 'a1':2.79361, 'a2':2.289, 'a3':-0.0004, 'a4':1.35730 }
    TBL1[4,4] = { 'delta':3.56478, 'a1':3.56478, 'a2':2.79572, 'a3':-0.00020, 'a4':1.34522 }
    TBL1[5,4] = { 'delta':1.07271, 'a1':1.0687, 'a2':-28., 'a3':-3.4, 'a4':-17.90 }
    TBL1[5,5] = { 'delta':4.35761, 'a1':4.35761, 'a2':3.29989, 'a3':-0.000142, 'a4':1.33085 }
    TBL1[6,5] = { 'delta':2.37521, 'a1':2.37515, 'a2':-5.50, 'a3':-0.672, 'a4':-1.206 }
    TBL1[6,6] = { 'delta':5.16594, 'a1':5.16594, 'a2':3.81003, 'a3':-0.000111, 'a4':1.31809 }
    TBL1[7,6] = { 'delta':3.40439, 'a1':3.40438, 'a2':-2.03, 'a3':-0.0109, 'a4':0.2931 }
    TBL1[7,7] = { 'delta':5.98547, 'a1':5.98547, 'a2':4.32747, 'a3':-0.000091, 'a4':1.30757 }
    TBL1[8,7] = { 'delta':4.35924, 'a1':4.35924, 'a2':-0.274, 'a3':-0.0034, 'a4':0.74198 }
    TBL1[8,8] = { 'delta':6.81327, 'a1':6.81327, 'a2':4.85207, 'a3':-0.000078, 'a4':1.29905 }
    TBL1[9,8] = { 'delta':5.28081, 'a1':5.28081, 'a2':0.9429, 'a3':-0.00150, 'a4':0.93670 }
    TBL1[10,8] = { 'delta':2.80128, 'a1':2.80099, 'a2':-22.9, 'a3':-0.43, 'a4':-6.456 }
    TBL1[9,9] = { 'delta':7.64735, 'a1':7.64734, 'a2':5.38314, 'a3':-0.000069, 'a4':1.29217 }
    TBL1[10,9] = { 'delta':6.18436, 'a1':6.18436, 'a2':1.92226, 'a3':-0.00080, 'a4':1.03870 }
    TBL1[11,9] = { 'delta':4.05104, 'a1':4.05101, 'a2':-11.00, 'a3':-0.053, 'a4':-1.568 }
    TBL1[10,10] = { 'delta':8.48628, 'a1':8.48628, 'a2':5.91988, 'a3':-0.000062, 'a4':1.28657 }
    TBL1[11,10] = { 'delta':7.07706, 'a1':7.07706, 'a2':2.7754, 'a3':-0.00048, 'a4':1.09871 }
    TBL1[12,10] = { 'delta':5.14457, 'a1':5.14457, 'a2':-6.269, 'a3':-0.0147, 'a4':-0.2362 }
    TBL1[11,11] = { 'delta':9.32904, 'a1':9.32904, 'a2':6.46155, 'a3':-0.000056, 'a4':1.28198 }
    TBL1[12,11] = { 'delta':7.96274, 'a1':7.96274, 'a2':3.5535, 'a3':-0.00032, 'a4':1.13691 }
    TBL1[12,12] = { 'delta':10.1749, 'a1':10.1749, 'a2':7.00748, 'a3':-0.00005, 'a4':1.27819 }

    # TABLE III
    TBL2 = {}
    TBL2[2,1] = { 'delta': 1j*1.91907,'a1':3.23813,'a2':1.54514,'a3':1.91906,'a4':-0.021,'a5':-0.0109 }
    TBL2[3,1] = { 'delta': 1j*3.17492,'a1':2.11224,'a2':0.710824,'a3':3.17492,'a4':-0.0061,'a5':-0.0022 }
    TBL2[4,1] = { 'delta': 1j*4.26749,'a1':1.82009,'a2':0.000000,'a3':4.26749,'a4':-0.0048,'a5':0.000000 }
    TBL2[3,2] = { 'delta': 1j*1.87115,'a1':7.2471,'a2':3.4744,'a3':1.87108,'a4':-0.12,'a5':-0.061 }
    TBL2[4,2] = { 'delta': 1j*3.47950,'a1':4.19465,'a2':1.30534,'a3':3.47950,'a4':-0.0106,'a5':-0.0040 }
    TBL2[5,2] = { 'delta': 1j*4.72816,'a1':3.61332,'a2':0.882398,'a3':4.72816,'a4':-0.0067,'a5':-0.0018 }
    TBL2[4,3] = { 'delta': 1j*1.37578,'a1':22.66,'a2':12.807,'a3':1.37549,'a4':-1.6,'a5':-0.87 }
    TBL2[5,3] = { 'delta': 1j*3.54313,'a1':6.80319,'a2':2.05358,'a3':3.54312,'a4':-0.024,'a5':-0.0094 }
    TBL2[6,3] = { 'delta': 1j*4.98492,'a1':5.59000,'a2':1.29263,'a3':4.98492,'a4':-0.0103,'a5':-0.0029 }
    TBL2[7,3] = { 'delta': 1j*6.24553,'a1':5.13084,'a2':0.000000,'a3':6.24552,'a4':-0.0077,'a5':0.000000 }
    TBL2[6,4] = { 'delta': 1j*3.38736,'a1':10.6913,'a2':3.26423,'a3':3.38733,'a4':-0.075,'a5':-0.029 }
    TBL2[7,4] = { 'delta': 1j*5.07533,'a1':7.93057,'a2':1.78114,'a3':5.07532,'a4':-0.018,'a5':-0.0053 }
    TBL2[8,4] = { 'delta': 1j*6.47378,'a1':7.07896,'a2':0.000000,'a3':6.47378,'a4':-0.0100,'a5':0.000000 }
    TBL2[7,5] = { 'delta': 1j*2.98127,'a1':18.146,'a2':5.9243,'a3':2.98114,'a4':-0.32,'a5':-0.131 }
    TBL2[8,5] = { 'delta': 1j*5.01168,'a1':10.9114,'a2':2.43320,'a3':5.01167,'a4':-0.033,'a5':-0.0101 }
    TBL2[9,5] = { 'delta': 1j*6.57480,'a1':9.30775,'a2':1.66898,'a3':6.57480,'a4':-0.0152,'a5':-0.0036 }
    TBL2[8,6] = { 'delta': 1j*2.19168,'a1':43.25,'a2':16.68,'a3':2.1906,'a4':-2.9,'a5':-1.45 }
    TBL2[9,6] = { 'delta': 1j*4.78975,'a1':15.0733,'a2':3.41635,'a3':4.78972,'a4':-0.077,'a5':-0.024 }
    TBL2[10,6] = { 'delta': 1j*6.55627,'a1':11.9630,'a2':2.12050,'a3':6.55626,'a4':-0.0252,'a5':-0.0063 }
    TBL2[11,6] = { 'delta': 1j*8.06162,'a1':10.7711,'a2':0.000000,'a3':8.06162,'a4':-0.0153,'a5':0.000000 }
    TBL2[10,7] = { 'delta': 1j*4.38687,'a1':21.7120,'a2':5.1575,'a3':4.38680,'a4':-0.21,'a5':-0.068 }
    TBL2[11,7] = { 'delta': 1j*6.41836,'a1':15.2830,'a2':2.71488,'a3':6.41835,'a4':-0.042,'a5':-0.0108 }
    TBL2[12,7] = { 'delta': 1j*8.07005,'a1':13.2593,'a2':0.000000,'a3':8.07005,'a4':-0.021,'a5':0.000000 }
    TBL2[11,8] = { 'delta': 1j*3.74604,'a1':34.980,'a2':9.159,'a3':3.74569,'a4':-0.91,'a5':-0.32 }
    TBL2[12,8] = { 'delta': 1j*6.15394,'a1':19.6999,'a2':3.56155,'a3':6.15392,'a4':-0.084,'a5':-0.022 }
    TBL2[12,9] = { 'delta': 1j*2.70389,'a1':79.21,'a2':25.64,'a3':2.7015,'a4':-7.2,'a5':-3.20 }

    #
    if (l,m) in TBL1:

        # Unpack table
        a1 = TBL1[l,m]['a1']
        a2 = TBL1[l,m]['a2']
        a3 = TBL1[l,m]['a3']
        a4 = TBL1[l,m]['a4']

        # Evaluate Eq 63
        wr = 0.5*m - a1*sqrt( 0.5*eps ) + (a2 + a3*n)*eps
        wc = -( n+0.5 ) * ( sqrt(0.5*eps) - a4 * eps )

    elif (l,m) in TBL2:

        # Unpack table
        a1 = TBL2[l,m]['a1']
        a2 = TBL2[l,m]['a2']
        a3 = TBL2[l,m]['a3']
        a4 = TBL2[l,m]['a4']
        a5 = TBL2[l,m]['a5']

        # Evaluate Eq 64
        wr = 0.5*m + (a1+a2*n)*eps
        wc = -1.0 * ( a3 + n + 0.5 ) * sqrt( 0.5*eps ) + (a4+a5*n)*eps

    else:

        #
        error('unsupported multipole given (l,m) = %s'%str((l,m)))

    #
    cw = wr + 1j*wc


    #
    return cw


# Berti+'s 2005 fit for QNM frequencies
def Berti0512160(jf,l,m,n):

    '''
    Fit for Kerr -2 QNMs from Berti+ gr-qc/0512160.
    external data sourced from https://pages.jh.edu/~eberti2/ringdown/
    '''

    # Import usefuls
    from numpy import loadtxt,array,ndarray
    import positive

    # Load fit coefficients
    data_path = parent(os.path.realpath(__file__))+'/data/berti_kerrcw_fitcoeffsWEB.dat'
    data = loadtxt(data_path)

    # Unpack: l,m,n,f1,f2,f3,q1,q2,q3
    ll,mm,nn,ff1,ff2,ff3,qq1,qq2,qq3 = data.T

    #
    def lowlevel(JF,M):

        #
        if JF<0:
            M *= -1
            JF *= -1

        #
        k = (ll==l) & (mm==M) & (nn==n)

        #
        if not sum(k):
            error('this model does not include (l,m,n)=(%i,%i,%i)'%(l,m,n))

        #
        f1 = ff1[k]; f2 = ff2[k]; f3 = ff3[k]
        q1 = qq1[k]; q2 = qq2[k]; q3 = qq3[k]
        #
        wr = f1 + f2 * ( 1-JF )**f3
        Q  = q1 + q2 * ( 1-JF )**q3
        # See eqn 2.1 here https://arxiv.org/pdf/gr-qc/0512160.pdf
        wc = wr/(2*Q)
        #
        return wr+1j*wc

    #
    if isinstance(jf,(list,tuple,ndarray)):
        return array( [ lowlevel(j,m) for j in jf ] ).T[0]
    else:
        return lowlevel(jf,m)


# Fits for spin-2 QNM frequencies from arxiv:1810.03550
def cw181003550(jf,l,m,n):
    """Fit for quasi-normal mode frequencies

    Fit for the quasi-normal mode frequencies from
    https://arxiv.org/abs/1810.03550 for Kerr under -2 spin-weighted spheroidal
    harmonics. Fits are provided for the following indices

    |  l  |  m  |  n  |
    | --- | --- | --- |
    |  2  |  2  |  0  |
    |  2  | -2  |  0  |
    |  2  |  2  |  1  |
    |  2  | -2  |  1  |
    |  3  |  2  |  0  |
    |  3  | -2  |  0  |
    |  4  |  4  |  0  |
    |  4  | -4  |  0  |
    |  2  |  1  |  0  |
    |  2  | -1  |  0  |
    |  3  |  3  |  0  |
    |  3  | -3  |  0  |
    |  3  |  3  |  1  |
    |  3  | -3  |  1  |
    |  4  |  3  |  0  |
    |  4  | -3  |  0  |
    |  5  |  5  |  0  |
    |  5  | -5  |  0  |

    Parameters
    ----------
    jf: float
         Dimensionless final spin
    l: int
        Polar index
    m: int
        Azimuthal index
    n: int
        Overtone index

    Returns
    -------
    float
        Evaluation of the fit at `jf` for the requested Kerr -2 QNM
    """

    # Import usefuls
    from numpy import loadtxt,array,ndarray
    from imp import load_source
    import positive

    # Load fit functions from reference module
    module_path = parent(os.path.realpath(__file__))+'/data/ksm2_cw.py'
    cw_module = load_source( '', module_path )

    # Extract dict of fit functions
    fit_dictionary = cw_module.CW

    if (l,m,n) in fit_dictionary:
        #
        ans = fit_dictionary[l,m,n](jf)
    else:
        #
        error('this fit does not apply to (l,m,n)=(%i,%i,%i)'%(l,m,n))

    #
    return ans



# Fits for spin-2 spherical-spheroidal mixing coefficients from arxiv:1810.03550
def ysprod181003550(jf,ll,mm,lmn):
    """Fit for spherical-spheroidal mixing coefficients

    Fit for the spherical-spheroidal mixing coefficients from
    https://arxiv.org/abs/1810.03550 for Kerr under -2 spin-weighted harmonics.
    Fits are provided for the following spherical harmonic and Kerr indices

    | ll  | mm  | lmn       |
    | --- | --- | --------- |
    |  2  |  1  | (2, 1, 0) |
    |  2  |  2  | (2, 2, 0) |
    |  2  |  2  | (2, 2, 1) |
    |  3  |  2  | (2, 2, 0) |
    |  3  |  2  | (2, 2, 1) |
    |  3  |  2  | (3, 2, 0) |
    |  3  |  3  | (3, 3, 0) |
    |  3  |  3  | (3, 3, 1) |
    |  4  |  3  | (3, 3, 0) |
    |  4  |  3  | (4, 3, 0) |
    |  4  |  4  | (4, 4, 0) |
    |  5  |  5  | (5, 5, 0) |

    Parameters
    ----------
    jf: float
         Dimensionless final spin
    ll: int
        Spherical harmonic degree
    mm: int
        Spherical harmonic order
    lmn: list of int
        List of Kerr Indices [l, m, n]

    Returns
    -------
    float
        Evaluation of the fit at `jf` for the requested mixing coefficient
    """

    # Import usefuls
    from numpy import loadtxt,array,ndarray,log,exp
    from imp import load_source
    import positive

    # Extract dict of fit functions
    fit_dictionary = {
        (2, 1, 2, 1, 0): lambda x0: 0.9971577101354098*exp(6.2815088293225569j)  +  6.3541921214411894e-03 * (  143454.0616281430993695*exp(4.5060813273501665j)*(x0) + 354688.4750832330319099*exp(1.7326693927013841j)*(x0*x0) + 240378.2854125543963164*exp(5.1629102848140072j)*(x0*x0*x0) + 6026.9252628974973049*exp(1.8880583980908965j) ) / ( 1.0 +  73780.2159267508977791*exp(1.4129254015451644j)*(x0) + 97493.6172260692255804*exp(4.5395814919256727j)*(x0*x0) + 34814.9777696923483745*exp(1.4206733963391489j)*(x0*x0*x0) ),
        (2, 2, 2, 2, 0): lambda x0: 0.9973343021336419*exp(6.2813148178761091j)  +  7.5336160373579110e-03 * (  14.5923758203105400*exp(5.0600523238823607j)*(x0) + 28.7612830955165180*exp(1.6289978409506747j)*(x0*x0) + 14.5113507529443453*exp(4.6362218859245612j)*(x0*x0*x0) + 1.9624092507664150*exp(3.0112613110519790j) ) / ( 1.0 +  0.8867427721075676*exp(6.2202532788943463j)*(x0) + 1.0019792255065854*exp(3.2737011007062509j)*(x0*x0) + 0.0821482616116315*exp(2.4952790723412233j)*(x0*x0*x0) ),
        (2, 2, 2, 2, 1): lambda x0: 0.9968251006655715*exp(6.2782464977815033j)  +  2.0757805219598607e-02 * (  15.0768877264486765*exp(4.8322813296124032j)*(x0) + 31.1388349304345873*exp(1.5850449725805840j)*(x0*x0) + 15.4486406485143153*exp(4.6727325182881687j)*(x0*x0*x0) + 0.7189749887588365*exp(2.8084047359333271j) ) / ( 1.0 +  0.8059219252903900*exp(0.2579235302312085j)*(x0) + 0.6950198452267902*exp(3.6843441377638189j)*(x0*x0) + 0.3561345138627161*exp(2.8129259367413266j)*(x0*x0*x0) ),
        (3, 2, 2, 2, 0): lambda x0: 0.0205978660711896*exp(0.0474295298012882j)  +  6.9190162168113994e-02 * (  2.7656806568571959*exp(2.1329817160503861j)*(x0) + 3.9562158982293116*exp(4.6530163694526001j)*(x0*x0) + 2.3363698535756998*exp(2.6443646723682295j)*(x0*x0*x0) + 2.3989803671798935*exp(6.2766581209274568j) ) / ( 1.0 +  1.0595398565336638*exp(1.6448612531651137j)*(x0) + 0.9130774341264614*exp(6.0285976636462575j)*(x0*x0) + 0.6946816943215194*exp(3.3327882895176271j)*(x0*x0*x0) ),
        (3, 2, 2, 2, 1): lambda x0: 0.0220303770209119*exp(0.1645224015737339j)  +  7.3233344302596703e-02 * (  24.9322113499648026*exp(1.0180661306127561j)*(x0) + 30.1973220184149511*exp(4.4046911898286494j)*(x0*x0) + 11.2741216816767498*exp(2.9810158869949035j)*(x0*x0*x0) + 2.4373637035655071*exp(6.1958958829162727j) ) / ( 1.0 +  11.3967182799355697*exp(0.8537537359837979j)*(x0) + 10.9150545704939930*exp(2.6609572234291781j)*(x0*x0) + 7.2195768331341306*exp(4.9591911678862166j)*(x0*x0*x0) ),
        (3, 2, 3, 2, 0): lambda x0: 0.9900948849287589*exp(6.2804248687509565j)  +  2.3690082209346527e-02 * (  71893.0284688364044996*exp(1.2395199521970826j)*(x0) + 170547.7535011355357710*exp(5.0370601277314870j)*(x0*x0) + 129473.0632400779868476*exp(2.3589834727049306j)*(x0*x0*x0) + 1935.5063129042880519*exp(4.6680053884319301j) ) / ( 1.0 +  38206.4439771973629831*exp(4.3669921291251104j)*(x0) + 35811.0156501504534390*exp(0.8202376613805515j)*(x0*x0) + 8378.3365919880543515*exp(3.2588556618808240j)*(x0*x0*x0) ),
        (3, 3, 3, 3, 0): lambda x0: 0.9956935091939635*exp(6.2784823412948683j)  +  1.4545599733034410e-02 * (  7.2112377450866258*exp(0.6281060207724505j)*(x0) + 6.5381226130671095*exp(4.6215676022520444j)*(x0*x0) + 4.4510347535912222*exp(2.9227656614904154j)*(x0*x0*x0) + 1.7112774109660507*exp(2.9527107589222190j) ) / ( 1.0 +  1.4974006961584732*exp(4.8103032611120984j)*(x0) + 1.5287573244457504*exp(2.2468641698880383j)*(x0*x0) + 0.5211398892820160*exp(5.6886611584470419j)*(x0*x0*x0) ),
        (3, 3, 3, 3, 1): lambda x0: 0.9947799139299213*exp(6.2687860201480916j)  +  4.0478484180679702e-02 * (  4.4112734035486856*exp(1.2501463097148089j)*(x0) + 11.5876238172707406*exp(0.2795912119606259j)*(x0*x0) + 17.3218141087277253*exp(3.7903687208531087j)*(x0*x0*x0) + 0.6772374108565415*exp(2.5796853216144990j) ) / ( 1.0 +  3.8782075663390487*exp(5.4280212005550617j)*(x0) + 3.4912931569199648*exp(2.5238982607321545j)*(x0*x0) + 1.0367733448133998*exp(6.0498233292055152j)*(x0*x0*x0) ),
        (4, 3, 3, 3, 0): lambda x0: 0.0281121577247875*exp(0.0484878595517481j)  +  8.6382569875194229e-02 * (  12.0872895226366044*exp(0.4722122066619678j)*(x0) + 30.6262626401175417*exp(3.3281158362521670j)*(x0*x0) + 16.3281991298750100*exp(6.1785375072204518j)*(x0*x0*x0) + 2.3603267682389149*exp(6.2662351579714608j) ) / ( 1.0 +  4.9638141584463549*exp(0.4514701750473943j)*(x0) + 6.2552471990602712*exp(3.0584854159700825j)*(x0*x0) + 1.4538151679610098*exp(5.6955388697651710j)*(x0*x0*x0) ),
        (4, 3, 4, 3, 0): lambda x0: 0.9873523634400163*exp(6.2794650976486421j)  +  3.3027803522918557e-02 * (  700838.9044441945152357*exp(1.1066866283952814j)*(x0) + 1843013.1216291214805096*exp(4.8808349224255725j)*(x0*x0) + 1436658.3612134086433798*exp(2.1412051022385667j)*(x0*x0*x0) + 13844.4111501989991666*exp(4.5601015740698632j) ) / ( 1.0 +  356669.1344140542205423*exp(4.1565052819700004j)*(x0) + 327401.1637445305241272*exp(0.6329771391103556j)*(x0*x0) + 88620.8619731830985984*exp(3.2425422751663255j)*(x0*x0*x0) ),
        (4, 4, 4, 4, 0): lambda x0: 0.9947834747976544*exp(6.2775928790314088j)  +  2.4790925424940623e-02 * (  6.5171792863640983*exp(0.7983475243325006j)*(x0) + 7.7748196938039094*exp(4.2485120698165844j)*(x0*x0) + 1.1576799667402324*exp(1.5905452385036978j)*(x0*x0*x0) + 1.2434427129854981*exp(2.9615526265836647j) ) / ( 1.0 +  0.4454803253853161*exp(4.3912182331287690j)*(x0) + 0.5943671978440922*exp(2.5316559344513467j)*(x0*x0) + 0.2474336968120706*exp(5.9707578218053605j)*(x0*x0*x0) ),
        (5, 5, 5, 5, 0): lambda x0: 0.9943365401253647*exp(6.2773480319726191j)  +  3.1259875807999535e-02 * (  6.5508011783841358*exp(0.9339806071173702j)*(x0) + 8.0557862161937326*exp(4.2881187610320346j)*(x0*x0) + 0.9297117055414360*exp(1.0436436392517001j)*(x0*x0*x0) + 1.0903601095842754*exp(2.9711989367542477j) ) / ( 1.0 +  0.2312769649802813*exp(4.9081434508733581j)*(x0) + 0.5495791564905941*exp(2.7762081323140197j)*(x0*x0) + 0.2129999495217834*exp(6.1508375766326919j)*(x0*x0*x0) )
    }

    # Extract kerr indices
    l,m,n = lmn

    # Eval fit
    if (ll,mm,l,m,n) in fit_dictionary:
        #
        beta = 1.0 / ( 2 + ll-abs(mm) )
        kappa = lambda JF: (log( 2 - JF ) / log(3))**(beta)
        return fit_dictionary[ll,mm,l,m,n]( kappa(jf) )
    else:
        #
        error('this fit does not apply to (ll,mm,l,m,n)=(%i,%i,%i)'%(ll,mm,l,m,n))



#
def mass_ratio_convention_sort(m1,m2,chi1,chi2):

    '''
    Function to enforce mass ratio convention m1>m2.

    USAGE:

    m1,m2,chi1,chi2 = mass_ratio_convention_sort(m1,m2,chi1,chi2,format=None)

    INPUTS:

    m1,         1st component mass
    m2,         2nd component mass
    chi1,       1st dimensionless spin
    chi2,       2nd dimensionless spin

    OUTPUTS:

    m1,m2,chi1,chi2

    NOTE that outputs are swapped according to desired convention.

    londonl@mit.edu 2019

    '''

    # Import usefuls
    from numpy import min,max,array,ndarray,ones_like

    # Enforce arrays
    float_input_mass = not isinstance(m1,(ndarray,list,tuple))
    if float_input_mass:
        m1 = array([m1]);     m2 = array([m2])
    float_input_chi = not isinstance(chi1,(ndarray,list,tuple))
    if float_input_chi:
        chi1 = chi1*ones_like(m1); chi2 = chi2*ones_like(m2)

    #
    L = len( m1 )
    if  (L != len(m2)) or (len(chi1)!=len(chi2)) :
        error( 'lengths of input parameters not same' )

    # Prepare for swap / allocate output
    m1_   = array(m2);   m2_   = array(m1)
    chi1_ = array(chi2); chi2_ = array(chi1)

    #
    for k in range(L):

        # Enforce m1 > m2
        if (m1[k] < m2[k]):

            m1_[k] = m2[k]
            m2_[k] = m1[k]

            chi1_[k] = chi2[k]
            chi2_[k] = chi1[k]

    #
    if float_input_mass:
        m1_   = m1_[0];   m2_   = m2_[0]
    if float_input_chi:
        chi1_ = chi1_[0]; chi2_ = chi2_[0]

    #
    return (m1_,m2_,chi1_,chi2_)


#
def teukolsky_angular_adjoint_rule(aw,Alm,allow_warning=True):
    '''
    The adjoint of teukolskys angular equation is simply its complex conjugate
    '''
    from numpy import conj

    warning('The angular ajoint should only be envoked when there is no interest in the radial problem. If this is indeed the setting in which we wish to use the angular adjoint, then please turn adjoint off via "adjoint=False", and manually conjugate the output of angular related quantities (ie frequency and separation constant). Applying radial and angular adjoint options concurrently happens to be redundant.')
    return ( conj(aw), conj(Alm) )

#
def teukolsky_radial_adjoint_rule(s,w,Alm):
    '''
    The adjoint of teukolskys radial equation is ( s->-s,A->conj(A)+2s )
    '''
    from numpy import conj
    return ( -s, w, 2*s+conj(Alm) )


# Define function that returns the recursion coefficients as functions of an integer index
def leaver_mixed_ahelper( l,m,s,awj,awk,Bjk,london=1,verbose=False,adjoint=False ):
    '''
    Let L(awj) be the spheroidal angular operator without the eigenvalue.
    Let Sk be the eigenvector of L(awk)
    Here we store the recursion functions needed to solve:
    ( L(awj) + Bjk ) Sk == 0
    Where Bjk is a complex valued constant.
    The implication here is that while L(awk)Sk = -Ak as is handled in leaver_ahelper,
    Sk is also an aigenvector of L(awj)
    '''

    error('This functionality is based on an incorrect premise. Do not use related functions and options.')

    # Import usefuls
    from numpy import exp,sqrt

    # If the adjoint equation is of interest, apply the adjoint rule
    if adjoint:
        awj,Alm = teukolsky_angular_adjoint_rule(awj,Alm)

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # ANGULAR
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    if london==1:

        '''
        S(u) = exp( a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](1+u)^k )
        '''

        # Use abs of singular exponents AND write recursion functions so that the
        # appropriate physical solution is always used
        k1 = 0.5*abs(m-s)
        k2 = 0.5*abs(m+s)
        # As output from Mathematica
        a_alpha = lambda k:	-2*(1 + k)*(1 + k + 2*k1)
        a_beta  = lambda k:	-Bjk + k + k1 - 2*awk*(1 + 2*k + 2*k1) + k2 + (k + k1 + k2)**2 - s - (awj + s)**2
        a_gamma = lambda k:  2*(awk*(-awk + k + k1 + k2) + awj*(awj + s))
        # Exponential pre scale for angular function evaluation
        scale_fun_u = lambda COSTH: exp( awk * COSTH )
        # Define how the exopansion variable relates to u=cos(theta)
        u2v_map = lambda U: 1+U

    elif london==-1:

        '''
        S(u) = exp( - a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](1+u)^k )
        '''

        # Use abs of singular exponents AND write recursion functions so that the
        # appropriate physical solution is always used
        k1 = 0.5*abs(m-s)
        k2 = 0.5*abs(m+s)
        # As output from Mathematica
        a_alpha = lambda k:	2*(1 + k)*(1 + k + 2*k2)
        a_beta  = lambda k:	-Bjk + k + k1 + k2 + (k + k1 + k2)**2 - 2*awk*(1 + 2*k + 2*k2) - (awj - s)**2 - s
        a_gamma = lambda k: -2*(awj**2 + awk*(-awk + k + k1 + k2) - awj*s)
        # Exponential pre scale for angular function evaluation
        scale_fun_u = lambda COSTH: exp( -awk * COSTH )
        # Define how the exopansion variable relates to u=cos(theta)
        u2v_map = lambda U: U-1

    else:

        error('Unknown input option. Must be -1 or 1 corresponding to the sign of the exponent in the desired solution form.')

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # Package for output
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    if (k1<0) or (k2<0):
        print( 'k1 = '+str(k1))
        print( 'k2 = '+str(k2))
        error('negative singular exponent!')

    # Construct answer
    ans = (k1,k2,a_alpha,a_beta,a_gamma,scale_fun_u,u2v_map)

    # Return answer
    return ans


# Define function that returns the recursion coefficients as functions of an integer index
def leaver_ahelper( l,m,s,aw,Alm,london=False,verbose=False,adjoint=False ):
    '''
    Note that we will diver from Leaver's solution by handling the angular singular exponents differently than Leaver has. To use leaver's solution set london=False.
    '''

    # Import usefuls
    from numpy import exp,sqrt,ndarray,cos,array

    # Determine if the user wishes to consider the mixed problem
    mixed = isinstance(aw,(tuple,list,ndarray))
    if mixed:
        mixed = 2==len(aw)
        if len(aw)>2: error('Iterable aw found, but it is not of length 2 as requirede to consider the mixed eigenvalue problem.')
    # Interface with leaver_mixed_ahelper
    if mixed:
        # Unpack aw values. Note that awj lives in the operator, awk lives in the eigenfunction
        awj,awk = aw
        if london==False: london=1
        alert('Retrieving recurion functions for mixed the problem',verbose=verbose)
        return leaver_mixed_ahelper( l,m,s,awj,awk,Alm,london=london,verbose=verbose,adjoint=adjoint )

    # If the adjoint equation is of interest, apply the adjoint rule
    if adjoint:
        aw,Alm = teukolsky_angular_adjoint_rule(aw,Alm)

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # ANGULAR
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    if london:

        if london==1:

            '''
            S(u) = exp( a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](1+u)^k )
            '''

            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	-2*(1 + k)*(1 + k + 2*k1)
            a_beta  = lambda k:	-Alm - aw**2 - 2*aw*(1 + 2*k + 2*k1 + s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k:  2.0*aw*( k + k1+k2 + s )
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: 1+U
            # Define starting variable transformation variable
            theta2u_map = lambda TH: cos(TH)
            #
            scale_fun_u = lambda U: (1+U)**k1 * (1-U)**k2 * exp( aw * U )

        elif london==4:

            '''
            Solution to angular equation if (a*w)^2 term in potential is removed
            '''
            # alert('Not using (aw)^2 term in potential')
            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	-2*(1 + k)*(1 + k + 2*k1)
            a_beta  = lambda k:	-Alm - 2*aw*(1 + 2*k + 2*k1 + s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k: 2*aw*(-aw + k + k1 + k2 + s)
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: 1+U
            # Define starting variable transformation variable
            theta2u_map = lambda TH: cos(TH)
            #
            scale_fun_u = lambda U: (1+U)**k1 * (1-U)**k2 * exp( aw * U )

        elif london==3:

            '''
            Solution to adjoint equation where w is replaced with 1j*d/dt
            S(u) = exp( a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](1+u)^k )
            '''

            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	-2*(1 + k)*(1 + k + 2*k1)
            a_beta  = lambda k:	-Alm - aw**2 - 2*aw*(1 + 2*k + 2*k1 - s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k: 2*aw*(k + k1 + k2 - s)
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: 1+U
            # Define starting variable transformation variable
            theta2u_map = lambda TH: cos(TH)
            #
            scale_fun_u = lambda U: (1+U)**k1 * (1-U)**k2 * exp( aw * U )

        elif london==-1:

            '''
            S(u) = exp( - a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](u-1)^k )
            '''

            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	2*(1 + k)*(1 + k + 2*k2)
            a_beta  = lambda k:	-Alm - aw**2 - 2*aw*(1 + 2*k + 2*k2 - s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k: -2*aw*(k + k1 + k2 - s)
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: U-1
            # Define starting variable transformation variable
            theta2u_map = lambda TH: cos(TH)
            #
            scale_fun_u = lambda U: (1+U)**k1 * (1-U)**k2 * exp( -aw * U )

        elif london==2:

            '''
            u = aw*cos(theta)
            S(u) = exp( u ) (aw+u)^k1 (aw-u)^k2 Sum( a[k](aw+u)^k )
            '''

            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	-2*aw*(1 + k)*(1 + k + 2*k1)
            a_beta  = lambda k:	-Alm - aw**2 - 2*aw*(1 + 2*k + 2*k1 + s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k: 2*(k + k1 + k2 + s)
            # Define starting variable transformation variable
            theta2u_map = lambda TH: aw*cos(TH)
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: U+aw
            #
            scale_fun_u = lambda U: (array(aw+U,dtype=complex))**k1 * (array(aw-U,dtype=complex))**k2 * exp( U )

        elif london==-2:

            '''
            u = aw*cos(theta)
            S(u) = exp( -u ) (aw+u)^k1 (aw-u)^k2 Sum( a[k](-aw+u)^k )
            '''

            # Use abs of singular exponents AND write recursion functions so that the
            # appropriate physical solution is always used
            k1 = 0.5*abs(m-s)
            k2 = 0.5*abs(m+s)
            # Use Leaver's form for the recurion functions
            a_alpha = lambda k:	2*aw*(1 + k)*(1 + k + 2*k2)
            a_beta  = lambda k:	-Alm - aw**2 - 2*aw*(1 + 2*k + 2*k2 - s) + (k + k1 + k2 - s)*(1 + k + k1 + k2 + s)
            a_gamma = lambda k: -2*(k + k1 + k2 - s)
            # Define starting variable transformation variable
            theta2u_map = lambda TH: aw*cos(TH)
            # Define how the exopansion variable relates to u=cos(theta)
            u2v_map = lambda U: U-aw
            #
            scale_fun_u = lambda U: (array(aw+U,dtype=complex))**k1 * (array(aw-U,dtype=complex))**k2 * exp( -U )

        else:

            error('Unknown input option.')

    else:

        '''
        S(u) = exp( a w u ) (1+u)^k1 (1-u)^k2 Sum( a[k](1+u)^k )
        '''

        # Use abs of singular exponents AND write recursion functions so that the
        # appropriate physical solution is always used
        k1 = 0.5*abs(m-s)
        k2 = 0.5*abs(m+s)
        # Use Leaver's form for the recurion functions
        a_alpha = lambda k:	-2.0 * (k+1.0) * (k+2.0*k1+1.0)
        a_beta  = lambda k:	k*(k-1.0) \
                            + 2.0*k*( k1+k2+1.0-2.0*aw ) \
                            - ( 2.0*aw*(2.0*k1+s+1.0)-(k1+k2)*(k1+k2+1) ) \
                            - ( aw*aw + s*(s+1.0) + Alm )
        a_gamma = lambda k:   2.0*aw*( k + k1+k2 + s )
        # Define how the exopansion variable relates to u=cos(theta)
        u2v_map = lambda U: 1+U
        # Define starting variable transformation variable
        theta2u_map = lambda TH: cos(TH)
        #
        scale_fun_u = lambda U: (1+U)**k1 * (1-U)**k2 * exp( aw * U )

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # Package for output
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    if (k1<0) or (k2<0):
        print( 'k1 = '+str(k1))
        print( 'k2 = '+str(k2))
        error('negative singular exponent!')

    # Construct answer
    ans = (k1,k2,a_alpha,a_beta,a_gamma,scale_fun_u,u2v_map,theta2u_map)

    # Return answer
    return ans


#
def leaver_rhelper( l,m,s,a,w,Alm, london=True, verbose=False, adjoint=False ):

    # Import usefuls
    from numpy import sqrt, exp

    #
    if adjoint:
        s,w,Alm = teukolsky_radial_adjoint_rule(s,w,Alm)

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # RADIAL
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    london=False # set london false here becuase we expect leaver's version to be faster
    if london:
        # There is only one solution that satisfies the boundary
        # conditions at the event horizon and infinity.
        p1 = p2 = 1
        b  = sqrt(1.0-4.0*a*a)
        r_alpha = lambda k: 1 + k**2 - s + k*(2 - s - 1j*w) + ((2*1j)*a*m + k*((2*1j)*a*m - 1j*w) - 1j*w)/b - 1j*w
        r_beta  = lambda k: lambda k: -1 - Alm - 2*k**2 - s + k*(-2 + (4*1j)*w) + (2*1j)*w - 2*a*m*w + (4 - a**2)*w**2 + ((-2*1j)*a*m + (2*1j)*w - (4*1j)*a**2*w - 4*a*m*w + (4 - 8*a**2)*w**2 + k*((-4*1j)*a*m + (4*1j - (8*1j)*a**2)*w))/b
        r_gamma = lambda k: k**2 + k*(s - (3*1j)*w) - (2*1j)*s*w - 2*w**2 + (k*((2*1j)*a*m - 1j*w) + 4*a*m*w - 2*w**2)/b
        # Exponential pre scale for radial function evaluation
        r_exp_scale = lambda r: exp( aw * r )
    else:
        # There is only one solution that satisfies the boundary
        # conditions at the event horizon and infinity.
        p1 = p2 = 1
        # Precompute usefuls
        b  = sqrt(1.0-4.0*a*a)
        c_param = 0.5*w - a*m
        #
        c0    =         1.0 - s - 1.0j*w - (2.0j/b) * c_param
        c1    =         -4.0 + 2.0j*w*(2.0+b) + (4.0j/b) * c_param
        c2    =         s + 3.0 - 3.0j*w - (2.0j/b) * c_param
        c3    =         w*w*(4.0+2.0*b-a*a) - 2.0*a*m*w - s - 1.0 \
                        + (2.0+b)*1j*w - Alm + ((4.0*w+2.0j)/b) * c_param
        c4    =         s + 1.0 - 2.0*w*w - (2.0*s+3.0)*1j*w - ((4.0*w+2.0*1j)/b)*c_param
        # Define recursion functions
        r_alpha = lambda k:	k*k + (c0+1)*k + c0
        r_beta  = lambda k:   -2.0*k*k + (c1+2.0)*k + c3
        r_gamma = lambda k:	k*k + (c2-3.0)*k + c4 - c2 + 2.0
        # Exponential pre scale for radial function evaluation
        r_exp_scale = lambda r: exp( aw * r )

    return p1,p2,r_alpha,r_beta,r_gamma,r_exp_scale


# Define function that returns the recursion coefficients as functions of an integer index
def leaver_helper( l,m,s,a,w,Alm, london=True, verbose=False, adjoint=False ):
    '''
    Note that we will diver from Leaver's solution by handling the angular singular exponents differently than Leaver has. To use leaver's solution set london=False.
    '''

    # Import usefuls
    from numpy import exp,sqrt

    # Predefine useful quantities
    aw = a*w

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # ANGULAR
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # Use lower level module
    k1,k2,a_alpha,a_beta,a_gamma,scale_fun_u,u2v_map,theta2u_map = leaver_ahelper( l,m,s,a*w,Alm, london=london, verbose=verbose, adjoint=adjoint )

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # RADIAL
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # Use lower level module
    p1,p2,r_alpha,r_beta,r_gamma,r_exp_scale = leaver_rhelper( l,m,s,a,w,Alm, london=london, verbose=verbose, adjoint=adjoint )

    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #
    # Package for output
    # ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~ #

    # Construct answer
    ans = { 'angulars':(k1,k2,a_alpha,a_beta,a_gamma,scale_fun_u,u2v_map,theta2u_map),
            'radials': (p1,p2,r_alpha,r_beta,r_gamma,r_exp_scale) }

    # Return answer
    return ans


# Equation 27 of Leaver '86
# Characteristic Eqn for Spheroidal Radial Functions
def leaver27( a, l, m, w, Alm, s=-2.0, vec=False, mpm=False, adjoint=False, tol=1e-10,london=True,verbose=False, **kwargs ):

    '''
    Equation 27 of Leaver '86
    Characteristic Eqn for Spheroidal Radial Functions
    - LLondon
    '''

    from numpy import complex256 as dtyp

    # Enforce Data Type
    a = dtyp(a)
    w = dtyp(w)
    Alm = dtyp(Alm)

    # alert('s=%i'%s)
    # if s != 2:
    #     error('wrong spin')

    #
    pmax = 5e2

    #
    if mpm:
        from mpmath import sqrt
    else:
        from numpy import sqrt

    # global c0, c1, c2, c3, c4, alpha, beta, gamma, l_min

    #
    l_min = l-max(abs(m),abs(s)) # VERY IMPORTANT


    # ------------------------------------------------ #
    # Radial parameter defs
    # ------------------------------------------------ #
    _,_,alpha,beta,gamma,_ = leaver_rhelper( l,m,s,a,w,Alm, london=london, verbose=verbose, adjoint=adjoint )

    #
    v = 1.0
    for p in range(l_min+1):
        v = beta(p) - ( alpha(p-1.0)*gamma(p) / v )

    #
    aa = lambda p:   -alpha(p-1.0+l_min)*gamma(p+l_min)
    bb = lambda p:   beta(p+l_min)
    u,state = lentz(aa,bb,tol)
    u = beta(l_min) - u

    #
    x = v-u
    if vec:
        x = [x.real,x.imag]

    #
    return x


# Equation 21 of Leaver '86
# Characteristic Eqn for Spheroidal Angular Functions
def leaver21( a, l, m, w, Alm, s=-2.0, vec=False, adjoint=False,tol=1e-10,london=True,verbose=False, **kwargs ):
    '''
    Equation 21 of Leaver '86
    Characteristic Eqn for Spheroidal Angular Functions
    - LLondon
    '''

    #
    pmax = 5e2

    #
    l_min = l-max(abs(m),abs(s)) # VERY IMPORTANT

    '''# NOTE: Here we do NOT pass the adjoint keyword, as it we will adjuncticate(?) in leaver27 for the radial equation, and it would be redundant to adjuncticate(??) twice. '''
    k1,k2,alpha,beta,gamma,_,_,_ = leaver_ahelper( l,m,s,a*w,Alm, london=london, verbose=verbose, adjoint=False )

    #
    v = 1.0
    for p in range(l_min+1):
        v = beta(p) - (alpha(p-1.0)*gamma(p) / v)

    #
    aa = lambda p: -alpha(p-1.0+l_min)*gamma(p+l_min)
    bb = lambda p: beta(p+l_min)
    u,state = lentz(aa,bb,tol)
    u = beta(l_min) - u

    #
    x = v-u
    if vec:
        x = [x.real,x.imag]

    #
    return x



#
def leaver_2D_workfunction( j, l, m, cw, s, tol=1e-10 ):

    # Import Maths
    from numpy import log,exp,linalg,array
    from scipy.optimize import root,fmin,minimize
    from positive import alert,red,warning,leaver_workfunction

    error('function must be rewritten to evaluate the angular constraint given possible frequency values, and using sc_leaver to estimate the separation constant (with a guess?)')
    # Try using fmin
    # Define the intermediate work function to be used for this iteration
    fun = lambda X: log(linalg.norm(  leaver21( jf,l,m, cw, X[0]+1j*X[1], s=s )  ))
    foo  = fmin( fun, guess, disp=False, full_output=True, ftol=tol )
    sc = foo[0][0]+1j*foo[0][1]
    __lvrfmin2__ = exp(foo[1])

    # given A(cw), evaluate leaver27

    # return output of leaver27
    return None



# Work function for QNM solver
def leaver_workfunction( j, l, m, state, s=-2, mpm=False, adjoint=False, tol=1e-10, use21=True, use27=True, london=None ):
    '''
    work_function_to_zero = leaver( state )

    state = [ complex_w complex_eigenval ]
    '''

    #
    from numpy import complex128
    if mpm:
        import mpmath
        mpmath.mp.dps = 8
        dtyp = mpmath.mpc
    else:
        from numpy import complex256 as dtyp


    # alert('s=%i'%s)

    # Unpack inputs
    a = dtyp(j)/2.0                 # Change from M=1 to M=1/2 mass convention

    #
    complex_w = 2.0*dtyp(state[0])  # Change from M=1 to M=1/2 mass convention
    ceigenval = dtyp(state[1])

    #
    if len(state) == 4:
        complex_w = 2 * (dtyp(state[0])+1.0j*dtyp(state[1]))
        ceigenval = dtyp(state[2]) + 1.0j*dtyp(state[3])

    # concat list outputs
    #print adjoint

    # x = leaver21(a,l,m,complex_w,ceigenval,vec=True,s=s,mpm=mpm,adjoint=adjoint,tol=tol) +  leaver27(a,l,m,complex_w,ceigenval,vec=True,s=s,mpm=mpm,adjoint=adjoint,tol=tol)

    x = []
    if use21:
        x += leaver21(a,l,m,complex_w,ceigenval,vec=True,s=s,mpm=mpm,adjoint=adjoint,tol=tol,london=london)
    if use27:
        x += leaver27(a,l,m,complex_w,ceigenval,vec=True,s=s,mpm=mpm,adjoint=adjoint,tol=tol,london=london)
    if not x:
        error('use21 or/and use27 must be true')


    #
    x = [ complex128(e) for e in x ]
    # print x

    # if s!=2:
    #     alert('s=%i'%s)
    #     error('something is off with spin weight propogation')

    #
    return x




# Given a separation constant, find a frequency*spin such that the spheroidal series expansion converges
def aw_leaver( Alm, l, m, s,tol=1e-9, london=True, verbose=False, guess=None, awj=None, awk=None, adjoint=False  ):
    '''
    Given a separation constant, find a frequency*spin such that the spheroidal series expansion converges
    '''

    # Import Maths
    from numpy import log,exp,linalg,array
    from scipy.optimize import root,fmin,minimize
    from positive import alert,red,warning,leaver_workfunction
    from numpy import complex128 as dtyp

    #
    l_min = l-max(abs(m),abs(s)) # VERY IMPORTANT

    #
    if awj and awk:
        error('When specifying spin-frequencies for the mixed problem, only one of the two frequencies must specified.')
    if awj:
        internal_leaver_ahelper = lambda AWK: leaver_ahelper( l,m,s,[awj,AWK],Alm+s, london=london, verbose=verbose, adjoint=adjoint )
    elif awk:
        internal_leaver_ahelper = lambda AWJ: leaver_ahelper( l,m,s,[AWJ,awk],Alm+s, london=london, verbose=verbose, adjoint=adjoint )
    else:
        internal_leaver_ahelper = lambda AW: leaver_ahelper( l,m,s,AW,Alm+s, london=london, verbose=verbose, adjoint=adjoint )

    #
    def action(aw):
        _,_,alpha,beta,gamma,_,_ = internal_leaver_ahelper(aw)
        v = 1.0
        for p in range(l_min+1):
            v = beta(p) - (alpha(p-1.0)*gamma(p) / v)
        aa = lambda p: -alpha(p-1.0+l_min)*gamma(p+l_min)
        bb = lambda p: beta(p+l_min)
        u,state = lentz(aa,bb,tol)
        u = beta(l_min) - u
        x = v-u
        if verbose: print('err = '+str(abs(x)))
        x = array([x.real,x.imag],dtype=float).ravel()
        return x

    if verbose: print('')

    # Try using root
    # Define the intermediate work function to be used for this iteration
    indirect_action = lambda STATE: action(STATE[0]+1j*STATE[1])
    # indirect_action = lambda STATE: log( 1.0 + abs( array(  action(STATE[0]+1j*STATE[1])  ) ) )
    aw_guess = 0.5 + 1j * 0.01 if guess is None else guess
    guess = [aw_guess.real,aw_guess.imag]
    foo  = root( indirect_action, guess, tol=tol )
    aw = foo.x[0]+1j*foo.x[1]
    fmin = foo.fun
    foo.action = indirect_action
    retry = ( 'not making good progress' in foo.message.lower() ) or ( 'error' in foo.message.lower() )

    # # Try using fmin
    # # Define the intermediate work function to be used for this iteration
    # indirect_action = lambda STATE: linalg.norm(action(STATE[0]+1j*STATE[1]))**2
    # Alm_guess = scberti(aw,l,m,s)
    # guess = [Alm_guess.real,Alm_guess.imag]
    # foo  = fmin( indirect_action, guess, disp=False, full_output=True, ftol=tol )
    # Alm = foo[0][0]+1j*foo[0][1]
    # fmin = foo[1]
    # retry = fmin>1e-3

    # alert('err = '+str(fmin))
    if retry:
        warning('retry!')

    return (aw,fmin,retry,foo)





# Compute perturbed Kerr separation constant given a frequency
def sc_leaver( aw, l, m, s,tol=1e-10, london=True, s_included=False, verbose=False, adjoint=False, __CHECK__=True  ):
    '''
    Given (aw, l, m, s), compute and return separation constant.
    '''

    # Import Maths
    from numpy import log,exp,linalg,array
    from scipy.optimize import root,fmin,minimize
    from positive import alert,red,warning,leaver_workfunction
    from numpy import complex128 as dtyp

    #
    p_min = l-max(abs(m),abs(s)) # VERY IMPORTANT

    #
    def action(Alm):
        _,_,alpha,beta,gamma,_,_,_ = leaver_ahelper( l,m,s,aw,Alm, london=london, verbose=verbose, adjoint=False )
        v = 1.0
        for p in range(p_min+1):
            v = beta(p) - (alpha(p-1.0)*gamma(p) / v)
        aa = lambda p: -alpha(p-1.0+p_min)*gamma(p+p_min)
        bb = lambda p: beta(p+p_min)
        u,state = lentz(aa,bb,tol)
        u = beta(p_min) - u
        x = v-u
        if verbose: print('err = '+str(abs(x)))
        x = array([x.real,x.imag],dtype=float).ravel()
        return x

    if verbose: print('')

    # Try using root
    # Define the intermediate work function to be used for this iteration
    indirect_action = lambda STATE: action(STATE[0]+1j*STATE[1])
    # indirect_action = lambda STATE: log( 1.0 + abs( array(  action(STATE[0]+1j*STATE[1])  ) ) )
    aw_guess = aw if isinstance(aw,(float,complex)) else aw
    Alm_guess = scberti(aw_guess,l,m,s,adjoint=False)
    guess = [Alm_guess.real,Alm_guess.imag]
    foo  = root( indirect_action, guess, tol=tol )
    Alm = foo.x[0]+1j*foo.x[1]
    fmin = indirect_action( foo.fun )
    retry = ( 'not making good progress' in foo.message.lower() ) or ( 'error' in foo.message.lower() )

    # # Try using fmin
    # # Define the intermediate work function to be used for this iteration
    # indirect_action = lambda STATE: linalg.norm(action(STATE[0]+1j*STATE[1]))**2
    # Alm_guess = scberti(aw,l,m,s)
    # guess = [Alm_guess.real,Alm_guess.imag]
    # foo  = fmin( indirect_action, guess, disp=False, full_output=True, ftol=tol )
    # Alm = foo[0][0]+1j*foo[0][1]
    # fmin = foo[1]
    # retry = fmin>1e-3

    # Given the structure of the spheroidal harmonic differential equation for perturbed Kerr, we have a choice to include a factor of s in the potential, or in the eigenvalue. There's good reason to consider it a part of the latter as s->-s has the action of leaving the eigenvalue unchanged.
    if s_included:
        Alm = Alm + s

    # Impose check on equivalence class
    if __CHECK__:
        if (l==abs(s)+3):
            (Alm_,fmin_,retry_,foo_) = sc_leaver( -aw, l, -m, s,tol=tol, london=london, s_included=s_included, verbose=verbose, adjoint=adjoint, __CHECK__=False  )
            if linalg.norm(fmin_)<linalg.norm(fmin):
                (Alm,fmin,retry,foo) = (Alm_,fmin_,retry_,foo_)
            if verbose:
                warning('Strange behavior has been noticed for this equivalence class of l and s. We have checked to verify that the optimal root is used here.')

    # alert('err = '+str(fmin))
    if retry:
        warning('retry! needed in sc_leaver')

    return (Alm,fmin,retry,foo)




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
''' Implement Berti's approximation for the separation constants '''
# NOTE that Beuer et all 1977 also did it
# NOTE Relevant references:
# * Primary: arxiv:0511111v4
# * Proc. R. Soc. Lond. A-1977-Breuer-71-86
# * E_Seidel_1989_Class._Quantum_Grav._6_012
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
def scberti(acw, l,m,s=-2,adjoint=False):

    '''
    Estimate the Shpheroidal Harmonic separation constant using results of a general perturbative expansion. Primary reference: arxiv:0511111v4 Equation 2.3
    '''

    #
    from numpy import zeros,array,sum

    # If the adjoint equation is of interest, apply the adjoint rule
    if adjoint:
        acw,_ = teukolsky_angular_adjoint_rule(acw,0)


    # NOTE that the input here is acw = jf*complex_w
    f = zeros((6,),dtype='complex128')

    #
    l,m,s = float(l),float(m),float(s)

    f[0] = l*(l+1) - s*(s+1)
    f[1] = - 2.0 * m * s*s / ( l*(l+1) )

    hapb = max( abs(m), abs(s) )
    hamb = m*s/hapb
    h = lambda ll: (ll*ll - hapb*hapb) * (ll*ll-hamb*hamb) * (ll*ll-s*s) / ( 2*(l-0.5)*ll*ll*ll*(ll-0.5) )

    f[2] = h(l+1) - h(l) - 1
    f[3] = 2*h(l)*m*s*s/((l-1)*l*l*(l+1)) - 2*h(l+1)*m*s*s/(l*(l+1)*(l+1)*(l+2))
    f[4] = m*m*s*s*s*s*( 4*h(l+1)/(l*l*(l+1)*(l+1)*(l+1)*(l+1)*(l+2)*(l+2)) \
                        - 4*h(l)/((l-1)*(l-1)*l*l*l*l*(l+1)*(l+1)) ) \
                        - (l+2)*h(l+1)*h(l+2)/(2*(l+1)*(2*l+3)) \
                        + h(l+1)*h(l+1)/(2*l+2) + h(l)*h(l+1)/(2*l*l+2*l) - h(l)*h(l)/(2*l) \
                        + (l-1)*h(l-1)*h(l)/(4*l*l-2*l)

    '''
    # NOTE that this term diverges for l=2, and the same is true for the paper's f[6]
    f[5] = m*m*m*s*s*s*s*s*s*( 8.0*h(l)/(l*l*l*l*l*l*(l+1)*(l+1)*(l+1)*(l-1)*(l-1)*(l-1)) \
                             - 8.0*h(l+1)/(l*l*l*(l+1)*(l+1)*(l+1)*(l+1)*(l+1)*(l+1)*(l+2)*(l+2)*(l+2)) ) \
              + m*s*s*h(l) * (-h(l+1)*(7.0*l*l+7*l+4)/(l*l*l*(l+2)*(l+1)*(l+1)*(l+1)*(l-1)) \
                              -h(l-1)*(3.0*l-4)/(l*l*l*(l+1)*(2*l-1)*(l-2)) ) \
              + m*s*s*( (3.0*l+7)*h(l+1)*h(l+2)/(l*(l+1)*(l+1)*(l+1)*(l+3)*(2*l+3)) \
                                 -(3.0*h(l+1)*h(l+1)/(l*(l+1)*(l+1)*(l+1)*(l+2)) + 3.0*h(l)*h(l)/(l*l*l*(l-1)*(l+1)) ) )
    '''

    # Calcualate the series sum, and return output
    return sum( array([ f[k] * acw**k for k in range(len(f)) ]) )



#
def prod(A,B,TH,WEIGHT_FUNCTION=None):
    from numpy import sin,pi
    if WEIGHT_FUNCTION is None:
        WEIGHT_FUNCTION = 2*pi*sin(TH)
    INTGRND = A.conj()*B*WEIGHT_FUNCTION
    RE_INTGRND = INTGRND.real
    IM_INTGRND = INTGRND.imag
    TH0,TH1 = lim(TH)
    return spline(TH,RE_INTGRND).integral(TH0,TH1) + 1j*spline(TH,IM_INTGRND).integral(TH0,TH1)

# ------------------------------------------------------------------ #
# Calculate the inner-product between a spherical and spheroidal harmonic
# ------------------------------------------------------------------ #
def ysprod( jf,
            ll,
            mm,
            lmn,
            s = -2,
            N=2**9,         # Number of points in theta to use for trapezoidal integration
            theta = None,   # Pre computed theta domain
            use_nr_convention = True,
            verbose=False):

    #
    from positive import slm,sYlm as ylm,warning
    from numpy import pi,linspace,trapz,sin,sqrt
    from positive import spline,lim

    #
    th = theta if not (theta is None) else linspace(0,pi,N)
    ph = 0
    # prod = lambda A,B: 2*pi * trapz( A.conj()*B*sin(th), x=th )

    # Validate the lmn input
    if len(lmn) not in (3,6):
        error('the lmn input must contain only l m and n; note that the p label is handeled here by the sign of jf')

    # Unpack 1st order mode labels
    if len(lmn)==3:
        l,m,n = lmn
        so=False
        m_eff = m
    elif len(lmn)==6:
        l,m,n,_,l2,m2,n2,_ = lmn
        so=True
        m_eff = m+m2
        if verbose: warning('Second Order mode given. An ansatz will be used for what this harmonic looks like: products of the related 1st order spheroidal functions. This ansatz could be WRONG.','ysprod')


    #
    if m_eff==mm:
        #
        y = ylm(s,ll,mm,th,ph)
        _s = slm(jf,l,m,n,th,ph,s=s,norm=False,__rescale__=False) if not so else slm(jf,l,m,n,th,ph,norm=False,__rescale__=False)*slm(jf,l2,m2,n2,th,ph,norm=False,__rescale__=False,use_nr_convention=use_nr_convention)
        ss = _s / sqrt(prod(_s,_s,th))
        ans = prod( y,ss,th ) # note that this is consistent with the matlab implementation modulo the 2*pi convention
    else:
        # print m,m_eff,mm,list(lmnp)
        ans = 0
        # raise

    return ans


# ------------------------------------------------------------------ #
# Calculate inner product of two spheroidal harmonics at a a given spin
# NOTE that this inner product does not rescale the spheroidal functions so that the spherical normalization is recovered
# ------------------------------------------------------------------ #
def ssprod(jf, z1, z2, N=2**8,verbose=False,theta=None, london=False,s=-2,aw=None, use_nr_convention=True ):

    '''
    To be used outside of slm for general calculation of inner-products. This is NOT the function slm uses to normalize the spheroidal harmonics.
    '''

    #
    from positive import prod
    from numpy import linspace,pi,sqrt

    #
    def helper(x1,x2,th=None):
        if th is None: th = linspace(0,pi,len(x1))
        c1 = sqrt( prod(x1,x1,th) )
        c2 = sqrt( prod(x2,x2,th) )
        s1_ = s1/c1
        s2_ = s2/c2
        return prod(s1_,s2_,th)

    #
    if len(z1)==len(z2)==3:
        #
        l1,m1,n1 = z1
        l2,m2,n2 = z2
        #
        if m1 == m2 :
            th, phi = pi*linspace(0,1,N), 0
            s1 = slm( jf, l1, m1, n1, th, phi, norm=False, __rescale__=False, london=london,aw=aw, use_nr_convention=use_nr_convention,s=s )
            s2 = slm( jf, l2, m2, n2, th, phi, norm=False, __rescale__=False, london=london,aw=aw, use_nr_convention=use_nr_convention,s=s ) if (l2,m2,n2) != (l1,m1,n1) else s1
            #
            ans = helper(s1,s2,th)
        else:
            ans = 0
    else:
        s1,s2 = z1,z2
        if theta is None:
            error('must input theta vals when inputting vectors')
        if len(s1)!=len(s2):
            error('If 2nd and 3rd inputs are spheroidal function then they must be the ame length, and it is assumed that the span theta between 0 and pi')
        ans = helper(s1,s2,theta)

    return ans


# ------------------------------------------------------------------ #
# Calculate inner product of two spheroidal harmonics at a a given spin
# NOTE that this inner product does not rescale the spheroidal functions so that the spherical normalization is recovered
# ------------------------------------------------------------------ #
def internal_ssprod( jf, z1, z2, s=-2, verbose=False, N=2**9, london=False,aw=None ):
    '''
    To be used by slm to normalize output
    '''

    #
    from numpy import linspace,trapz,array,pi,sin

    #
    l1,m1,n1 = z1
    l2,m2,n2 = z2

    #
    if m1 == m2 :
        #
        th, phi = pi*linspace(0,1,N), 0
        # # Handle optional inner product definition
        # if prod is None:
        #     prod = lambda A,B: 2*pi * trapz( A.conj()*B*sin(th), x=th )
        #
        s1 = slm( jf, l1, m1, n1, th, phi,s=s, norm=False, __rescale__=False, london=london,aw=aw )
        s2 = slm( jf, l2, m2, n2, th, phi,s=s, norm=False, __rescale__=False, london=london,aw=aw ) if (l2,m2,n2) != (l1,m1,n1) else s1
        #
        ans = prod(s1,s2,th)
    else:
        ans = 0

    #
    return ans
    


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
''' Calculate set of spheroidal harmonic duals '''
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
def slm_dual_set( jf, l, m, n, theta, phi, s=-2, lmax=8, lmin=2, aw=None, verbose=False, tol=None, conjugate_expansion=True ):
    '''
    Construct set of dual-spheroidals
    '''

    # Import usefuls
    from numpy import array,pi,arange,linalg,dot,conj,zeros,double

    # Warn if l is large
    if lmax>8: warning('Input of lmax>8 found. The output of this function is increasingly inaccurate for lmax>8 due to numerical errors at the default value of the tol keyword input.')
        
    #
    if not isinstance(phi,(float,int,double)):
        error('phi must be number; zero makes sense as the functions phi dependence is exp(1j*m*phi), and so can be added externally')

    #
    if lmin<abs(m): lmin = max(abs(m),abs(s))

    # -------------------------------------- #
    # Construct a space of spheroidals as a starting basis
    # -------------------------------------- #
    lnspace = []; nmin=0; nmax=0
    lspace = arange( lmin,lmax+1 )
    nspace = arange( nmin,nmax+1 )
    for j,ll in enumerate(lspace):
        for k,nn in enumerate(nspace):
            lnspace.append( (ll,nn) )
    Sspace = []
    for ln in lnspace:
        ll,nn = ln
        Sspace.append( slm( jf, ll, m, nn, theta, phi, s=s, verbose=verbose, aw=aw, use_nr_convention=False, tol=tol ) )
    Sspace = array(Sspace)

    # Handle sanity-check option for whether to expand in spheroidals or their complex conjugates
    if conjugate_expansion:

        ##########################################
        # Expand in spheroidal conjugates        #
        ##########################################

        # -------------------------------------- #
        # Construct Gram matrix for spheroidals
        # -------------------------------------- #
        u = zeros( (len(lnspace),len(lnspace)), dtype=complex )
        for j,ln1 in enumerate(lnspace):
            for k,ln2 in enumerate(lnspace):
                s1 = Sspace[j,:]
                s2 = Sspace[k,:]
                # Compute the normalized inner-product
                u[j,k] = ssprod( None, s1, s2.conj(), theta=theta, aw=None, use_nr_convention=False )
        # -------------------------------------- #
        # Invert and conjugate
        # -------------------------------------- #
        v = linalg.pinv(u)

        # -------------------------------------- #
        # Use v to project dual functions out of regular ones
        # -------------------------------------- #
        aSspace = dot(v,Sspace.conj())

    else:

        #########################################
        # Expand in regular spheroidals         #
        #########################################

        # -------------------------------------- #
        # Construct Gram matrix for spheroidals
        # -------------------------------------- #
        u = zeros( (len(lnspace),len(lnspace)), dtype=complex )
        for j,ln1 in enumerate(lnspace):
            for k,ln2 in enumerate(lnspace):
                s1 = Sspace[j,:]
                s2 = Sspace[k,:]
                u[j,k] = ssprod(jf, s1, s2, theta=theta, aw=aw, use_nr_convention=False )
        # -------------------------------------- #
        # Invert and conjugate
        # -------------------------------------- #
        v = conj(linalg.pinv(u))

        # -------------------------------------- #
        # Use v to project dual functions out of regular ones
        # -------------------------------------- #
        aSspace = dot(v,Sspace.conj())

    #
    foo,bar = {},{}
    for k,(l,n) in enumerate(lnspace):
        foo[ (l,n) if len(nspace)>1 else l ] = aSspace[k,:]
        bar[ (l,n) if len(nspace)>1 else l ] =  Sspace[k,:]
    #
    ans = {}
    ans['Slm'] = bar
    ans['AdjSlm'] = foo
    ans['lnspace'] = lnspace
    ans['Sspace'] = Sspace
    ans['aSspace'] = aSspace
    ans['SGramian'] = u
    return ans




def depreciated_slm_dual_set_slow( jf, l, m, n, theta, phi, s=-2, lmax=8, lmin=2, aw=None, verbose=False ):
    '''
    Construct set of dual-spheroidals
    Things that could spped this function up:
    * calculate Sspace first, and then use it to directly calculate gramian rather than calling ssprod
    '''
    # Import usefuls
    from numpy import array,pi,arange,linalg,dot,conj,zeros
    #error('This function is still being written')
    # -------------------------------------- #
    # Construct Gram matrix for spheroidals
    # -------------------------------------- #
    lnspace = []; nmin=0; nmax=0
    lspace = arange( lmin,lmax+1 )
    nspace = arange( nmin,nmax+1 )
    for j,ll in enumerate(lspace):
        for k,nn in enumerate(nspace):
            lnspace.append( (ll,nn) )
    u = zeros( (len(lnspace),len(lnspace)), dtype=complex )
    for j,ln1 in enumerate(lnspace):
        for k,ln2 in enumerate(lnspace):
            l1,n1 = ln1
            l2,n2 = ln2
            z1 = (l1,m,n1)
            z2 = (l2,m,n2)
            u[j,k] = ssprod(jf, z1, z2, N=2**10, aw=aw, use_nr_convention=False)
    # -------------------------------------- #
    # Invert and conjugate
    # -------------------------------------- #
    v = conj(linalg.pinv(u))
    # -------------------------------------- #
    # Construct a space of spheroidals as a starting basis
    # -------------------------------------- #
    Sspace = []
    for ln in lnspace:
        ll,nn = ln
        Sspace.append( slm( jf, ll, m, nn, theta, phi, s=s, verbose=verbose, aw=aw, use_nr_convention=False ) )
    Sspace = array(Sspace)
    # -------------------------------------- #
    # Use v to project dual functions out of regular ones
    # -------------------------------------- #
    aSspace = dot(v,Sspace)
    #
    foo,bar = {},{}
    for k,(l,n) in enumerate(lnspace):
        foo[ (l,n) if len(nspace)>1 else l ] = aSspace[k,:]
        bar[ (l,n) if len(nspace)>1 else l ] =  Sspace[k,:]
    #
    ans = {}
    ans['Slm'] = bar
    ans['AdjSlm'] = foo
    ans['lnspace'] = lnspace
    ans['Sspace'] = Sspace
    ans['aSspace'] = aSspace
    ans['SGramian'] = u
    return ans


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
''' Spheroidal Harmonic angular function via leaver's sum FOR m>0 '''
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
def slpm( jf,               # Dimentionless spin parameter
          l,
          m,
          n,
          theta,            # Polar spherical harmonic angle
          phi,              # Azimuthal spherical harmonic angle
          s       = -2,     # Spin weight
          __rescale__ = True, # Internal usage only: Recover scaling of spherical harmonics in zero spin limit
          norm = True,     # If true, normalize the waveform
          output_iterations = False,
          __aw_sc__ = None, # optional frequency and separation parameter pair
          london = False,   # toggle for which series solution to use (they are all largely equivalent)
          aw = None,        # when not none, the separation constant will be found automatically
          adjoint=False,
          tol=None,
          verbose = False ):# Be verbose

    #
    from positive import red
    from positive import leaver as lvr
    from positive import rgb,lim,leaver_workfunction,cyan,alert,pylim,sYlm,error,internal_ssprod
    from numpy import complex256, cos, ones, mean, isinf, pi, exp, array, ndarray, unwrap, angle, linalg, sqrt, linspace, sin, float128
    # from scipy.misc import factorial as f
    from scipy.integrate import trapz

    #
    if m<0: error('this low level routine is only valid for m>0; use slm() for general m cases')

    # Ensure that thet is iterable
    if not isinstance(theta,ndarray):
        theta = array([theta])

    #
    if __aw_sc__ is None:

        if aw is None:

            # Validate the spin input
            if isinstance(jf,int): jf = float(jf)

            # Use tabulated cw and sc values from the core package
            cw,sc = lvr( jf, l, m, n, s=s )

            # Validate the QNM frequency and separation constant used
            lvrtol=1e-4
            lvrwrk = linalg.norm( leaver_workfunction(jf,l,m,[cw.real,cw.imag,sc.real,sc.imag],adjoint=adjoint,s=s, london=1) )
            if lvrwrk>lvrtol:
                msg = 'There is a problem in '+cyan('kerr.core.leaver')+'. The values output are not consistent with leaver''s characteristic equations within %f.\n%s\n# The mode is (jf,l,m,n)=(%f,%i,%i,%i)\n# The leaver_workfunction value is %s\n%s\n'%(lvrtol,'#'*40,jf,l,m,n,red(str(lvrwrk)),'#'*40)
                error(msg,'slm')
            # If verbose, check the consisitency of the values used
            if verbose:
                msg = 'Checking consistency of QNM frequncy and separation constant used against Leaver''s constraint equations:\n\t*  '+cyan('leaver_workfunction(jf=%1.4f,l,m,[cw,sc]) = %s'%(jf,lvrwrk))+'\n\t*  cw = %s\n\t*  sc = %s'%(cw,sc)
                alert(msg,'slm')

            # Define dimensionless deformation parameter
            aw = complex256( jf*cw )

        else:

            #
            from numpy import complex128 as dtyp
            sc = sc_leaver( dtyp(aw), l, m, s, verbose=verbose, adjoint=False, london=london)[0]

    else:

        # Use input values
        aw,sc = __aw_sc__


    #
    from numpy import complex128 as dtyp
    sc2 = sc_leaver( dtyp(aw), l, m, s, verbose=verbose,adjoint=False, london=london, tol=tol)[0]
    if abs(sc2-sc)>1e-3:
        print('aw  = '+str(aw))
        print('sc  = '+str(sc))
        print('sc2 = '+str(sc2))
        print('err = '+str(abs(sc2-sc)))
        warning('input separation constant not consistent with angular constraint, so we will use a different one to give you an answer that converges.')
        sc = sc2

    # ------------------------------------------------ #
    # Angular parameter functions
    # ------------------------------------------------ #

    # Retrieve desired information from central location
    k1,k2,alpha,beta,gamma,scale_fun_u,u2v_map,theta2u_map = leaver_ahelper( l,m,s,aw,sc, london=london, verbose=verbose )

    # ------------------------------------------------ #
    # Calculate the angular eighenfunction
    # ------------------------------------------------ #

    # Variable map for theta
    u = theta2u_map(theta)
    # Calculate the variable used for the series solution
    v = u2v_map( u )

    # the non-sum part of eq 18
    X = ones(u.shape,dtype=complex256)
    X = X * scale_fun_u(u)

    # initial series values
    a0 = 1.0 # a choice, setting the norm of Slm

    a1 = -beta(0)/alpha(0)

    C = 1.0
    C = C*((-1)**(max(-m,-s)))*((-1)**l)

    # Apply normalization
    if norm:
        if __aw_sc__: error('this function is not configured to output normalized harmonics when manually specifying the deformation parameter and separation consant')
        z = (l,m,n)
        if norm == -1:
            # Scale such that spherical counterpart is normalized
            C /= ysprod(jf,l,m,z,s,london=london)
        else:
            C /= sqrt( internal_ssprod(jf,z,z,s,london=london,aw=aw) )


    # the sum part
    done = False
    Y = a0*ones(u.shape,dtype=complex256)
    Y = Y + a1*v
    k = 1
    kmax = 5e3
    err,yy = [],[]
    et2=1e-8 if tol is None else tol
    max_a = max(abs(array([a0,a1])))
    v_pow_k = v
    while not done:
        k += 1
        j = k-1
        a2 = -1.0*( beta(j)*a1 + gamma(j)*a0 ) / alpha(j)
        v_pow_k = v_pow_k*v
        dY = a2*v_pow_k
        Y += dY
        xx = max(abs( dY ))

        #
        if output_iterations:
            yy.append( C*array(Y)*X*exp(1j*m*phi) )
            err.append( xx )

        k_is_too_large = k>kmax
        done = (k>=l) and ( (xx<et2 and k>30) or k_is_too_large )
        done = done or xx<et2
        a0 = a1
        a1 = a2

    # together now
    S = X*Y*exp(1j*m*phi)

    # Use same sign convention as spherical harmonics
    # e.g http://en.wikipedia.org/wiki/Spin-weighted_spherical_harmonics#Calculating
    S = C * S

    # Warn if the series did not appear to converge
    if k_is_too_large:
        warning('The while-loop exited becuase too many iterations have passed. The series may not converge for given inputs.')

    #
    return S,yy,err



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
''' Spheroidal Harmonic angular function via leaver's sum '''
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
def slm(  jf,               # Dimentionless spin parameter
          l,
          m,
          n,
          theta,            # Polar spherical harmonic angle
          phi,              # Azimuthal spherical harmonic angle
          s       = -2,     # Spin weight
          plot    = False,  # Toggel for plotting
          __rescale__ = True, # Internal usage only: Recover scaling of spherical harmonics in zero spin limit
          norm = True,     # If true, normalize the waveform
          ax = None,        # axes handles for plotting to; must be length 1(single theta) or 2(many theta)
          __aw_sc__ = None,
          aw = None,        # when not none, the separation constant will be found automatically
          london = False,
          use_nr_convention = True, # Toggle whether to use NR convention for multipoles
          tol = None,
          verbose = False ):# Be verbose

    # Setup plotting backend
    if plot:
        import matplotlib as mpl
        mpl.rcParams['lines.linewidth'] = 0.8
        mpl.rcParams['font.family'] = 'serif'
        mpl.rcParams['font.size'] = 16
        mpl.rcParams['axes.labelsize'] = 16

    #
    from positive import red
    from positive import leaver as lvr
    # from kerr.formula.ksm2_slm_norm import CC as normcfit
    # from kerr.formula.ksm2_sc import SC as scfit
    # from kerr.formula.ksm2_cw import CW as cwfit
    from positive import rgb,lim,leaver_workfunction,cyan,alert,pylim,sYlm,error,internal_ssprod
    from numpy import complex256,cos,ones,mean,isinf,pi,exp,array,ndarray,unwrap,angle,linalg,sqrt,linspace,sin,float128
    from matplotlib.pyplot import subplot,gca,xlabel,ylabel,xlim,ylim,title,figure,sca
    from matplotlib.pyplot import plot as plot_
    # from scipy.misc import factorial as f
    from scipy.integrate import trapz

    #
    if m<0:
        if use_nr_convention:
            S,yy,err = slpm( jf, l, -m, n, pi-theta, pi+phi, s=s, __rescale__=__rescale__, norm=norm, output_iterations=plot, verbose=verbose, __aw_sc__=__aw_sc__, london=london, aw=aw, tol=tol )
            S = ((-1)**(l+m)) * S.conj()
            warning('NR convention being used for m<0 multipole. This results in a spheroidal function that does not satisfy Teukolsky\'s equation with the given labeling. To disable this warning, use keyword input use_nr_convention=False.')
        else:
            aw = -aw
            m = -m
            s = -s
            S,yy,err = slpm( jf, l, m, n, theta, phi, s=s, __rescale__=__rescale__, norm=norm, output_iterations=plot, verbose=verbose, __aw_sc__=__aw_sc__, london=london, aw=aw, tol=tol )
    else:
        S,yy,err = slpm( jf, l, m, n, theta, phi, s=s, __rescale__=__rescale__, norm=norm, output_iterations=plot, verbose=verbose, __aw_sc__=__aw_sc__, london=london, aw=aw, tol=tol )

    #
    if plot:
        def ploterr():
            plot_( err, '-ob',mfc='w',mec='b' )
            gca().set_yscale("log", nonposy='clip')
            title( '$l = %i$, $m = %i$, $jf = %s$'%(l,m,'%1.4f'%jf if jf is not None else 'n/a') )
            ylabel('Error Estimate')
            xlabel('Iteration #')
        if isinstance(theta,(float,int)):
            if ax is None:
                figure(figsize=3*array([3,3]))
            else:
                sca(ax[0])
            ploterr()
        elif isinstance(theta,ndarray):
            if ax is None:
                figure(figsize=3*array([6,2.6]))
                subplot(1,2,1)
            else:
                sca(ax[0])
            ploterr()
            if ax is not None:
                sca(ax[-1])
            else:
                subplot(1,2,2)
            clr = rgb( max(len(yy),1),reverse=True )
            for k,y in enumerate(yy):
                plot_(theta,abs(y),color=clr[k],alpha=float(k+1)/len(yy))
            plot_(theta,abs(S),'--k')
            pylim(theta,abs(S))
            fs=20
            xlabel(r'$\theta$',size=fs)
            ylabel(r'$|S_{%i%i%i}(\theta,\phi)|$'%(l,m,n),size=fs )
            title(r'$\phi=%1.4f$'%phi)

    #
    if len(S) is 1:
        return S[0]

    #
    return S


# Validate list of l,m values
def validate_lm_list( lm_space,s=-2 ):

    # Validate list of l,m values
    lmin = abs(s)
    msg = 'lm_space should be iterable of iterables of length 2; eg [(2,2),(3,2)]'
    if not isiterable(lm_space): error(msg)
    for dex,j in enumerate(lm_space):
        if isiterable(j):
            if len(j)!=2:
                error(msg)
            else:
                l,m = j
                if (not isinstance(l,int)) or (not isinstance(m,int)):
                    error('values fo l and m must be integers')
                else:
                    lm_space[dex] = (l,m)
        else:
            error(msg)
    msg = 'lm_space must be a ordered iterable of unique elements'
    if len(set(lm_space))!=len(lm_space):
        error(msg)

    #
    return None

# Calculte matrix of spherical spheroidal harmonic inner-products (sYlm|Slmn)
def ysprod_matrix( jf, lm_space, N_theta=128, __aw_sc__=None, s=-2 ):
    '''

    == Calculte matrix of spherical spheroidal harmonic inner-products (sYlm|Slmn) ==

    |a) = sum_j a_j |Yj) # Spherical representation with j=(L,M)
        = sum_k b_k |Sk) # Spheroidal rep with k=(l,m,n)

    -->

    a_j = (Yj|a)
        = sum_k b_k (Yj|Sk)

    * (Yj|Sk) is treated as a matrix and the rest vectors
    * (Yj|Sk) will be enforced to square:

        A. IF lm_space is of length N, THEN sigma = (Yj|Sk) will be NxN
        B. We CHOOSE k = (L,M,0) so that (Yj|Sk) is square
        C. In the point above, we explicitely disregard overtones; they may be added in a future version of this method (if the dimensionality can be sorted ...)

    USAGE
    ---
    sigma = ysprod_matrix( jf, lm_space, N_theta=128, __aw_sc__=None, s=-2 )


    londonl@mit.edu 2019

    '''

    # Import usefuls
    from positive import slm,sYlm,prod
    from numpy import pi,linspace,trapz,sin,sqrt,zeros_like,ones,conj

    # Validate list of l,m values
    validate_lm_list(lm_space,s=s)

    #
    theta = linspace( 0, pi, N_theta )
    phi = 0

    # Define index space for spheroidal basis
    k_space = []
    for l,m in lm_space:
        k_space.append( (l,m,0) )

    #
    K = len(lm_space)
    ans = ones( (K,K), dtype=complex )

    #
    for j,(l,m) in enumerate(lm_space):

        #
        sYj = sYlm(s,l,m,theta,phi)
        y = sYj/sqrt(prod(sYj,sYj,theta))

        for k in range( len(k_space) ):

            #
            l_,m_,n_ = k_space[k]

            #
            if m==m_:
                Sk = slm(jf,l_,m_,n_,theta,phi,norm=False,__aw_sc__=__aw_sc__)
                s_ = Sk/sqrt(prod(Sk,Sk,theta))
                ans[j,k] = conj(prod( y,s_, theta ))
            else:
                ans[j,k] = 0
            # print (L,M),(l,m,n), ans[j,k]

    #
    return ans


# Given a dictionary of spherical multipole moment data values (i.e. l,m: spherical_multipole_float ), calculate the spheroidal counterpart
def ys_change( spherical_basis_vector, lm_space, dimensionless_spin, N_theta=128, __aw_sc__=None, return_sigma=False ):
    '''
    Given a dictionary of spherical multipole moment data values (i.e. l,m: spherical_multipole_float ), calculate the spheroidal counterpart
    '''

    #
    from numpy import dot
    from numpy.linalg import inv,pinv,lstsq

    # Calculate the mixing matrix
    sigma = ysprod_matrix( dimensionless_spin, lm_space, N_theta=N_theta, __aw_sc__=__aw_sc__ )

    # Take the inverse of the mixing matrix
    inv_sigma = pinv( sigma )

    # Calculate the spheroidal vector
    spheroidal_basis_vector = dot( inv_sigma, spherical_basis_vector )

    # Return desired information
    if return_sigma:
        return spheroidal_basis_vector,sigma
    else:
        return spheroidal_basis_vector

#
def calc_spheroidal_multipoles( domain_vals, spherical_multipole_dict, dimensionless_spin_series, s=-2, verbose=False ):
    '''
    Low level function to convert spherical multipole time or frequency series to spheroidal ones GIVEN the dimensionless_spin_series associated with the spacetime. This method interprets the spacetime as Kerr at all radii. All values of m in the spherical multipole dict must be identical
    '''

    # Import usefuls
    from numpy import diff,array,ones_like,mod

    # Collect spherical multipole indeces and sort by l
    j_space = spherical_multipole_dict.keys()
    # Validate list of l,m values
    validate_lm_list(j_space,s=s)
    # Sort
    j_space.sort(key=lambda X: X[0])

    #
    if len(set( [ j[-1] for j in j_space ] ))>1:
        error( 'all values of m in the spherical multipole dict must be identical' )

    #
    spheroidal_multipole_dict = { (l,m,0):ones_like(spherical_multipole_dict[l,m]) for l,m in spherical_multipole_dict }
    sigmas = []

    #
    q=0
    for u,v in enumerate(domain_vals):

        #
        q += 1
        if 0==mod(q,51):
            if verbose: print('.',end='')

        # Construct spherical basis vector
        spherical_basis_vector = [ spherical_multipole_dict[j][u] for j in j_space ]

        # Get the associated spin
        dimensionless_spin = dimensionless_spin_series[u]

        #
        spheroidal_basis_vector,sigma = ys_change( spherical_basis_vector, j_space, dimensionless_spin, return_sigma=True )

        #
        sigmas.append(sigma)

        #
        for dex,(l,m) in enumerate(j_space):

            #
            k = (l,m,0)

            #
            spheroidal_multipole_dict[k][u] = spheroidal_basis_vector[dex]

    #
    sigmas = array(sigmas)


    return spheroidal_multipole_dict,sigmas



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
'''Class for boxes in complex frequency space'''
# The routines of this class assist in the solving and classification of
# QNM solutions
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
class cwbox:
    # ************************************************************* #
    # This is a class to fascilitate the solving of leaver's equations varying
    # the real and comlex frequency components, and optimizing over the separation constants.
    # ************************************************************* #
    def __init__(this,
                 l,m,               # QNM indeces
                 cwr,               # Center coordinate of real part
                 cwc,               # Center coordinate of imag part
                 wid,               # box width
                 hig,               # box height
                 res = 50,          # Number of gridpoints in each dimension
                 parent = None,     # Parent of current object
                 sc = None,         # optiional holder for separatino constant
                 verbose = False,   # be verbose
                 maxn = None,       # Overtones with n>maxn will be actively ignored. NOTE that by convention n>=0.
                 smallboxes = True, # Toggle for using small boxes for new solutions
                 s = -2,            # Spin weight
                 adjoint = False,
                 **kwargs ):
        #
        from numpy import array,complex128,meshgrid,float128
        #
        this.verbose,this.res = verbose,res
        # Store QNM ideces
        this.l,this.m,this.s = l,m,s
        # Set box params
        this.width,this.height = None,None
        this.setboxprops(cwr,cwc,wid,hig,res,sc=sc)
        # Initial a list of children: if a box contains multiple solutions, then it is split according to each solutions location
        this.children = [this]
        # Point the object to its parent
        this.parent = parent
        #
        this.__jf__ = []
        # temp grid of separation constants
        this.__scgrid__ = []
        # current value of scalarized work-function
        this.__lvrfmin__ = None
        # Dictionary for high-level data: the data of all of this object's children is collected here
        this.data = {}
        this.dataformat = '{ ... (l,m,n,tail_flag) : { "jf":[...],"cw":[...],"sc":[...],"lvrfmin":[...] } ... }'
        # Dictionary for low-level data: If this object is fundamental, then its data will be stored here in the same format as above
        this.__data__ = {}
        # QNM label: (l,m,n,t), NOTE that "t" is 0 if the QNM is not a power-law tail and 1 otherwise
        this.__label__ = ()
        # Counter for the number of times map hass benn called on this object
        this.mapcount = 0
        # Default value for temporary separation constant
        this.__sc__ = 4.0
        # Maximum overtone label allowed.  NOTE that by convention n>=0.
        this.__maxn__ = maxn
        #
        this.adjoint = adjoint
        #
        this.__removeme__ = False
        #
        this.__smallboxes__ = smallboxes

    # Set box params & separation constant center
    def setboxprops(this,cwr,cwc,wid,hig,res,sc=None,data=None,pec=None):
        # import maths and other
        from numpy import complex128,float128,array,linspace
        import matplotlib.patches as patches
        # set props for box geometry
        this.center = array([cwr,cwc])
        this.__cw__ = cwr + 1j*cwc          # Store cw for convinience

        # Boxes may only shrink. NOTE that this is usefull as some poetntial solutions, or unwanted solutions may be reomved, and we want to avoid finding them again. NOTE that this would be nice to implement, but it currently brakes the root finding.
        this.width,this.height  = float128( abs(wid) ),float128( abs(hig) )
        # if (this.width is None) or (this.height is None):
        #     this.width,this.height  = float128( abs(wid) ),float128( abs(hig) )
        # else:
        #     this.width,this.height  = min(float128( abs(wid) ),this.width),min(this.height,float128( abs(hig) ))

        this.limit  = array([this.center[0]-this.width/2.0,       # real min
                             this.center[0]+this.width/2.0,       # real max
                             this.center[1]-this.height/2.0,      # imag min
                             this.center[1]+this.height/2.0])     # imag max
        this.wr_range = linspace( this.limit[0], this.limit[1], res )
        this.wc_range = linspace( this.limit[2], this.limit[3], res )
        # Set patch object for plotting. NOTE the negative sign exists here per convention
        if None is pec: pec = 'k'
        this.patch = patches.Rectangle( (min(this.limit[0:2]), min(-this.limit[2:4]) ), this.width, this.height, fill=False, edgecolor=pec, alpha=0.4, linestyle='dotted' )
        # set holder for separation constant value
        if sc is not None:
            this.__sc__ = sc
        # Initiate the data holder for this box. The data holder will contain lists of spin, official cw and sc values
        if data is not None:
            this.data=data

    # Map the potential solutions in this box
    def map(this,jf):

        # Import useful things
        from kerr import localmins # finds local minima of a 2D array
        from kerr.basics import alert,green,yellow,cyan,bold,magenta,blue
        from numpy import array,delete,ones

        #%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#
        # Add the input jf to the list of jf values. NOTE that this is not the primary recommended list for referencing jf. Please use the "data" field instead.
        this.__jf__.append(jf)
        #%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#%%#

        #

        if this.verbose:
            if this.parent is None:
                alert('\n\n# '+'--'*40+' #\n'+blue(bold('Attempting to map qnm solutions for: jf = %1.8f'%(jf)))+'\n# '+'--'*40+' #\n','map')
            else:
                print('\n# '+'..'*40+' #\n'+blue('jf = %1.8f,  label = %s'%(jf,this.__label__))+'\n# '+'..'*40+' #')

        # Map solutions using discrete grid
        if this.isfundamental():
            # Brute-force calculate solutions to leaver's equations
            if this.verbose: alert('Solvinq Leaver''s Eqns over grid','map')
            this.__x__,this.__scgrid__ = this.lvrgridsolve(jf)
            # Use a local-min finder to estimate the qnm locations for the grid of work function values, x
            if this.verbose: alert('Searching for local minima. Ignoring mins on boundaries.','map')
            this.__localmin__ = localmins(this.__x__,edge_ignore=True)
            if this.verbose: alert('Number of local minima found: %s.'%magenta('%i'%(len(array(this.__localmin__)[0]))),'map')
            # If needed, split the box into sub-boxes: Give the current box children!
            this.splitcenter() # NOTE that if there is only one lcal min, then no split takes place
            # So far QNM solutions have been estimates mthat have discretization error. Now, we wish to refine the
            # solutions using optimization.
            if this.verbose: alert('Refining QNM solution locations using a hybrid strategy.','map')
            this.refine(jf)
        else:
            # Map solutions for all children
            for child in [ k for k in this.children if this is not k ]:
                child.map(jf)

        # Collect QNM solution data for this BH spin. NOTE that only non-fundamental objects are curated
        if this.verbose: alert('Collecting final QNM solution information ...','map')
        this.curate(jf)

        # Remove duplicate solutions
        this.validatechildren()

        #
        if this.verbose: alert('Mapping of Kerr QNM with (l,m)=(%i,%i) within box now complete for this box.' % (this.l,this.m ) ,'map')

        # Some book-keeping on the number of times this object has been mapped
        this.mapcount += 1


    # For the given bh spin, collect all QNM frequencies and separation constants within the current box
    # NOTE that the outputs are coincident lists
    def curate(this,jf):

        #
        from numpy import arange,array,sign

        #
        children = this.collectchildren()
        cwlist,sclist = [ child.__cw__ for child in children ],[ child.__sc__ for child in children ]
        if this.isfundamental():
            cwlist.append( this.__cw__ )
            sclist.append( this.__sc__ )

        # sort the output lists by the imaginary part of the cw values
        sbn = lambda k: abs( cwlist[k].imag ) # Sort By Overtone(N)
        space = arange( len(cwlist) )
        map_  = sorted( space, key=sbn )
        std_cwlist = array( [ cwlist[k] for k in map_ ] )
        std_sclist = array( [ sclist[k] for k in map_ ] )

        # ---------------------------------------------------------- #
        # Separate positive, zero and negative frequency solutions
        # ---------------------------------------------------------- #

        # Solutions with frequencies less than this value will be considered to be power-laws
        pltol = 0.01
        # Frequencies
        if jf == 0: jf = 1e-20 # NOTE that here we ensure that 0 jf is positive only for BOOK-KEEPING purposes
        sorted_cw_pos = list(  std_cwlist[ (sign(std_cwlist.real) == sign(jf)) * (abs(std_cwlist.real)>pltol) ]  )
        sorted_cw_neg = list(  std_cwlist[ (sign(std_cwlist.real) ==-sign(jf)) * (abs(std_cwlist.real)>pltol) ]  )
        sorted_cw_zro = list(  std_cwlist[ abs(std_cwlist.real)<=pltol ]  )

        # Create a dictionary between (cw,sc) and child objects
        A,B = {},{}
        for child in children:
            A[child] = ( child.__cw__, child.__sc__ )
            B[ A[child] ] = child
        #
        def inferlabel( cwsc ):
            cw,sc = cwsc[0],cwsc[1]
            ll = this.l
            if abs(cw.real)<pltol :
                # power-law decay
                tt = 1
                nn = sorted_cw_zro.index( cw )
                mm = this.m
                pp = 0
            else:
                tt = 0
                if sign(jf)==sign(cw.real):
                    # prograde
                    mm = this.m
                    nn = sorted_cw_pos.index( cw )
                    pp = 1
                else:
                    # retrograde
                    mm = -1 * this.m
                    nn = sorted_cw_neg.index( cw )
                    pp = -1
            #
            return (ll,mm,nn,tt,pp)

        # ---------------------------------------------------------- #
        # Create a dictionary to keep track of potential solutions
        # ---------------------------------------------------------- #
        label = {}
        invlabel = {}
        for child in children:
            cwsc = ( child.__cw__, child.__sc__ )
            child.state = [ child.__cw__.real, child.__cw__.imag,  child.__sc__.real, child.__sc__.imag ]
            __label__ = inferlabel( cwsc )
            label[child] = __label__
            invlabel[__label__] = child
            child.__label__ = label[child]

        #
        this.labelmap = label
        this.inverse_labelmap = invlabel
        '''
        IMPORTANT: Here it is assumed that the solutions will change in a continuous manner, and that after the first mapping, no new solutions are of interest, unless a box-split occurs.
        '''

        # Store the high-level data product
        for child in children:
            L = this.labelmap[child]
            if not L in this.data:
                this.data[ L ] = {}
                this.data[ L ][ 'jf' ] = [jf]
                this.data[ L ][ 'cw' ] = [ child.__cw__ ]
                this.data[ L ][ 'sc' ] = [ child.__sc__ ]
                this.data[ L ][ 'lvrfmin' ] = [ child.__lvrfmin__ ]
            else:
                this.data[ L ][ 'jf' ].append(jf)
                this.data[ L ][ 'cw' ].append(child.__cw__)
                this.data[ L ][ 'sc' ].append(child.__sc__)
                this.data[ L ][ 'lvrfmin' ].append(child.__lvrfmin__)
            # Store the information to this child also
            child.__data__['jf'] = this.data[ L ][ 'jf' ]
            child.__data__['cw'] = this.data[ L ][ 'cw' ]
            child.__data__['sc'] = this.data[ L ][ 'sc' ]
            child.__data__['lvrfmin'] = this.data[ L ][ 'lvrfmin' ]


    # Refine the box center using fminsearch
    def refine(this,jf):
        # Import useful things
        from numpy import complex128,array,linalg,log,exp,abs
        from scipy.optimize import fmin,root,fmin_tnc,fmin_slsqp
        from kerr.pttools import leaver_workfunction,scberti
        from kerr.basics import alert,say,magenta,bold,green,cyan,yellow
        from kerr import localmins # finds local minima of a 2D array

        #
        if this.isfundamental():
            # use the box center for refined minimization
            CW = complex128( this.center[0] + 1j*this.center[1] )
            # SC = this.__sc__
            SC = scberti( CW*jf, this.l, this.m, s=this.s )
            state = [ CW.real,CW.imag, SC.real,SC.imag ]

            #
            retrycount,maxretrycount,done = -1,1,False
            while done is False:

                #
                retrycount += 1

                #
                if retrycount==0:
                    alert(cyan('* Constructing guess using scberti-grid or extrap.'),'refine')
                    state = this.guess(jf,gridguess=state)
                else:
                    alert(cyan('* Constructing guess using 4D-grid or extrap.'),'refine')
                    state = this.guess(jf)

                # Solve leaver's equations using a hybrid strategy
                cw,sc,this.__lvrfmin__,retry = this.lvrsolve(jf,state)

                # If the root finder had some trouble, then mark this box with a warning (for plotting)
                done = (not retry) or (retrycount>=maxretrycount)
                #
                if retry:

                    newres = 2*this.res

                    if this.verbose:
                        msg = yellow( 'The current function value is %s. Retrying root finding for %ind time with higher resolution pre-grid, and brute-force 4D.'%(this.__lvrfmin__, retrycount+2) )
                        alert(msg,'refine')
                        # say('Retrying.','refine')

                    # Increase the resolution of the box
                    this.setboxprops(this.__cw__.real,this.__cw__.imag,this.width,this.height,newres,sc=this.__sc__)
                    # NOTE that the commented out code below is depreciated by the use of guess() above.
                    # # Brute force solve again
                    # this.__x__,this.__scgrid__ = this.lvrgridsolve(jf,fullopt=True)
                    # # Use the first local min as a guess
                    # this.__localmin__ = localmins(this.__x__,edge_ignore=True)
                    # state = this.grids2states()[0]

            # if this.verbose: print X.message+' The final function value is %s'%(this.__lvrfmin__)
            if this.verbose: print('The final function value is '+green(bold('%s'%(this.__lvrfmin__))))

            if this.verbose:
                print( '\n\t Geuss   cw: %s' % CW)
                print( '\t Optimal cw: %s' % cw)
                print( '\t Approx  sc: %s' % scberti( CW*jf, this.l, this.m ))
                print( '\t Geuss   sc: %s' % (state[2]+1j*state[3]))
                print( '\t Optimal sc: %s\n' % sc)

            # Set the core properties of the new box
            this.setboxprops( cw.real, cw.imag, this.width,this.height,this.res,sc=sc )

            # Rescale this object's boxes based on new centers
            this.parent.sensescale()

        else:
            #
            for child in [ k for k in this.children if this is not k ]:
                child.refine(jf)


    # Determine if the current object has more than itself as a child
    def isfundamental(this):
        return len(this.children) is 1


    # ************************************************************* #
    # Determin whether to split this box into sub-boxes (i.e. children)
    # and if needed, split
    # ************************************************************* #
    def splitcenter(this):
        from numpy import array,zeros,linalg,inf,mean,amax,amin,sqrt
        from kerr.basics import magenta,bold,alert,error,red,warning,yellow
        mins =  this.__localmin__
        num_solutions = len(array(mins)[0])
        if num_solutions > 1: # Split the box
            # for each min
            for k in range(len(mins[0])):

                # construct the center location
                kr = mins[1][k]; wr = this.wr_range[ kr ]
                kc = mins[0][k]; wc = this.wc_range[ kc ]
                sc = this.__scgrid__[kr,kc]
                # Determine the resolution of the new box
                res = int( max( 20, 1.5*float(this.res)/num_solutions ) )
                # Create the new child. NOTE that the child's dimensions will be set below using a standard method.
                child = cwbox( this.l,this.m,wr,wc,0,0, res, parent=this, sc=sc, verbose=this.verbose,s=this.s )
                # Add the new box to the current box's child list
                this.children.append( child )

            # NOTE that here we set the box dimensions of all children using the relative distances between them
            this.sensescale()

            # Now redefine the box size to contain all children
            # NOTE that this step exists only to ensure that the box always contains all of its children's centers
            children = this.collectchildren()
            wr = array( [ child.center[0] for child in children ] )
            wc = array( [ child.center[1] for child in children ] )
            width = amax(wr)-amin(wr)
            height = amax(wc)-amin(wc)
            cwr = mean(wr)
            cwc = mean(wc)
            this.setboxprops( cwr,cwc,width,height,this.res,sc=sc )

        elif num_solutions == 1:
            # construcut the center location
            k = 0 # there should be only one local min
            kr = mins[1][k]
            kc = mins[0][k]
            wr = this.wr_range[ kr ]
            wc = this.wc_range[ kc ]
            # retrieve associated separation constant
            sc  = this.__scgrid__[kr,kc]
            # Recenter the box on the current min
            this.setboxprops(wr,wc,this.width,this.height,this.res,sc=sc)
        else:
            #
            if len(this.__jf__)>3:
                alert('Invalid number of local minima found: %s.'% (magenta(bold('%s'%num_solutions))), 'splitcenter' )
                # Use the extrapolated values as a guess?
                alert(yellow('Now trying to use extrapolation, wrather than grid guess, to center the current box.'),'splitcenter')
                #
                guess = this.guess(this.__jf__[-1],gridguess=[1.0,1.0,4.0,1.0])
                wr,wc,cr,cc = guess[0],guess[1],guess[2],guess[3]
                sc = cr+1j*cc
                # Recenter the box on the current min
                this.setboxprops(wr,wc,this.width,this.height,this.res,sc=sc)
            else:
                warning('Invalid number of local minima found: %s. This box will be removed. NOTE that this may not be what you want, and further inspection may be warranted.'% (magenta(bold('%s'%num_solutions))), 'splitcenter' )
                this.__removeme__ = True


    # Validate children: Remove duplicates
    def validatechildren(this):
        #
        from numpy import linalg,array
        from kerr import alert,yellow,cyan,blue,magenta
        tol = 1e-6

        #
        if not this.isfundamental():

            #
            children = this.collectchildren()
            initial_count = len(children)

            # Remove identical twins
            for a,tom in enumerate( children ):
                for b,tim in enumerate( children ):
                    if b>a:
                        if linalg.norm(array(tom.center)-array(tim.center)) < tol:
                            if this.verbose:
                                msg = 'Removing overtone '+yellow('%s'%list(tim.__label__))+' becuase it has a twin.'
                                alert(msg,'validatechildren')
                            tim.parent.children.remove(tim)
                            del tim
                            break

            # Remove overtones over the max label
            if this.__maxn__ is not None:
                for k,child in enumerate(this.collectchildren()):
                    if child.__label__[2] > this.__maxn__:
                        if this.verbose:
                            msg = 'Removing overtone '+yellow('%s'%list(child.__label__))+' becuase its label is higher than the allowed value specified.'
                            alert(msg,'validatechildren')
                        this.labelmap.pop( child.__label__ , None)
                        child.parent.children.remove(child)
                        del child

            # Remove all boxes marked for deletion
            for child in this.collectchildren():
                if child.__removeme__:
                    this.labelmap.pop( child.__label__, None )
                    child.parent.children.remove( child )
                    del child

            #
            final_count = len( this.collectchildren() )
            #
            if this.verbose:
                if final_count != initial_count:
                    alert( yellow('%i children have been removed, and %i remain.') % (-final_count+initial_count,final_count) ,'validatechildren')
                else:
                    alert( 'All children have been deemed valid.', 'validatechildren' )


    # Method for collecting all fundamental children
    def collectchildren(this,children=None):
        #
        if children is None:
            children = []
        #
        if this.isfundamental():
            children.append(this)
        else:
            for child in [ k for k in this.children if k is not this ]:
                children += child.collectchildren()
        #
        return children


    # Method to plot solutions
    def plot(this,fig=None,show=False,showlabel=False):
        #
        from numpy import array,amin,amax,sign
        from matplotlib.pyplot import plot,xlim,ylim,xlabel,ylabel,title,figure,gca,text
        from matplotlib.pyplot import show as show_

        #
        children = this.collectchildren()
        wr = array( [ child.center[0] for child in children ] )
        wc =-array( [ child.center[1] for child in children ] )
        wr_min,wr_max = amin(wr),amax(wr)
        wc_min,wc_max = amin(wc),amax(wc)

        padscale = 0.15
        padr,padc = 1.5*padscale*(wr_max-wr_min), padscale*(wc_max-wc_min)
        wr_min -= padr; wr_max += padr
        wc_min -= padc; wc_max += padc
        #
        if fig is None:
            # fig = figure( figsize=12*array((wr_max-wr_min, wc_max-wc_min))/(wr_max-wr_min), dpi=200, facecolor='w', edgecolor='k' )
            fig = figure( figsize=12.0*array((4.5, 3))/4.0, dpi=200, facecolor='w', edgecolor='k' )
        #
        xlim( [wr_min,wr_max] )
        ylim( [wc_min,wc_max] )
        ax = gca()
        #
        for child in children:
            plot( child.center[0],-child.center[1], '+k', ms=10 )
            ax.add_patch( child.patch )
            if showlabel:
                text( child.center[0]+sign(child.center[0])*child.width/2,-(child.center[1]+child.height/2),
                      '$(%i,%i,%i,%i,%i)$'%(this.labelmap[child]),
                      ha=('right' if sign(child.center[0])<0 else 'left' ),
                      fontsize=10,
                      alpha=0.9 )
        #
        xlabel(r'$\mathrm{re}\;\tilde\omega_{%i%i}$'%(this.l,this.m))
        ylabel(r'-$\mathrm{im}\;\tilde\omega_{%i%i}$'%(this.l,this.m))
        title(r'$j_f = %1.6f$'%this.__jf__[-1],fontsize=18)
        #
        if show: show_()

    # ************************************************************* #
    # Solve leaver's equations in a given box=[wr_range,wc_range]
    # NOTE that the box is a list, not an array
    # ************************************************************* #
    def lvrgridsolve(this,jf=0,fullopt=False):
        # Import maths
        from numpy import linalg,complex128,ones,array
        from kerr.pttools import scberti
        from kerr.pttools import leaver_workfunction
        from scipy.optimize import fmin,root
        import sys

        # Pre-allocate an array that will hold work function values
        x = ones(  ( this.wc_range.size,this.wr_range.size )  )
        # Pre-allocate an array that will hold sep const vals
        scgrid = ones(  ( this.wc_range.size,this.wc_range.size ), dtype=complex128  )
        # Solve over the grid
        for i,wr in enumerate( this.wr_range ):
            for j,wc in enumerate( this.wc_range ):
                # Costruct the complex frequency for this i and j
                cw = complex128( wr+1j*wc )

                # # Define the intermediate work function to be used for this iteration
                # fun = lambda SC: linalg.norm( array(leaver_workfunction( jf,this.l,this.m, [cw.real,cw.imag,SC[0],SC[1]] )) )
                # # For this complex frequency, optimize over separation constant using initial guess
                # SC0_= scberti( cw*jf, this.l, this.m ) # Use Berti's analytic prediction as a guess
                # SC0 = [SC0_.real,SC0_.imag]
                # X  = fmin( fun, SC0, disp=False, full_output=True, maxiter=1 )
                # # Store work function value
                # x[j][i] = X[1]
                # # Store sep const vals
                # scgrid[j][i] = X[0][0] + 1j*X[0][1]

                if fullopt is False:

                    # Define the intermediate work function to be used for this iteration
                    fun = lambda SC: linalg.norm( array(leaver_workfunction( jf,this.l,this.m, [cw.real,cw.imag,SC[0],SC[1]], s=this.s, adjoint=this.adjoint )) )
                    # For this complex frequency, optimize over separation constant using initial guess
                    SC0_= sc_leaver( cw*jf, this.l, this.m, s=this.s, adjoint=False )[0]
                    SC0 = [SC0_.real,SC0_.imag]
                    # Store work function value
                    x[j][i] = fun(SC0)
                    # Store sep const vals
                    scgrid[j][i] = SC0_

                else:

                    SC0_= sc_leaver( cw*jf, this.l, this.m, s=this.s, adjoint=False )[0]
                    SC0 = [SC0_.real,SC0_.imag,0,0]
                    #cfun = lambda Y: [ Y[0]+abs(Y[3]), Y[1]+abs(Y[2]) ]
                    fun = lambda SC:leaver_workfunction( jf,this.l,this.m, [cw.real,cw.imag,SC[0],SC[1]], s=this.s, adjoint=this.adjoint )
                    X  = root( fun, SC0 )
                    scgrid[j][i] = X.x[0]+1j*X.x[1]
                    x[j][i] = linalg.norm( array(X.fun) )


            if this.verbose:
                sys.stdout.flush()
                print('.',end='')

        if this.verbose: print('Done.')
        # return work function values AND the optimal separation constants
        return x,scgrid


    # Convert output of localmin to a state vector for minimization
    def grids2states(this):

        #
        from numpy import complex128
        state = []

        #
        for k in range( len(this.__localmin__[0]) ):
            #
            kr,kc = this.__localmin__[1][k], this.__localmin__[0][k]
            cw = complex128( this.wr_range[kr] + 1j*this.wc_range[kc] )
            sc = complex128( this.__scgrid__[kr,kc] )
            #
            state.append( [cw.real,cw.imag,sc.real,sc.imag] )

        #
        return state


    # Get guess either from local min, or from extrapolation of past data
    def guess(this,jf,gridguess=None):
        #
        from kerr.pttools import leaver_workfunction
        from kerr.basics import alert,magenta,apolyfit
        from kerr import localmins
        from numpy import array,linalg,arange,complex128,allclose,nan
        from scipy.interpolate import InterpolatedUnivariateSpline as spline
        # Get a guess from the localmin
        if gridguess is None:
            this.__x__,this.__scgrid__ = this.lvrgridsolve(jf,fullopt=True)
            this.__localmin__ = localmins(this.__x__,edge_ignore=True)
            states = this.grids2states()
            if len(states):
                guess1 = states[0]
            else:
                error('The grid is empty.')
        else:
            guess1 = gridguess
        # Get a guess from extrapolation ( performed in curate() )
        guess2 = [ v for v in guess1 ]
        if this.mapcount > 3:
            # if there are three map points, try to use polynomial fitting to determine the state at the current jf value
            nn = len(this.__data__['jf'])
            order = min(2,nn)
            #
            xx = array(this.__data__['jf'])[-4:]
            #
            yy = array(this.__data__['cw'])[-4:]
            yr = apolyfit( xx, yy.real, order )(jf)
            yc = apolyfit( yy.real, yy.imag, order )(yr)
            cw = complex128( yr + 1j*yc )
            #
            zz = array(this.__data__['sc'])[-4:]
            zr = apolyfit( xx, zz.real, order  )(jf)
            zc = apolyfit( zz.real, zz.imag, order  )(zr)
            sc = complex128( zr + 1j*zc )
            #
            guess2 = [ cw.real, cw.imag, sc.real, sc.imag ]
        # Determine the best guess
        if not ( allclose(guess1,guess2) ):
            x1 = linalg.norm( leaver_workfunction( jf,this.l,this.m, guess1, s=this.s, adjoint=this.adjoint ) )
            x2 = linalg.norm( leaver_workfunction( jf,this.l,this.m, guess2, s=this.s, adjoint=this.adjoint ) )
            alert(magenta('The function value at guess from grid is:   %s'%x1),'guess')
            alert(magenta('The function value at guess from extrap is: %s'%x2),'guess')
            if x2 is nan:
                x2 = 100.0*x1
            if x1<x2:
                guess = guess1
                alert(magenta('Using the guess from the grid.'),'guess')
            else:
                guess = guess2
                alert(magenta('Using the guess from extrapolation.'),'guess')
        else:
            x1 = linalg.norm( leaver_workfunction( jf,this.l,this.m, guess1, s=this.s, adjoint=this.adjoint ) )
            guess = guess1
            alert(magenta('The function value at guess from grid is %s'%x1),'guess')

        # Recenter the box on the current guess
        wr,wc = guess[0],guess[1]
        sc = guess[2]+1j*guess[3]
        this.setboxprops(wr,wc,this.width,this.height,this.res,sc=sc)

        # Return the guess solution
        return guess


    # Determine whether the current box contains a complex frequency given an iterable whose first two entries are the real and imag part of the complex frequency
    def contains(this,guess):
        #
        cwrmin = min( this.limit[:2] )
        cwrmax = max( this.limit[:2] )
        cwcmin = min( this.limit[2:] )
        cwcmax = max( this.limit[2:] )
        #
        isin  = True
        isin = isin and ( guess[0]<cwrmax )
        isin = isin and ( guess[0]>cwrmin )
        isin = isin and ( guess[1]<cwcmax )
        isin = isin and ( guess[1]>cwcmin )
        #
        return isin


    # Try solving the 4D equation near a single guess value [ cw.real cw.imag sc.real sc.imag ]
    def lvrsolve(this,jf,guess,tol=1e-8):

        # Import Maths
        from numpy import log,exp,linalg,array
        from scipy.optimize import root,fmin,minimize
        from kerr.pttools import leaver_workfunction
        from kerr import alert,red,warning

        # Try using root
        # Define the intermediate work function to be used for this iteration
        fun = lambda STATE: log( 1.0 + abs(array(leaver_workfunction( jf,this.l,this.m, STATE, s=this.s, adjoint=this.adjoint ))) )
        X  = root( fun, guess, tol=tol )
        cw1,sc1 = X.x[0]+1j*X.x[1], X.x[2]+1j*X.x[3]
        __lvrfmin1__ = linalg.norm(array( exp(X.fun)-1.0 ))
        retry1 = ( 'not making good progress' in X.message.lower() ) or ( 'error' in X.message.lower() )


        # Try using fmin
        # Define the intermediate work function to be used for this iteration
        fun = lambda STATE: log(linalg.norm(  leaver_workfunction( jf,this.l,this.m, STATE, s=this.s, adjoint=this.adjoint )  ))
        X  = fmin( fun, guess, disp=False, full_output=True, ftol=tol )
        cw2,sc2 = X[0][0]+1j*X[0][1], X[0][2]+1j*X[0][3]
        __lvrfmin2__ = exp(X[1])
        retry2 = this.__lvrfmin__ > 1e-3

        # Use the solution that converged the fastest to avoid solutions that have wandered significantly from the initial guess OR use the solution with the smallest fmin
        if __lvrfmin1__ < __lvrfmin2__ : # use the fmin value for convenience
            cw,sc,retry = cw1,sc1,retry1
            __lvrfmin__ = __lvrfmin1__
        else:
            cw,sc,retry = cw2,sc2,retry2
            __lvrfmin__ = __lvrfmin2__


        # Always retry if the solution is outside of the box
        if not this.contains( [cw.real,cw.imag] ):
            warning('The proposed solution is outside of the box, and may now not correspond to the correct label.')
            # retry = True
            # alert(red('Retrying because the trial solution is outside of the box.'),'lvrsolve')

        # Don't retry if fval is small
        if __lvrfmin__ > 1e-3:
            retry = True
            alert(red('Retrying because the trial fmin value is greater than 1e-3.'),'lvrsolve')

        # Don't retry if fval is small
        if retry and (__lvrfmin__ < 1e-4):
            retry = False
            alert(red('Not retrying becuase the fmin value is low.'),'lvrsolve')

        # Return the solution
        return cw,sc,__lvrfmin__,retry

    # Give a solution for the current spin, fix the solution location, but vary the spin such that the current solution has an error of tol. This change in spin for tol may be useful in dynamically stepping through spin values.
    def gauge( this, jf, solution, tol=1e-4 ):

        # Import Maths
        from numpy import log,exp,linalg,array
        from scipy.optimize import root,fmin,minimize
        from kerr.pttools import leaver_workfunction
        from kerr import alert,red,warning,error

        #
        fun = lambda JF: linalg.norm(  leaver_workfunction( JF,this.l,this.m, solution, s=this.s, adjoint=this.adjoint )  )

        f0 = fun( jf )
        djf = 1e-6
        done = False
        _jf = jf; kmax = 2e3
        k = 0; rtol = 1e-2 * tol
        while not done:
            #
            k+=1
            #
            _jf += djf
            #
            f = fun( _jf )
            delta = (f-f0) - tol
            #
            we_have_gone_too_far = delta > rtol
            we_must_go_further = delta < 0
            #
            if we_have_gone_too_far:
                # go back a step, and half djf
                _jf -= djf
                djf /= 2.0
                done = False
            elif we_must_go_further:
                done = False
                djf *= 1.055
            else:
                done = True

            #
            if k>kmax: error('This process has not converged.')

        #
        ans = _jf
        return ans



    # Given a box's children, resize the boxes relative to child locations: no boxes overlap
    def sensescale(this):

        #
        from numpy import array,inf,linalg,sqrt
        from kerr import alert

        #
        children = this.collectchildren()

        # Let my people know.
        if this.verbose:
            alert('Sensing the scale of the current object\'s sub-boxes.','sensescale')

        # Determine the distance between this min, and its closest neighbor
        scalar = sqrt(2) if (not this.__smallboxes__) else 2.0*sqrt(2.0)
        for tom in children:

            d = inf
            for jerry in [ kid for kid in children if kid is not tom ]:

                r = array(tom.center)
                r_= array(jerry.center)
                d_= linalg.norm(r_-r)
                if d_ < d:
                    d = d_

            # Use the smallest distance found to determine a box size
            s = d/scalar
            width = s; height = s; res = int( max( 20, 1.5*float(this.res)/len(children) ) ) if (len(children)>1) else this.res

            # Define the new box size for this child
            tom.setboxprops( tom.center[0], tom.center[1], width, height, res )

    #
    def pop(this):

        def pop(a):
            a = a[:-1]

        this.__jf__.pop()
        for k in this.__data__:
            pop( this.__data__[ k ][ 'jf' ]      )
            pop( this.__data__[ k ][ 'cw' ]      )
            pop( this.__data__[ k ][ 'sc' ]      )
            pop( this.__data__[ k ][ 'lvrfmin' ] )



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
'''Functions for calculating QNM freuqncies parameterized by BH spin'''
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

# Try solving the 4D equation near a single guess value [ cw.real cw.imag sc.real sc.imag ]
def lvrsolve(jf,l,m,guess,tol=1e-8,s=-2, adjoint=False):

    '''
    Low-level function for numerically finding the root of leaver's equations
    '''

    # Import Maths
    from numpy import log,exp,linalg,array
    from scipy.optimize import root,fmin,minimize
    from positive import alert,red,warning,leaver_workfunction

    # Try using root
    # Define the intermediate work function to be used for this iteration
    fun = lambda STATE: log( 1.0 + abs(array(leaver_workfunction( jf,l,m, STATE, s=s, adjoint=adjoint ))) )
    X  = root( fun, guess, tol=tol )
    cw1,sc1 = X.x[0]+1j*X.x[1], X.x[2]+1j*X.x[3]
    __lvrfmin1__ = linalg.norm(array( exp(X.fun)-1.0 ))
    retry1 = ( 'not making good progress' in X.message.lower() ) or ( 'error' in X.message.lower() )


    # Try using fmin
    # Define the intermediate work function to be used for this iteration
    fun = lambda STATE: log(linalg.norm(  leaver_workfunction( jf,l,m, STATE, s=s, adjoint=adjoint )  ))
    X  = fmin( fun, guess, disp=False, full_output=True, ftol=tol )
    cw2,sc2 = X[0][0]+1j*X[0][1], X[0][2]+1j*X[0][3]
    __lvrfmin2__ = exp(X[1])
    retry2 = __lvrfmin2__ > 1e-3

    # Use the solution that converged the fastest to avoid solutions that have wandered significantly from the initial guess OR use the solution with the smallest fmin
    if __lvrfmin1__ < __lvrfmin2__ : # use the fmin value for convenience
        cw,sc,retry = cw1,sc1,retry1
        __lvrfmin__ = __lvrfmin1__
    else:
        cw,sc,retry = cw2,sc2,retry2
        __lvrfmin__ = __lvrfmin2__

    # Don't retry if fval is small
    if __lvrfmin__ > 1e-3:
        retry = True
        alert(red('Retrying because the trial fmin value is greater than 1e-3.'))

    # Don't retry if fval is small
    if retry and (__lvrfmin__ < 1e-4):
        retry = False
        alert(red('Not retrying becuase the fmin value is low.'))

    # Return the solution
    return cw,sc,__lvrfmin__,retry


# Extrapolative guess for gravitational perturbations. This function is best used within leaver_needle which solves leaver's equations for a range of spin values.
def leaver_extrap_guess( j, cw, sc, l, m, tol = 1e-3, d2j = 1e-6, step_sign = 1, verbose=False, plot=False, spline_order=3, monotomic_steps=False, boundary_spin=None, s=-2, adjoint=False ):

    '''
    Extrapolative guess for gravitational perturbations. This function is best used within leaver_needle which solves leaver's equations for a range of spin values.

    londonl@mit.edu 2019
    '''

    #
    from numpy import complex128, polyfit, linalg, ndarray, array, linspace, polyval, diff, sign, ones_like, linalg, hstack, sqrt
    if plot: from matplotlib.pyplot import figure,show,plot,xlim
    from scipy.interpolate import InterpolatedUnivariateSpline as spline

    #
    if not ( step_sign in (-1,1) ):
        error('step_sign input must be either -1 or 1 as it determins the direction of changes in spin')

    #
    if not isinstance(j,(list,ndarray,tuple)):
        j = array([j])
    if not isinstance(cw,(list,ndarray,tuple)):
        cw_ = ones_like(j,dtype=complex)
        cw_[-1] = cw; cw = cw_
    if not isinstance(sc,(list,ndarray,tuple)):
        sc_ = ones_like(j,dtype=complex)
        sc_[-1] = sc; sc = sc_

    #
    current_j = j[-1]
    initial_solution = [ cw[-1].real, cw[-1].imag, sc[-1].real, sc[-1].imag ]

    #
    lvrwrk = lambda J,STATE: linalg.norm(  leaver_workfunction( J,l,abs(m),STATE,s=s, adjoint=adjoint )  )

    # Make sure that starting piont satisfies the tolerance
    current_err = best_err = lvrwrk( current_j, initial_solution )

    # print current_err
    if current_err>tol:
        print(j)
        print(current_j)
        print(initial_solution)
        print(current_err)
        warning('Current solution does not satisfy the input tolerance value.')

    # Determine the polynomial order to use based on the total number of points
    nn = len(j)
    order = min( nn-1, spline_order ) # NOTE that 4 and 5 don't work as well, especially near extremal values of spin; 3may also have problems
    place = -order-1

    xx = array(j)[place:]
    yy = array(cw)[place:]
    zz = array(sc)[place:]

    alert('order is: %i'%order)
    if order>0:

        ## NOTE that coupling the splines can sometimes cause unhandled nans
        # yrspl = spline( xx, yy.real, k=order )
        # ycspl = spline( yy.real, yy.imag, k=order )
        # zrspl = spline( xx, zz.real, k=order )
        # zcspl = spline( zz.real, zz.imag, k=order )
        # yrspl_fun = yrspl
        # ycspl_fun = lambda J: ycspl( yrspl(J) )
        # zrspl_fun = zrspl
        # zcspl_fun = lambda J: zcspl( zrspl(J) )

        yrspl_fun = spline( xx, yy.real, k=order )
        ycspl_fun = spline( xx, yy.imag, k=order )
        zrspl_fun = spline( xx, zz.real, k=order )
        zcspl_fun = spline( xx, zz.imag, k=order )

    else:
        yrspl_fun = lambda J: cw[0].real*ones_like(J)
        ycspl_fun = lambda J: cw[0].imag*ones_like(J)
        zrspl_fun = lambda J: sc[0].real*ones_like(J)
        zcspl_fun = lambda J: sc[0].imag*ones_like(J)


    if plot:
        figure()
        plot( xx, yy.real, 'ob' )
        dxs = abs(diff(lim(xx)))/4 if abs(diff(lim(xx)))!=0 else 1e-4
        xs = linspace( min(xx)-dxs,max(xx)+dxs )
        plot( xs, yrspl_fun(xs), 'r' )
        xlim(lim(xs))
        if verbose:
            print(lim(xs))
            print(lim(yrspl_fun(xs)))
        show()

    guess_fit = lambda J: [ yrspl_fun(J), ycspl_fun(J), zrspl_fun(J), zcspl_fun(J) ]

    #
    k = -1; kmax = 500
    done = False
    exit_code = 0
    near_bounary = False
    best_j = current_j = j[-1]
    mind2j = 1e-7
    max_dj = sqrt(5)/42
    starting_j = j[-1]
    best_guess = guess_fit(current_j)
    if verbose: print('>> k,starting_j,starting_err = ',k,current_j,current_err)
    while not done:

        #
        k+=1
        current_j += d2j*step_sign
        if boundary_spin:
            if (boundary_spin-current_j)*step_sign < 0:
                alert('We\'re quite close to the specified boundary, so we will reduce the internal step size as to not exceed the boundary.')
                current_j -= d2j*step_sign
                print('** current_j = ',current_j)
                print('** boundary_spin = ',boundary_spin)
                new_d2j = max( min( d2j/21.0, abs( ( boundary_spin-current_j ) /21.0) ), 1e-6 )
                if new_d2j == 1e-6:
                    warning('Min value of d2j reached')
                print('** new_d2j = ',new_d2j)
                current_j = current_j + new_d2j*step_sign
                print('** new_current_j = ',current_j)
                print('** old_tol = ',tol)
                tol *= 0.01
                if tol<1e-7:
                    tol = 1e-7
                    warning('Min value of tol reached')
                print('** new_tol = ',tol)
                d2j = new_d2j
                if not near_bounary:
                    near_bounary = True
                    kmax = 4*kmax


        #
        # if d2j<mind2j: d2j = mind2j
        current_guess = guess_fit(current_j)

        #
        current_err = lvrwrk( current_j, current_guess )

        #
        if verbose: print('* k,best_j,best_err = ',k,best_j,best_err)

        #
        tolerance_is_exceeded = (current_err>tol)
        max_dj_exceeded = abs(current_j-starting_j)>max_dj

        # #
        # if (len(j)>3) and monotomic_steps:
        #     stepsize_may_increase = (abs(current_j-j[-1])+d2j) > abs(j[-1]-j[-2])
        # else:
        #     stepsize_may_increase = False

        best_j = current_j
        best_guess = current_guess
        best_err = current_err

        #
        if tolerance_is_exceeded: # or stepsize_may_increase:
            print('* k,best_j,best_err,tol,d2j = ',k,best_j,best_err,tol,d2j)
            if k>0:
                done = True
                alert('Tolerance exceeded. Exiting.')
                exit_code = 0
            else:
                warning('Tolerance exceeded on first iteration. Shrinking intermediate step size.')
                d2j = d2j/200
                if d2j<1e-20:
                    error('d2j<1e-20 -- something is wrong with the underlying equations setup')
                current_j = j[-1]
                k = -1
                best_guess = initial_solution
        else:
            if (k==kmax) and (not near_bounary):
                done = True
                warning('Max iterations exceeded. Exiting.')
                exit_code = 1

        if max_dj_exceeded:
            alert('Exiting because max_dj=%f has been exceeded'%max_dj)
            done = True
            exit_code = 0

        if abs(current_j-boundary_spin)<1e-10:
            alert('We are close enough to the boundary to stop.')
            print('$$ start_spin = ',j[-1])
            print('$$ boundary_spin = ',boundary_spin)
            print('$$ current_j = ',current_j)
            k = kmax
            done = True
            exit_code = -1

    #
    return best_j, best_guess, exit_code



# Solve leaver's equations between two spin values given a solution at a starting point
def leaver_needle( initial_spin, final_spin, l, m, initial_solution, tol=1e-3, initial_d2spin=1e-3, plot = False,verbose=False, use_feedback=True, spline_order=3, s=-2, adjoint=False ):

    '''
    Given an initial location and realted solution in the frequency-separation constant space,
    find the solution to leaver's equations between inut BH spin values for the specified l,m multipole.

    londonl@mit.edu 2019
    '''

    # Import usefuls
    from numpy import sign,array,diff,argmin,argsort,hstack

    # Determin the direction of requested changes in spin
    step_sign = sign( final_spin - initial_spin )

    # Unpack the initial solution.
    # NOTE that whether this is a solution of leaver's equations is tested within leaver_extrap_guess
    cwr,cwc,scr,scc = initial_solution
    initial_cw = cwr+1j*cwc
    initial_sc = scr+1j*scc

    # Initialize outputs
    j,cw,sc,err,retry = [initial_spin],[initial_cw],[initial_sc],[0],[False]

    #
    done = False
    k = 0
    internal_res = 24
    current_j = initial_spin
    d2j = initial_d2spin # Initial value of internal step size
    monotomic_steps = False
    while not done :

        #
        current_j,current_guess,exit_code = leaver_extrap_guess( j, cw, sc, l, m, tol=tol, d2j=d2j, step_sign=step_sign, verbose=False, plot=plot, spline_order=spline_order, boundary_spin=final_spin,s=s, adjoint=adjoint )
        if (current_j == j[-1]) and (exit_code!=1):
            # If there has been no spin, then divinde the extrap step size by internal_res.
            # Here we use internal_res as a resolution heuristic.
            d2j/=internal_res
            alert('current_j == j[-1]')
            if d2j<1e-9:
                done = True
                warning('Exiting becuase d2j is too small.')
        else:

            done = step_sign*(final_spin-current_j) < 1e-10

            j.append( current_j )
            # Set the dynamic step size based on previous step sizes
            # Here we use internal_res as a resolution heuristic.
            d2j = abs(j[-1]-j[-2])/internal_res
            if verbose: print('d2j = ',d2j)
            current_retry = True
            tol2 = 1.0e-8
            k2 = 0
            while current_retry:
                k2 += 1
                current_cw,current_sc,current_err,current_retry = lvrsolve(current_j,l,m,current_guess,s=s,tol=tol2/k2**2, adjoint=adjoint)
                if k2>6:
                    current_retry = False
                    warning('Exiting lvrsolve loop becuase a solution could not be found quickly enough.')
            if verbose: print(k,current_j,current_cw,current_sc,current_err,current_retry)
            cw.append( current_cw )
            sc.append( current_sc )
            err.append( current_err )
            retry.append( current_retry )

        #
        if d2j==0:
            warning('Exiting because the computer thinks d2j is zero')
            break


    # Convert lists to arrays with increasing spin
    j,cw,sc,err,retry = [ array( v if step_sign==1 else v[::-1] ) for v in [j,cw,sc,err,retry] ]

    #
    return j,cw,sc,err,retry

#
def greedy_leaver_needle( j,cw,sc,err,retry, l, m, plot = False, verbose=False, spline_order=3, s=-2, adjoint=False ):

    #
    from positive import spline,leaver_needle,findpeaks
    from numpy import array ,argmax,argsort,linspace,linalg,median,log, exp,hstack,diff,sort,pi,sin

    # #
    # j,cw,sc,err,retry = leaver_needle( initial_spin, final_spin, l,m, initial_solution, tol=tol, verbose=verbose, plot=plot, spline_order=spline_order )

    # ------------------------------------------------------------ #
    # Calculate the error of the resulting spline model between the boundaries
    # ------------------------------------------------------------ #
    nums = 501
    alert('Calculating the error of the resulting spline model between the boundaries',verbose=verbose)
    lvrwrk = lambda J,STATE: linalg.norm(  leaver_workfunction( J,l,abs(m),STATE,s=s, adjoint=adjoint )  )
    # js = linspace(min(j),max(j),nums)
    js =  sin( linspace(0,pi/2,nums) )*(max(j)-min(j)) + min(j)
    cwrspl = spline(j,cw.real,k=2)
    cwcspl = spline(j,cw.imag,k=2)
    scrspl = spline(j,sc.real,k=2)
    sccspl = spline(j,sc.imag,k=2)
    statespl = lambda J: [ cwrspl(J), cwcspl(J), scrspl(J), sccspl(J) ]
    errs = array( [ lvrwrk(J,statespl(J)) for J in js ] )
    pks,locs = findpeaks( log(errs) )
    tols = exp( median( pks ) )

    #
    pks,locs = findpeaks( log(errs) )
    tols = exp( median( pks ) )

    #
    alert('Using greedy process to refine solution',header=True)
    from matplotlib.pyplot import plot,yscale,axvline,axhline,show,figure,figaspect,subplot

    #
    # j,cw,sc,err,retry = [ list(v) for v in [j,cw,sc,err,retry] ]
    done = ((max(errs)/tols) < 10) or (max(errs)<1e-4)
    print(done, 'max(errs) = ',max(errs),' tols = ',tols)
    if done:
        alert('The data seems to have no significant errors due to interpolation. Exiting.')
    while not done:

        kmax = argmax( errs )

        k_right = find( j>js[kmax] )[0]
        k_left = find( j<js[kmax] )[-1]

        jr = j[k_right]
        jl = j[k_left]


        plot( js, errs )
        yscale('log')
        axvline( js[kmax], color='r' )
        plot( j, err, 'or', mfc='none' )
        axvline( jr, ls=':', color='k' )
        axvline( jl, ls='--', color='k' )
        axhline(tols,color='g')
        show()

        initial_spin = jl
        final_spin = jr
        initial_solution = [ cw[k_left].real, cw[k_left].imag, sc[k_left].real, sc[k_left].imag ]

        j_,cw_,sc_,err_,retry_ = leaver_needle( initial_spin, final_spin, l,abs(m), initial_solution, tol=tols, verbose=verbose, spline_order=spline_order,s=s, adjoint=adjoint )

        j,cw,sc,err,retry = [ hstack([u,v]) for u,v in [(j,j_),(cw,cw_),(sc,sc_),(err,err_),(retry,retry_)] ]

        #
        sortmask = argsort(j)
        j,cw,sc,err,retry = [ v[sortmask] for v in (j,cw,sc,err,retry) ]
        uniquemask = hstack( [array([True]),diff(j)!=0] )
        j,cw,sc,err,retry = [ v[uniquemask] for v in (j,cw,sc,err,retry) ]

        #
        alert('Calculating the error of the resulting spline model between the boundaries',verbose=verbose)
        lvrwrk = lambda J,STATE: linalg.norm(  leaver_workfunction( J,l,abs(m),STATE,s=s, adjoint=adjoint )  )
        js = linspace(min(j),max(j),2e2)
        js = hstack([j,js])
        js = array(sort(js))
        cwrspl = spline(j,cw.real,k=spline_order)
        cwcspl = spline(j,cw.imag,k=spline_order)
        scrspl = spline(j,sc.real,k=spline_order)
        sccspl = spline(j,sc.imag,k=spline_order)
        statespl = lambda J: [ cwrspl(J), cwcspl(J), scrspl(J), sccspl(J) ]
        #
        errs = array( [ lvrwrk(J,statespl(J)) for J in js ] )

        #
        done = max(errs)<tols

        # current_j = js[k]
        # current_state = statespl( current_j )
        # current_cw,current_sc,current_err,current_retry = lvrsolve(current_j,l,m,current_state)
        #
        # j,cw,sc,err,retry = [ list(v) for v in [j,cw,sc,err,retry] ]
        # j.append( current_j )
        # cw.append( current_cw )
        # sc.append( current_sc )
        # err.append( current_err )
        # retry.append( current_retry )
        #
        # sort_mask = argsort(j)
        # j,cw,sc,err,retry = [ array(v) for v in [j,cw,sc,err,retry] ]
        # j,cw,sc,err,retry = [ v[sort_mask] for v in [j,cw,sc,err,retry] ]
        #
        # cwrspl = spline(j,cw.real,k=2)
        # cwcspl = spline(j,cw.imag,k=2)
        # scrspl = spline(j,sc.real,k=2)
        # sccspl = spline(j,sc.imag,k=2)
        # statespl = lambda J: [ cwrspl(J), cwcspl(J), scrspl(J), sccspl(J) ]
        #
        # errs = array( [ lvrwrk(J,statespl(J)) for J in js ] )
        #
        # figure( figsize=2*figaspect(0.5) )
        # subplot(1,2,1)
        # plot( js, errs )
        # axvline( js[k], color='r' )
        # axhline(tol,color='b',ls='--')
        # axhline(tols,color='g',ls='-')
        # yscale('log')
        # subplot(1,2,2)
        # plot( js, cwrspl(js) )
        # axvline( js[k], color='r' )
        #
        # done = max(errs)<=(tols)
        # print('max(errs) = ',max(errs))
        # print('tols = ',tols)
        # show()


    #
    return j,cw,sc,err,retry


#
class leaver_solve_workflow:

    '''
    Workflow class for solving and saving data from leaver's equationsself.
    '''

    #
    def __init__( this, initial_spin, final_spin, l, m, tol=1e-3, verbose=False, basedir=None, box_xywh=None, max_overtone=6, output=True, plot=True, initial_box_res=81, spline_order=3, initialize_only=False, s=-2, adjoint=False ):

        #
        this.__validate_inputs__(initial_spin, final_spin, l, m, tol, verbose, basedir, box_xywh, max_overtone, output, plot, initial_box_res, spline_order, s, adjoint)


        # ------------------------------------------------------------ #
        # Define a box in cw space over which to calculate QNM solutions
        # ------------------------------------------------------------ #
        alert('Initializing leaver box',verbose=this.verbose,header=True)
        this.__initialize_leaver_box__()

        # ------------------------------------------------------------ #
        # Map the QNM solution space at an initial spin value
        # ------------------------------------------------------------ #
        this.leaver_box.map( this.initial_spin )

        # ------------------------------------------------------------ #
        # Let's see what's in the box
        # ------------------------------------------------------------ #
        alert('The following QNMs have been found in the box:',header=True)
        this.starting_solutions = { k:this.leaver_box.data[k] for k in sorted(this.leaver_box.data.keys(), key = lambda x: x[1], reverse=True ) if k[2]<this.max_overtone }
        # Note that it is here that we enforce the max_overtone input
        this.sorted_mode_list = sorted(this.starting_solutions.keys(), key = lambda x: -float(x[-1])/(x[2]+1), reverse=not True )
        for k in this.sorted_mode_list:
            print('(l,m,n,x,p) = %s'%(str(k)))

        # ------------------------------------------------------------ #
        # Plot the QNM solution space at an initial spin value
        # ------------------------------------------------------------ #
        alert('Plotting 2D start frame',verbose=this.verbose,header=True)
        if this.plot: this.__plot2Dframe__()

        #
        if not initialize_only:
            alert('Threading QNM solutions',verbose=this.verbose,header=True)
            this.solve_all_modes()

        #
        alert('Done!',verbose=this.verbose,header=True)

    #
    def solve_all_modes(this):

        for z in this.sorted_mode_list:
            (l,m,n,x,p) = z
            if True:# m<0:

                alert('Working: (l,m,n,x,p) = %s'%str(z),header=True)
                this.solve_mode(*z)

                # ------------------------------------------------------------ #
                # Ploting
                # ------------------------------------------------------------ #
                if this.plot:
                    # Plot interpolation error
                    this.__plotModeSplineError__(z)
                    # Plot frequency and separation constant
                    this.__plotCWSC__(z)


    #
    def __plot2Dframe__(this,save=None):
        from matplotlib.pyplot import savefig,plot,xlim,ylim,xlabel,ylabel,title,figure,gca,subplot,close,gcf,figaspect
        alert('Saving 2D solution space frame at initial spin',verbose=this.verbose)
        this.leaver_box.plot(showlabel=True)
        frm_prefix = ('l%im%i_start' % (this.l,this.m)).replace('-','m')
        frm_fname = ('%s.png' % (frm_prefix))
        if save is None: save = this.output
        if save:
            savefig( this.frm_outdir+frm_fname )
            close(gcf())

    #
    def __plotModeSplineError__(this,z,save=None):

        #
        from matplotlib.pyplot import savefig, plot, xlim, ylim, xlabel, ylabel, title, figure, gca, subplot, close, gcf, figaspect, axhline, yscale, legend
        l,m,n,x,p = z
        figure( figsize=1.2*figaspect(0.618) )
        plot( this.results[z]['js'],this.results[z]['errs'] )
        axhline(this.tol,color='orange',ls='--',label='tol = %g'%this.tol)
        yscale('log'); xlabel( '$j$' )
        ylabel( r'$\epsilon$' ); legend()
        title(r'$(\ell,m,n)=(%i,%i,%i)$'%(l,m,n))
        fig_fname = ('l%im%in%i_epsilon.pdf' % (l,m,n)).replace('-','m')
        if save is None: save = this.output
        if save:
            savefig( this.outdir+fig_fname,pad_inches=.2, bbox_inches='tight' )
            close(gcf())

    #
    def __plotCWSC__(this,z,save=None):

        #
        from matplotlib.pyplot import savefig,plot,xlim,ylim,xlabel,ylabel,title,figure,gca,subplot,close,gcf,figaspect,legend,grid
        l,m,n,x,p = z

        #
        j = this.results[z]['j']
        cw = this.results[z]['cw']
        sc = this.results[z]['sc']
        js = this.results[z]['js']
        cwrspl = this.results[z]['cwrs']
        cwcspl = this.results[z]['cwcs']
        scrspl = this.results[z]['scrs']
        sccspl = this.results[z]['sccs']

        grey = '0.9'
        n = z[2]
        figure( figsize=3*figaspect(0.618) )
        subplot(2,2,1)
        plot( j, cw.real,'o',label='Numerical Data' )
        plot( js, cwrspl(js), 'r',label='Spline, k=%i'%this.spline_order )
        legend()
        xlabel('$j$'); ylabel(r'$\mathrm{re}\; \tilde{\omega}_{%i%i%i}$'%(l,m,n))
        grid(color=grey, linestyle='-')
        subplot(2,2,2)
        plot( j, cw.imag,'o' )
        plot( js, cwcspl(js), 'r' )
        xlabel('$j$'); ylabel(r'$\mathrm{im}\; \tilde{\omega}_{%i%i%i}$'%(l,m,n))
        grid(color=grey, linestyle='-')
        subplot(2,2,3)
        plot( j, sc.real,'o' )
        plot( js, scrspl(js), 'r' )
        xlabel('$j$'); ylabel(r'$\mathrm{re}\; \tilde{A}_{%i%i%i}$'%(l,m,n))
        grid(color=grey, linestyle='-')
        subplot(2,2,4)
        plot( j, sc.imag,'o' )
        plot( js, sccspl(js), 'r' )
        xlabel('$j$'); ylabel(r'$\mathrm{im}\; \tilde{A}_{%i%i%i}$'%(l,m,n))
        grid(color=grey, linestyle='-')
        fig_fname = ('l%im%in%i_results.pdf' % (l,m,n)).replace('-','m')
        if save is None: save = this.output
        if save:
            savefig( this.outdir+fig_fname,pad_inches=.2, bbox_inches='tight' )
            close(gcf())

    #
    def __initialize_leaver_box__(this,box_xywh=None):

        #
        if box_xywh is None:
            box_xywh = this.box_xywh
        # Extract box parameters
        x,y,wid,hig = this.box_xywh
        # Define the cwbox object
        this.leaver_box = cwbox( this.l,this.m,x,y,wid,hig,res=this.initial_box_res,maxn=this.max_overtone,verbose=this.verbose,s=this.s, adjoint=this.adjoint )
        # Shorthand
        a = this.leaver_box

        #
        return None

    #
    def solve_mode(this,l,m,n,x,p):

        #
        if this.plot: from matplotlib.pyplot import savefig,plot,xlim,ylim,xlabel,ylabel,title,figure,gca,subplot,close,gcf,figaspect
        from numpy import linspace,complex128,array,log,savetxt,vstack,pi,mod,cos,linalg,sign,exp,hstack,argsort,diff
        from positive import spline,leaver_needle
        import dill
        import pickle

        #
        z = (l,m,n,x,p)
        this.results[z] = {}

        #
        if not ( z in this.leaver_box.data ):
            error('Input mode indeces not in this.leaver_box')

        # ------------------------------------------------------------ #
        # Thread the solution from cwbox through parameter space
        # ------------------------------------------------------------ #
        alert('Threading the solution from cwbox through parameter space',verbose=this.verbose)
        solution_cw,solution_sc = this.leaver_box.data[z]['cw'][-1],this.leaver_box.data[z]['sc'][-1]
        print('>> ',this.leaver_box.data[z]['lvrfmin'][-1])
        # forwards
        initial_solution = [ solution_cw.real, solution_cw.imag, solution_sc.real, solution_sc.imag ]
        print('** ',leaver_workfunction( this.initial_spin, l, abs(m), initial_solution, s=this.s, adjoint=this.adjoint ))
        j,cw,sc,err,retry = leaver_needle( this.initial_spin, this.final_spin, l,abs(m), initial_solution, tol=this.tol/( n+1 + 2*(1-p) ), verbose=this.verbose, spline_order=this.spline_order, s=this.s, adjoint=this.adjoint )

        # backwards
        alert('Now evaluating leaver_needle backwards!',header=True)
        initial_solution = [ cw[-1].real, cw[-1].imag, sc[-1].real, sc[-1].imag ]
        j_,cw_,sc_,err_,retry_ = leaver_needle( this.final_spin, this.initial_spin, l,abs(m), initial_solution, tol=this.tol/( n+1 + 2*(1-p) ), verbose=this.verbose, spline_order=this.spline_order, s=this.s,initial_d2spin=abs(j[-1]-j[-2])/5, adjoint=this.adjoint )
        #
        j,cw,sc,err,retry = [ hstack([u,v]) for u,v in [(j,j_),(cw,cw_),(sc,sc_),(err,err_),(retry,retry_)] ]
        sortmask = argsort(j)
        j,cw,sc,err,retry = [ v[sortmask] for v in (j,cw,sc,err,retry) ]
        uniquemask = hstack( [array([True]),diff(j)!=0] )
        j,cw,sc,err,retry = [ v[uniquemask] for v in (j,cw,sc,err,retry) ]

        #
        this.results[z]['j'],this.results[z]['cw'],this.results[z]['sc'],this.results[z]['err'],this.results[z]['retry'] = j,cw,sc,err,retry

        # ------------------------------------------------------------ #
        # Calculate the error of the resulting spline model between the boundaries
        # ------------------------------------------------------------ #
        alert('Calculating the error of the resulting spline model between the boundaries',verbose=this.verbose)
        lvrwrk = lambda J,STATE: linalg.norm(  leaver_workfunction( J,l,abs(m),STATE,s=this.s, adjoint=this.adjoint )  )
        js = linspace(min(j),max(j),1e3)

        cwrspl = spline(j,cw.real,k=this.spline_order)
        cwcspl = spline(j,cw.imag,k=this.spline_order)
        scrspl = spline(j,sc.real,k=this.spline_order)
        sccspl = spline(j,sc.imag,k=this.spline_order)
        statespl = lambda J: [ cwrspl(J), cwcspl(J), scrspl(J), sccspl(J) ]

        # Store spline related quantities
        this.results[z]['errs'] = array( [ lvrwrk(J,statespl(J)) for J in js ] )
        this.results[z]['js'] = js
        this.results[z]['cwrs'] = cwrspl
        this.results[z]['cwcs'] = cwcspl
        this.results[z]['scrs'] = scrspl
        this.results[z]['sccs'] = sccspl
        this.results[z]['statespl'] = statespl

        # ------------------------------------------------------------ #
        # Save raw data and splines
        # ------------------------------------------------------------ #
        if this.output:
            data_array = vstack(  [ j,
                                    cw.real,
                                    cw.imag,
                                    sc.real,
                                    sc.imag,
                                    err ]  ).T

            fname = this.outdir+('l%im%1.0fn%i.txt'%z[:3]).replace('-','m')
            savetxt( fname, data_array, fmt='%18.12e', delimiter='\t\t', header=r's=%i Kerr QNM: [ jf reMw imMw reA imA error ], 2016/2019, londonl@mit, https://github.com/llondon6/'%this.s )
            # Save the current object
            alert('Saving the current object using pickle',verbose=this.verbose)
            with open( fname.replace('.txt','_splines.pickle') , 'wb') as object_file:
                pickle.dump( {'cwreal':cwrspl,'cwimag':cwcspl,'screal':scrspl,'scimag':sccspl} , object_file, pickle.HIGHEST_PROTOCOL )


    #
    def __validate_inputs__( this, initial_spin, final_spin, l, m, tol, verbose, basedir, box_xywh, max_overtone, output, plot, initial_box_res, spline_order, s, adjoint ):

        # Save inputs as properties of the current object
        alert('Found inputs:',verbose=verbose)
        for k in dir():
            if k != 'this':
                this.__dict__[k] = eval(k)
                if verbose: print('  ->  %s = %s'%( k, blue(str(eval(k))) ))

        # Import usefuls
        from os.path import join,expanduser
        from numpy import pi
        from positive import mkdir

        # Name directories for file IO
        alert('Making output directories ...',verbose=this.verbose)
        if this.basedir is None: this.basedir = ''
        this.basedir = expanduser(this.basedir)
        this.outdir = ( join( this.basedir,'./s%il%im%i/' % (s,l,abs(m))) ).replace('-','m')
        if this.outdir[-1] is not '/': this.outdir += '/'
        this.frm_outdir = this.outdir+'frames/'
        this.s = s
        # Make directories if needed
        mkdir(this.outdir,rm = False,verbose=this.verbose)  # Make the directory if it doesnt already exist and remove the directory if it already exists. Dont remove if there is checkpint data.
        mkdir(this.frm_outdir,verbose=this.verbose)

        #
        if this.output: this.plot = True

        #
        this.spline_order = spline_order

        #
        this.results = {}

        #
        if this.box_xywh is None:
            x = 0
            y = -0.5
            wid = 1.2*(m if abs(m)>0 else 1.0)
            hig = pi-1
            this.box_xywh = [x,y,wid,hig]
            alert('Using default parameter space box for starting spin.',verbose=this.verbose)
            alert('this.box_xywh = %s'%(str(this.box_xywh)),verbose=this.verbose)


#
def tkangular( S, theta, acw, m, s=-2, separation_constant=None,adjoint=False  ):
    '''
    Apply Teukolsy's angular operator to input
    '''
    #
    from numpy import sin, cos, isnan, diff,sign
    #
    zero = 1e-10
    theta[theta==0]=zero
    if separation_constant is None:
        separation_constant = sc_leaver( acw, 2, m, s,verbose=False,adjoint=False)[0]
    A = separation_constant
    #
    sn = sin(theta)
    cs = cos(theta)

    dS = spline_diff(theta,S)
    D2S = spline_diff( theta, sn * dS ) / sn
    #
    mscs = m+s*cs
    acwcs = acw*cs
    VS = (  -mscs*mscs/(sn*sn) + s + acwcs*( acwcs - 2*s ) + A  ) * S

    #
    ans = D2S + VS

    #
    return ans


# Compute the Clebsch-Gordan coefficient by wrapping the sympy function.
def clebsh_gordan_wrapper(j1,j2,m1,m2,J,M,precision=16):

    '''
    Compute the Clebsch-Gordan coefficient by wrapping the sympy functionality.
    ---
    USAGE: clebsh_gordan_wrapper(j1,j2,m1,m2,J,M,precision=16)
    '''

    # Import usefuls
    import sympy,numpy
    from sympy.physics.quantum.cg import CG

    # Compute and store for output
    ans = sympy.N( CG(j1, m1, j2, m2, J, M).doit(), precision )

    # return answer
    return complex( numpy.array(ans).astype(numpy.complex128) )


# Compute inner-products between cos(theta) and cos(theta)**2 and SWSHs
def swsh_prod_cos(s,l,lp,m,u_power):

    '''
    Compute the inner product
    < sYlm(l) | u^u_power | k+right_shift >

    USAGE
    ---
    ans = swsh_clebsh_gordan_prods(k,left_shift,u_power,right_shift)

    NOTES
    ---
    * Here, k is the polar index more commonly denoted l.
    * The experssions below were generated in Mathematica
    * u_power not in (1,2) causes this function to throw an error
    * related selection rules are manually implemented

    londonl@mit.edu 2020
    '''


    # Import usefuls
    from scipy import sqrt

    # Define a delta and do a precompute
    delta = lambda a,b: 1 if a==b else 0
    sqrt_factor = sqrt((2*l+1.0)/(2*lp+1.0))

    #
    if u_power==1:

        # Equation 3.9b of Teukolsky 1973 ApJ 185 649P
        ans = sqrt_factor * clebsh_gordan_wrapper(l,1,m,0,lp,m) * clebsh_gordan_wrapper(l,1,-s,0,lp,-s)

    elif u_power==2:

        # Equation 3.9a of Teukolsky 1973 ApJ 185 649P
        by3 = 1.0/3
        twoby3 = 2.0*by3
        ans = by3*delta(l,lp)  +  twoby3 * sqrt_factor * clebsh_gordan_wrapper(l,2,m,0,lp,m) * clebsh_gordan_wrapper(l,2,-s,0,lp,-s)

    else:

        #
        error('The inner-product between SWSHs and cos(theta)^%i is not handled by this function. The u_power input must be 1 or 2.'%u_power)

    # Return answer
    return ans


# Compute the innder product: < sYlm(k+left_shift) | u^u_power | k+right_shift >
def swsh_clebsh_gordan_prods(k,m,s,left_shift,u_power,right_shift):
    '''
    Compute the inner product
    < sYlm(k+left_shift) | u^u_power | k+right_shift >

    USAGE
    ---
    ans = swsh_clebsh_gordan_prods(k,left_shift,u_power,right_shift)

    NOTES
    ---
    * Here, k is the polar index more commonly denoted l.
    * The experssions below were generated in Mathematica
    * u_power not in (1,2) causes this function to throw an error
    * related selection rules are manually implemented

    londonl@mit.edu 2020
    '''

    #
    from scipy import sqrt,floor,angle,pi,sign

    #
    (k,m,s) = [ float(x) for x in (k,m,s) ]

    #
    Q ={    (0,1,-1):(sqrt(k - m)*sqrt(k + m)*sqrt(k - s)*sqrt(k + s))/(k*sqrt(-1 + 4*k**2)), \
            (0,1,1):sqrt((3 + 4*k*(2 + k))*(1 + k - m)*(1 + k + m)*(1 + k - s)*(1 + k + s))/((1 + k)*(1 + 2*k)*(3 + 2*k)), \
            (0,2,-1):(-2*sqrt(-1 + 4*k**2)*sqrt(k - m)*m*sqrt(k + m)*sqrt(k - s)*s*sqrt(k + s))/(k - 5*k**3 + 4*k**5), \
            (0,2,1):(-2*m*s*sqrt((3 + 4*k*(2 + k))*(1 + k - m)*(1 + k + m)*(1 + k - s)*(1 + k + s)))/(k*(1 + k)*(2 + k)*(1 + 2*k)*(3 + 2*k)), \
            (0,2,-2):((-1)**floor((pi - angle(-3 + 2*k) - angle(-1 + k - m) + angle(-1 + k + m) + angle(-1 + k - s) - angle(-1 + k + s))/(2*pi))*sqrt(-1 + k - m)*sqrt(k - m)*sqrt(-1 + k + m)*sqrt(k + m)*sqrt(-1 + k - s)*sqrt(k - s)*sqrt(-1 + k + s)*sqrt(k + s))/(sqrt(-3 + 2*k)*sqrt(1 + 2*k)*(k - 3*k**2 + 2*k**3)), \
            (0,2,2):sqrt(((1 + k - m)*(2 + k - m)*(1 + k + m)*(2 + k + m)*(1 + k - s)*(2 + k - s)*(1 + k + s)*(2 + k + s))/((1 + 2*k)*(5 + 2*k)))/((1 + k)*(2 + k)*(3 + 2*k)), \
            (0,1,0):-((m*s)/(k + k**2)), \
            (-2,1,-2):(m*s)/((2 - 3*k + k**2)*sign(3 - 2*k)), \
            (-1,1,-1):(m*s)/(k - k**2), \
            (-1,1,-2):((-1)**floor((pi - angle(3 + 4*(-2 + k)*k) - angle(-1 + k - m) + angle(-1 + k + m) + angle(-1 + k - s) - angle(-1 + k + s))/(2*pi))*sqrt(3 + 4*(-2 + k)*k)*sqrt(-1 + k - m)*sqrt(-1 + k + m)*sqrt(-1 + k - s)*sqrt(-1 + k + s))/((-1 + k)*(-3 + 2*k)*(-1 + 2*k)), \
            (-2,1,-1):((-1)**floor((pi - angle(3 + 4*(-2 + k)*k) + angle(-1 + k - m) - angle(-1 + k + m) - angle(-1 + k - s) + angle(-1 + k + s))/(2*pi))*sqrt(3 + 4*(-2 + k)*k)*sqrt(-1 + k - m)*sqrt(-1 + k + m)*sqrt(-1 + k - s)*sqrt(-1 + k + s))/((-1 + k)*(-3 + 2*k)*(-1 + 2*k)), \
            (1,1,1):-((m*s)/(2 + 3*k + k**2)), \
            (1,1,2):sqrt(((2 + k - m)*(2 + k + m)*(2 + k - s)*(2 + k + s))/((3 + 2*k)*(5 + 2*k)))/(2 + k), \
            (2,1,1):sqrt(((2 + k - m)*(2 + k + m)*(2 + k - s)*(2 + k + s))/((3 + 2*k)*(5 + 2*k)))/(2 + k), \
            (2,1,2):-((m*s)/(6 + 5*k + k**2)), \
            (0,2,0):1.0/3 + (2*(k + k**2 - 3*m**2)*(k + k**2 - 3*s**2))/(3*k*(1 + k)*(-1 + 2*k)*(3 + 2*k)), \
            (0,2,2):sqrt(((1 + k - m)*(2 + k - m)*(1 + k + m)*(2 + k + m)*(1 + k - s)*(2 + k - s)*(1 + k + s)*(2 + k + s))/((1 + 2*k)*(5 + 2*k)))/((1 + k)*(2 + k)*(3 + 2*k)), \
            (-2,2,-2):1.0/3 - (2*(2 + (-3 + k)*k - 3*m**2)*(2 + (-3 + k)*k - 3*s**2))/(3*(-2 + k)*(-1 + k)*(-5 + 2*k)*(-1 + 2*k)*sign(3 - 2*k)), \
            (-1,2,-2):(2*(-1)**floor((pi - angle(3 + 4*(-2 + k)*k) - angle(1 - k + m) + angle(-1 + k + m) + angle(1 - k + s) - angle(-1 + k + s))/(2*pi))*sqrt(3 + 4*(-2 + k)*k)*m*sqrt(1 - k + m)*sqrt(-1 + k + m)*s*sqrt(1 - k + s)*sqrt(-1 + k + s))/((-2 + k)*(-1 + k)*k*(-3 + 2*k)*(-1 + 2*k)), \
            (-2,2,-1):(2*(-1)**floor((pi - angle(3 + 4*(-2 + k)*k) + angle(1 - k + m) - angle(-1 + k + m) - angle(1 - k + s) + angle(-1 + k + s))/(2*pi))*sqrt(3 + 4*(-2 + k)*k)*m*sqrt(1 - k + m)*sqrt(-1 + k + m)*s*sqrt(1 - k + s)*sqrt(-1 + k + s))/((-2 + k)*(-1 + k)*k*(-3 + 2*k)*(-1 + 2*k)), \
            (-1,2,-1):((-1 + k)*k*(-1 + 2*(-1 + k)*k - 2*m**2) + 2*(k - k**2 + 3*m**2)*s**2)/(k*(3 + k + 4*(-2 + k)*k**2)), \
            (1,2,1):1.0/3 + (2*(2 + k*(3 + k) - 3*m**2)*(2 + k*(3 + k) - 3*s**2))/(3*(1 + k)*(2 + k)*(1 + 2*k)*(5 + 2*k)), \
            (1,2,2):(-2*m*s*sqrt(((2 + k - m)*(2 + k + m)*(2 + k - s)*(2 + k + s))/((3 + 2*k)*(5 + 2*k))))/((1 + k)*(2 + k)*(3 + k)), \
            (2,2,1):(-2*m*s*sqrt(((2 + k - m)*(2 + k + m)*(2 + k - s)*(2 + k + s))/((3 + 2*k)*(5 + 2*k))))/((1 + k)*(2 + k)*(3 + k))
        }

    #
    if not ( u_power in [1,2] ):
       error('This function handles inner-products between two spin wieghted spherical harmonics and cos(theta) or cos(theta)^2. You have entrered %s, which would correspond to cos(theta)^%s'%(red(str(u_power)),red(str(u_power))))

    #
    z = (left_shift,u_power,right_shift)

    #
    is_handled = (z in Q)
    lp_exists = ((z[0]+k)>=abs(s)) and ((z[-1]+k)>=abs(s))
    is_valid = lp_exists and is_handled

    #
    ans = Q[z] if is_valid else 0

    # Return answer // implicitely implement selection rules
    if z in Q:
       return Q[z]
    else:
       error('make sure that you should not be using the sympy version of this function: swsh_prod_cos')
       return 0

#
def aslmcg( a, s, l, m, n, theta, phi, kerr=True, lmin=None, lmax=None, span=6, force_norm=True ):
    '''
    Compute adjoint spheroidal harmonic functoin using the spherical harmonic clensch-gordan method. By default, kerr adjoint functions are computed.
    londonl@mit.edu 2020
    '''
    
    #
    from numpy.linalg import inv
    from numpy import zeros,array,double,ndarray,dot,sqrt,zeros_like
    
    # Return standard adjoint if requested
    if not kerr:
        aw = a * leaver( a, l, m, n )[0]
        S,A = slmcg( aw, s, l, m, theta, phi )
        return S.conj(), A.conj()
        
    #
    if not isinstance(phi,(float,int,double)):
        error('phi must be number; zero makes sense as the functions phi dependence is exp(1j*m*phi), and so can be added externally')
        
    # Otherwise proceed to computeation of Kerr "adjoint" function(s)
    
    #
    if l is not 2:
        error('This function currently works when l=2 is given, but it will generate and output harmonics for all l<=lmax.')
    
    # Handle input format
    if isinstance(a,(list,ndarray)):
        if len(a)>1:
            error('first input as iterable not handled; fun function on each element')
        else:
            a = a[0]
            
    # if lmin in None, set it relative to l
    if lmin is None: lmin = max(l-span,max(abs(s),abs(m)))
    # if lmax in None, set it relative to l
    if lmax is None: lmax = l+span
    
    # Define index range and perform precomputations
    lrange = range(lmin,lmax+1); num_ell = len(lrange)
    
    # # -------------------------------------- #
    # # ALTERNATE ROUTE -- Perform the integrals directly 
    # # NOTE that this is faster but less accurate
    # # in phase for small amplitudes
    # # -------------------------------------- #
    # # Use spheroidals directly
    # beta = zeros( (num_ell,num_ell), dtype=complex )
    # for j,llj in enumerate(lrange):
    #     for k,llk in enumerate(lrange):
    #         beta[j,k] = ysprod(a, llj,m, (llk,m,n), N=2**10, use_nr_convention=False )
    
    #
    beta = zeros( (num_ell,num_ell), dtype=complex )
    A = zeros_like(beta)
    for k,llk in enumerate( lrange ):
        
        # Calculate spherical-spheroidal mixing coefficients using matrix method
        aw = a * leaver( a, llk, m, n )[0]
        
        # Use helper function to calculate matrx elements
        _,vals_k,vecs_k,lrange_k = slmcg_helper(aw,s,llk,m,span=span)
        dex_map = { ll:lrange_k.index(ll) for ll in lrange_k }
        raw_beta_k = vecs_k[ :,dex_map[llk] ]
        
        #
        A[ k,k ] = vals_k[ dex_map[llk] ]
        
        lmin_k = min(lrange_k); lmax_k = max(lrange_k)
        # Create mask for wanted values in raw_beta_k
        start_dex_k = lrange_k.index(lmin) if lmin in lrange_k else  0
        end_dex_k   = lrange_k.index(lmax) if lmax in lrange_k else -1
        # Select wanted values 
        wanted_raw_beta_k = raw_beta_k[ start_dex_k : end_dex_k+1 ]
        # Seed beta with wanted values after determining the lrange mask of interest
        start_dex = lrange.index( lrange_k[start_dex_k] )
        end_dex   = lrange.index( lrange_k[end_dex_k] )
        beta[start_dex:end_dex+1,k] = wanted_raw_beta_k
        
    # Compute the inverse conjugate matrix
    X, Z = beta, inv(beta)
    nu = Z.conj()
    
    # Compute the related operator's matrix rep (a "heterogeneous adjoint")
    L_ddag = dot( Z, dot( A, X ) ).conj()
    
    # Construct space of spherical harmonics to use 
    Yspace = array( [ sYlm(s,llj,m,theta,phi) for llj in lrange ] )
    
    # Compute adjoint functions 
    # NOTE that this line can be slow if many (thousand) values of theta are used
    aSspace = dot( nu, Yspace )
    # Compute regular spheroidal function
    Sspace = dot(beta.T,Yspace)
    
    # Enforce normalization
    # NOTE that this is very optional as harmonics are arlready normalized to high
    # accuracy by construction. However, the stencil in theta may cause minor departures
    if force_norm:
        norm = lambda x: x/sqrt( prod(x,x,theta) )
        for k,llk in enumerate(lrange):
            aSspace[k,:] = norm( aSspace[k,:] )
            Yspace[k,:]  = norm(  Yspace[k,:] )
            Sspace[k,:]  = norm(  Sspace[k,:] )
    
    # Create maps between ell and harmonics
    foo,bar,sun = {},{},{}
    for k,llk in enumerate(lrange):
        foo[ llk ] = aSspace[k,:]
        bar[ llk ] =  Yspace[k,:]
        sun[ llk ] =  Sspace[k,:]
        
    # Package output
    ans = {}
    ans['Ylm'] = bar
    ans['AdjSlm'] = foo
    ans['Slm'] = sun
    ans['lnspace'] = lrange 
    ans['Yspace'] = Yspace
    ans['aSspace'] = aSspace
    ans['YSGramian'] = beta
    ans['overtone_index'] = n
    ans['matrix_op'] = L_ddag
    ans['ZAX'] = (Z,A,X)
    
    # Return output
    return ans
    
#
def slmcg_helper( aw, s, l, m, lmin=None, lmax=None, span=6 ):
    '''
    Compute matrix elements of spheroidal differential operator in spherical harmonic basis
    londonl@mit.edu 2020 
    '''        
    
    # Import usefuls
    from scipy.linalg import eig,inv
    from numpy import array,zeros,zeros_like,exp,double
    from numpy import ones,arange,ndarray,complex128

    # Preliminaries
    # ------------------------------ #

    # Handle input format
    if isinstance(aw,(list,ndarray)):
        if len(aw)>1:
            error('first input as iterable not handled; fun function on each element')
        else:
            aw = aw[0]
            
    # if lmin in None, set it relative to l
    if lmin is None: lmin = max(l-span,max(abs(s),abs(m)))
    # if lmax in None, set it relative to l
    if lmax is None: lmax = l+span
    
    # Define index range and perform precomputations
    lrange = range(lmin,lmax+1); num_ell = len(lrange)
    aw2 = aw*aw; c1 = -2*aw*s; c2 = aw2

    # Main bits
    # ------------------------------ #

    # Eigenvalue for non-spinning solution
    A0 = lambda ll: (ll-s)*(1+ll+s)

    # Make lambdas to reduce duplicate code
    # TODO: determine which clebsch gordan method is faster
    # # Possibly the faster option, but throws warnings which must be investigated
    # c1_term = lambda llj,llk: c1*swsh_clebsh_gordan_prods(llj,m,s,0,1,llk-llj)
    # c2_term = lambda llj,llk: c2*swsh_clebsh_gordan_prods(llj,m,s,0,2,llk-llj)
    
    # Safer option, likely
    c1_term = lambda llj,llk: c1*swsh_prod_cos(s,llj,llk,m,1)
    c2_term = lambda llj,llk: c2*swsh_prod_cos(s,llj,llk,m,2)

    # Pre-allocate and then fill the coefficient matrix
    Q = zeros((num_ell,num_ell),dtype=complex128)
    for j,lj in enumerate(lrange):
        for k,lk in enumerate(lrange):

            # Populate the coefficient matrix
            if   lk == lj-2:
                Q[j,k] = c2_term(lj,lk)
            elif lk == lj-1:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)
            elif lk == lj+0:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)-A0(lj)
            elif lk == lj+1:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)
            elif lk == lj+2:
                Q[j,k] = c2_term(lj,lk)
            else:
                Q[j,k] = 0

    # Use scipy to find the eigenvalues and eigenvectors,
    # aka the spheroidal eigenvalues, and lists of spherical-spheroidal inner-products
    vals,vecs = eig(Q)  
    
    #
    dex_map = { ll:lrange.index(ll) for ll in lrange }
    sep_consts = vals
    ysprod_array = vecs

    # Extract spherical-spheroidal inner-products of interest
    ysprod_vec = ysprod_array[ :,dex_map[l] ]
    
    #
    return Q,vals,vecs,lrange  
  #

#
def aslmcg2_helper( a, s, l, m, lmin=None, lmax=None, span=6 ):
    '''
    Compute matrix elements of spheroidal differential operator in spherical harmonic basis
    londonl@mit.edu 2020 
    '''        
    
    # Import usefuls
    from scipy.linalg import eig,inv
    from numpy import array,zeros,zeros_like,exp,double
    from numpy import ones,arange,ndarray,complex128,conj

    # Preliminaries
    # ------------------------------ #
    error('experimental function version. do not use')
    
    #
    w = leaver(a,l,m,0)[0]
    
    #
    aw = a*w

    # Handle input format
    if isinstance(aw,(list,ndarray)):
        if len(aw)>1:
            error('first input as iterable not handled; fun function on each element')
        else:
            aw = aw[0]
            
    # if lmin in None, set it relative to l
    if lmin is None: lmin = max(l-span,max(abs(s),abs(m)))
    # if lmax in None, set it relative to l
    if lmax is None: lmax = l+span

    # Main bits
    # ------------------------------ #

    # Eigenvalue for non-spinning solution
    A0 = lambda ll: (ll-s)*(1+ll+s)

    # Make lambdas to reduce duplicate code
    # TODO: determine which clebsch gordan method is faster
    # # Possibly the faster option, but throws warnings which must be investigated
    # c1_term = lambda llj,llk: c1*swsh_clebsh_gordan_prods(llj,m,s,0,1,llk-llj)
    # c2_term = lambda llj,llk: c2*swsh_clebsh_gordan_prods(llj,m,s,0,2,llk-llj)

    # Pre-allocate and then fill the coefficient matrix
    lrange = range(lmin,lmax+1); num_ell = len(lrange)
    print(l,m,s,lmin,lmax,lrange)
    Q = zeros((num_ell,num_ell),dtype=complex128)
    for j,lj in enumerate(lrange):
        
        # Load QNM frequency 
        awj = a*leaver(a,lj,m,0)[0]
        
        for k,lk in enumerate(lrange):
            
            # Load QNM frequency 
            awk = a*leaver(a,lk,m,0)[0]
    
            # Define index range and perform precomputations
            c1 = -2*s; c2 = awk
    
            # Safer option, likely
            lam = awk*awj/conj(awj)
            c1_term = lambda llj,llk: lam*c1*swsh_prod_cos(s,llj,llk,m,1)
            c2_term = lambda llj,llk: lam*c2*swsh_prod_cos(s,llj,llk,m,2)

            # Populate the coefficient matrix
            if   lk == lj-2:
                Q[j,k] = c2_term(lj,lk)
            elif lk == lj-1:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)
            elif lk == lj+0:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)-A0(lj)
            elif lk == lj+1:
                Q[j,k] = c1_term(lj,lk)+c2_term(lj,lk)
            elif lk == lj+2:
                Q[j,k] = c2_term(lj,lk)
            else:
                Q[j,k] = 0

    # Use scipy to find the eigenvalues and eigenvectors,
    # aka the spheroidal eigenvalues, and lists of spherical-spheroidal inner-products
    vals,vecs = eig(Q.T.conj())  
    
    #
    dex_map = { ll:lrange.index(ll) for ll in lrange }
    sep_consts = vals
    ysprod_array = vecs

    # Extract spherical-spheroidal inner-products of interest
    ysprod_vec = ysprod_array[ :,dex_map[l] ]
    
    #
    return Q,vals,vecs,lrange  
            
# Compute adjoint-spheroidal harmonics with clebsh-gordan coefficients from scipy
def aslmcg2( a, s, l, m, n, theta, phi, lmin=None, lmax=None, span=6, full_output=True ):

    '''
    Use Clebsh-Gordan coefficients to calculate spheroidal harmonics
    londonl@mit.edu 2015+2020

    '''

    # Import usefuls
    from scipy.linalg import eig,inv
    from numpy import array,zeros,zeros_like,exp,double
    from numpy import ones,arange,ndarray,complex128

    # Preliminaries
    # ------------------------------ #
    # error('experimental function version. do not use')

    # Handle input format
    if isinstance(a,(list,ndarray)):
        if len(a)>1:
            error('first input as iterable not handled; fun function on each element')
        else:
            a = a[0]
            
    # if lmin in None, set it relative to l
    if lmin is None: lmin = max(l-span,max(abs(s),abs(m)))
    # if lmax in None, set it relative to l
    if lmax is None: lmax = l+span
    
    # Define index range and perform precomputations
    lrange = range(lmin,lmax+1); num_ell = len(lrange)
    print(lmin,max(l-span,max(abs(s),abs(m))))
    print('>> ',l,m,s,lmin,lmax,lrange)

    # Main bits
    # ------------------------------ #
    
    # Use helper function to calculate matrx elements
    Q,vals,vecs,lrange = aslmcg2_helper( a, s, l, m, lmin=lmin, lmax=lmax, span=span )

    #
    dex_map = { ll:lrange.index(ll) for ll in lrange }
    sep_consts = vals
    ysprod_array = vecs

    # Extract spherical-spheroidal inner-products of interest
    ysprod_vec = ysprod_array[ :,dex_map[l] ]

    # Compute Spheroidal Harmonic
    S = zeros_like(theta,dtype=complex128)
    for k,lp in enumerate(lrange):
        S += sYlm(s,lp,m,theta,0) * ysprod_vec[k]
    S *= exp(1j*m*phi)

    # Extract separation constant. Account for sign convention
    A = -sep_consts[ dex_map[l] ]

    # Package output
    # ------------------------------ #

    # Initialize answer
    if full_output:
        ans = {}
        # Spheroidal harmonic and separation constant
        ans['standard_output'] = (S,A)
        # All separation constants
        ans['sep_consts'] = sep_consts
        # Array and l specific ysprods
        ans['ysprod_array'] = ysprod_array
        ans['ysprod_vec'] = ysprod_vec
        # Coefficient matrix
        ans['coeff_array'] = Q
        # store space of l values considered
        ans['lrange'] = lrange
        # map between l and index
        ans['dex_map'] = dex_map
    else:
        # Only output harmonic and sep const
        ans = S,A

    # Return asnwer
    return ans

            
# Compute spheroidal harmonics with clebsh-gordan coefficients from scipy
def slmcg( aw, s, l, m, theta, phi, lmin=None, lmax=None, span=6, full_output=False ):

    '''
    Use Clebsh-Gordan coefficients to calculate spheroidal harmonics
    londonl@mit.edu 2015+2020

    '''

    # Import usefuls
    from scipy.linalg import eig,inv
    from sympy.physics.quantum import cg
    from numpy import array,zeros,zeros_like,exp,double
    from numpy import ones,arange,ndarray,complex128

    # Preliminaries
    # ------------------------------ #

    # Handle input format
    if isinstance(aw,(list,ndarray)):
        if len(aw)>1:
            error('first input as iterable not handled; fun function on each element')
        else:
            aw = aw[0]

    # Main bits
    # ------------------------------ #
    
    # Use helper function to calculate matrx elements
    Q,vals,vecs,lrange = slmcg_helper( aw, s, l, m, lmin=lmin, lmax=lmax, span=span )

    #
    dex_map = { ll:lrange.index(ll) for ll in lrange }
    sep_consts = vals
    ysprod_array = vecs

    # Extract spherical-spheroidal inner-products of interest
    ysprod_vec = ysprod_array[ :,dex_map[l] ]

    # Compute Spheroidal Harmonic
    S = zeros_like(theta,dtype=complex128)
    for k,lp in enumerate(lrange):
        S += sYlm(s,lp,m,theta,0) * ysprod_vec[k]
    S *= exp(1j*m*phi)

    # Extract separation constant. Account for sign convention
    A = -sep_consts[ dex_map[l] ]

    # Package output
    # ------------------------------ #

    # Initialize answer
    if full_output:
        ans = {}
        # Spheroidal harmonic and separation constant
        ans['standard_output'] = (S,A)
        # All separation constants
        ans['sep_consts'] = sep_consts
        # Array and l specific ysprods
        ans['ysprod_array'] = ysprod_array
        ans['ysprod_vec'] = ysprod_vec
        # Coefficient matrix
        ans['coeff_array'] = Q
        # store space of l values considered
        ans['lrange'] = lrange
        # map between l and index
        ans['dex_map'] = dex_map
    else:
        # Only output harmonic and sep const
        ans = S,A

    # Return asnwer
    return ans


# Function to calculate "chi_p"
def calc_chi_p(m1,X1,m2,X2,L):
    '''
    Calculate chi_p: see eqn 3.4 of https://arxiv.org/pdf/1408.1810.pdf
    '''
    #
    from numpy import dot,array
    from numpy.linalg import norm
    
    #
    if m1<m2:
        m1,m2 = [ float(k) for k in (m2,m1) ]
        X1,X2 = [ array(k) for k in (X2,X1) ]

    #
    l = L/norm(L)
    
    #
    X1_l = l * dot( l, X1 )
    X1_perp = X1 - X1_l
    
    #
    X2_l = l * dot( l, X2 )
    X2_perp = X2 - X2_l
    
    #
    A1 = 2 + (3*m2)/(2*m1)
    A2 = 2 + (3*m1)/(2*m2)
    
    #
    m1_squared = m1*m1
    m2_squared = m2*m2
    S1_perp = norm( X1_perp * m1_squared )
    S2_perp = norm( X2_perp * m2_squared )
    
    #
    B1 = A1 * S1_perp
    B2 = A2 * S2_perp
    
    #
    chip = max( B1,B2 ) / ( A1 * m1_squared )
    
    #
    return chip
    
#
def calc_chi_eff(m1,X1,m2,X2,L):
    '''
    Calculate chi_s: see eqn 2 of https://arxiv.org/pdf/1508.07253.pdf
    '''
    #
    from numpy import dot,array
    from numpy.linalg import norm

    #
    l = L/norm(L)
    
    # #
    # X1_l = l * dot( l, X1 )
    # X2_l = l * dot( l, X2 )
    # X_eff = ( X1_l*m1 + X2_l*m2 ) / (m1+m2)
    # chi_eff = dot( l, X_eff )
    
    #
    chi_eff = (m1*dot( l, X1 ) + m2*dot( l, X2 ))/(m1+m2)
    
    #
    return chi_eff

#
def Schwarzschild_tortoise(r,M):
    '''
    Calculate the Schwazschild radial tortoise coordinate: 
    '''
    #
    from numpy import log
    #

    radial_tortoise = r + 2 * M * log( r / ( 2 * M ) - 1 )

    #
    return radial_tortoise
