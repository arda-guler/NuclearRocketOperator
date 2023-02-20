import math
pi = math.pi
uni_gas_const = uni_gas_const = 8.314472 # m2 kg s-2 K-1 mol-1

# this is for the supersoinc region of a nozzle
# do not use this for subsonic region as is
def calc_mach_num(A_ratio, gamma):

    gp1 = gamma + 1
    gm1 = gamma - 1

    arat = A_ratio
    aro = 2
    macho = 2.2

    fac1 = gp1/(2*gm1)
    machn = macho + 0.05

    while abs(A_ratio - aro) > .0001:
        fac = 1 + 0.5 * gm1 * machn**2
        arn = 1/(machn * fac**(-fac1) * (gp1/2)**fac1)
        
        try:
            deriv = (arn-aro)/(machn-macho)

        except ZeroDivisionError:
            print("\nFATAL: ZeroDivisionError in Mach number code. Try increasing area ratio.")
            input("Press Enter to quit...")
            quit()
            
        aro = arn
        macho = machn
        machn = macho + (arat - aro)/deriv
    
    return macho
