def hum_r2q(r):
    "Humidity conversion r(mix ratio) to q(bi shi)"
    return r / (1.0 + r)

def hum_q2r(q): #TODO
    "Humidity conversion q to r(mix ratio)"
    pass

def hum_e2r(e, p=p_std):
    "Humidity conversion e(vapor pressure) to r(mix ratio)"
    return epsilon_vapor * e / (p - e)

def hum_e2q(e, p=p_std):
    "Humidity conversion e(vapor pressure) to q(bi shi)"
    return epsilon_vapor * e / (p - 0.378 * e)
#TODO hum_r2e, hum_q2e

def hum_e2rho_v(e, T=T_std):
    "Humidity conversion e(vapor pressure) to rho_v(vapor density)"
    return epsilon_vapor * e / (R_d * T)



