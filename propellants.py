class propellant:
    def get_name(self):
        return self.name
    def get_MW(self):
        return self.MW

class H2(propellant):
    def __init__(self):
        self.name = "Hydrogen (H2)"
        self.MW = 2.01588

    def get_h(self, T):
        # takes T in K
        # returns enthalpy in J kg-1

        # this function is a polynomial fit on NIST data on 1 bar
        # with R = 0.9996
        return (0.0009 * T**2 + 13.388 * T - 97.507) * 1000

    def get_T_by_h(self, h):
        # takes h in J kg-1
        # returns T in K
        # for 1 bar only

        # is a reverse of get_h()
        return (-13388 + (3.6*h + 179589569.2)**0.5)/1.8

    def get_gamma(self, T):
        # takes T in K
        # returns gamma (unitless)

        return 1.43

    def get_speed_of_sound(self, T):
        # takes T in K
        # returns speed of sound in m s-1

        # this function is a polynomial fit on NIST data on 1 bar
        # with R = 0.9988
        return -5E-9 * T**4 + 1E-5 * T**3 - 0.0104 * T**2 + 5.7013 * T + 290.43
