class radiator:
    def __init__(self, max_cooling):
        self.max_cooling = max_cooling # W
        self.heat_capacity = 1e6 # J K-1
        self.T_max = 700
        self.T_min = 20
        self.T = self.T_min

    def update(self, Q_in, dt):
        Q_out = (self.T**4 - self.T_min**4)/(self.T_max**4 - self.T_min**4) * self.max_cooling
        q_net = (Q_in - Q_out) * dt
        self.T += q_net/self.heat_capacity
