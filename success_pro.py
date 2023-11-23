from scipy.stats import norm

def Ps(SN, s, h):
    a = norm.ppf(1-2**(-h))
    prob = norm.cdf(((s * SN)**(1/2) - a)/(SN + 1)**(1/2))
    return prob

if __name__ == "__main__":
    h = 10
    s = 2*10
    SN = 2**(-34)/ 2**(-64)
    prob = Ps(SN, s, h)
    print(prob)