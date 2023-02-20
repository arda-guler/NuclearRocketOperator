class fission_reactor:
    def __init__(self):
        self.prompt_neutron_lifetime = 1e-4
        self.mean_generation_lifetime = 0.1
        self.neutrons = 1
        self.neutron_number_scale = 1e11
        self.control_rod_relative_cross_section = 0.4
        
        self.thermal_fission_factor = 1.65
        self.thermal_utilization_factor = 0.71
        self.resonance_escape_probability = 0.87
        self.fast_fission_factor = 1.02
        
        self.fast_non_leakage_probability = 0.97
        self.thermal_non_leakage_probability = 0.99

        self.power_rate = 150e6 # W
        self.control_rod_insertion = 0.3
        self.control_rod_movement_speed = 0.05 # percent per second

        self.spontaneous_rate = 0.0001

    def update(self, dt):
        if self.control_rod_insertion < 0:
            self.control_rod_insertion = 0
        elif self.control_rod_insertion > 1:
            self.control_rod_insertion = 1

        self.thermal_utilization_factor = 0.8/(1 + self.control_rod_insertion * self.control_rod_relative_cross_section)
            
        #self.neutrons *= 1 + (self.k_eff() - 1) * (dt/self.mean_generation_lifetime)
        self.neutrons = self.neutrons * self.k_eff()**(dt/self.mean_generation_lifetime)

        if self.neutrons < self.spontaneous_rate:
            self.neutrons = self.spontaneous_rate

    def k_inf(self):
        return self.thermal_fission_factor * self.thermal_utilization_factor * self.resonance_escape_probability * self.fast_fission_factor

    def k_eff(self):
        return self.k_inf() * self.fast_non_leakage_probability * self.thermal_non_leakage_probability

    def power_output(self):
        return self.neutrons * self.power_rate
