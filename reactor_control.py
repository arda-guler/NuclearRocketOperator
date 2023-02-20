def apply_reactor_commands(reactor, dt):

    k_target = 1 + (1 - reactor.neutrons) / 15
        
    if reactor.k_eff() > k_target:
        reactor.control_rod_insertion += reactor.control_rod_movement_speed * dt
        control_case = "A"

    elif reactor.k_eff() < k_target:
        reactor.control_rod_insertion -= reactor.control_rod_movement_speed * dt
        control_case = "B"

    if reactor.control_rod_insertion < 0:
        reactor.control_rod_insertion = 0
    elif reactor.control_rod_insertion > 1:
        reactor.control_rod_insertion = 1
