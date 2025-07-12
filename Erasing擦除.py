import numpy as np
import matplotlib.pyplot as plt
m0 = 9.1093837e-31 # Electron mass (kg)
hbar = 1.0545718e-34  # Reduced Planck constant (J·s)
e_charge = 1.60217662e-19 # Electron charge (C)
def corrected_erasing_coefficient(d_tun, V_erase, C_control, C_tunnel,
                                 electron_energy=0.0, # Electron energy (eV)
                                 phi_b=3.2, # Barrier height (eV)
                                 m_star_ratio=0.42): # Effective mass ratio
    d_tun_m = d_tun * 1e-9
    C_control_F = C_control * 1e-15
    C_tunnel_F = C_tunnel * 1e-15
    C_total = C_control_F + C_tunnel_F
    V_tun = abs(V_erase) * (C_control_F / C_total)
    E_tun = V_tun / d_tun_m
    m_star = m_star_ratio * m0
    phi_b_J = phi_b * e_charge
    E_J = electron_energy * e_charge
    delta_energy = max(phi_b_J - E_J, 1e-20)  # V₀-E
    energy_term = delta_energy ** 1.5  # (V₀-E)^{3/2}
    numerator = 4 * np.sqrt(2 * m_star) * energy_term
    denominator = 3 * hbar * e_charge * E_tun
    exponent = - numerator / denominator
    return np.exp(exponent)
def main_analysis():
    d_control = 40 # Control oxide thickness (nm)
    d_tunnel = 20 # Tunnel oxide thickness (nm)
    C_control = 40 # Control gate capacitance (fF)
    C_tunnel = 20 # Tunnel capacitance (fF)
    erase_voltage = -12  # Erase voltage (V)
    plt.figure(figsize=(12, 18))
    plt.subplot(3, 1, 1)
    d_tun_range = np.linspace(7, 25, 100)
    T_energy0 = [corrected_erasing_coefficient(d, erase_voltage, C_control, C_tunnel, 
                                              electron_energy=0.0) for d in d_tun_range]
    T_energy03 = [corrected_erasing_coefficient(d, erase_voltage, C_control, C_tunnel, 
                                               electron_energy=0.3) for d in d_tun_range]
    T_energy06 = [corrected_erasing_coefficient(d, erase_voltage, C_control, C_tunnel, 
                                               electron_energy=0.6) for d in d_tun_range]
    plt.plot(d_tun_range, T_energy0, 'b-', linewidth=2, label='E=0.0 eV')
    plt.plot(d_tun_range, T_energy03, 'r--', linewidth=2, label='E=0.3 eV')
    plt.plot(d_tun_range, T_energy06, 'g:', linewidth=3, label='E=0.6 eV')
    for energy, style, color in zip([0.0, 0.3, 0.6], ['-', '--', ':'], ['b', 'r', 'g']):
        idx = np.argmax(np.array([corrected_erasing_coefficient(d, erase_voltage, C_control, C_tunnel, 
                                                              electron_energy=energy) 
                                 for d in d_tun_range]) > 1e-8)
        if idx > 0:
            plt.scatter(d_tun_range[idx], 1e-8, s=100, c=color, marker='*', 
                        label=f'E={energy}eV @ {d_tun_range[idx]:.1f}nm')

    plt.title('Erasing: Effect of Tunnel Oxide Thickness on Transmission Coefficient (V_erase=-12V)', fontsize=14)
    plt.xlabel('Tunnel Oxide Thickness (nm)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.subplot(3, 1, 2)
    V_erase_range = np.linspace(-5, -25, 100)
    T_energy0 = [corrected_erasing_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                              electron_energy=0.0) for V in V_erase_range]
    T_energy03 = [corrected_erasing_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                               electron_energy=0.3) for V in V_erase_range]
    T_energy06 = [corrected_erasing_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                               electron_energy=0.6) for V in V_erase_range]
    plt.plot(V_erase_range, T_energy0, 'b-', linewidth=2, label='E=0.0 eV')
    plt.plot(V_erase_range, T_energy03, 'r--', linewidth=2, label='E=0.3 eV')
    plt.plot(V_erase_range, T_energy06, 'g:', linewidth=3, label='E=0.6 eV')
    for energy, style, color in zip([0.0, 0.3, 0.6], ['-', '--', ':'], ['b', 'r', 'g']):
        viable_voltage = V_erase_range[np.array([corrected_erasing_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                                                             electron_energy=energy) 
                                               for V in V_erase_range]) > 1e-8]
        if len(viable_voltage) > 0:
            plt.scatter(viable_voltage[0], 1e-8, s=100, c=color, marker='*', 
                        label=f'E={energy}eV @ {viable_voltage[0]:.1f}V')
    plt.title('Erasing: Effect of Erase Voltage on Transmission Coefficient (d_tunnel=20nm)', fontsize=14)
    plt.xlabel('Erase Voltage (V)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.subplot(3, 1, 3)
    C_ratio_range = np.linspace(2, 8, 100)
    T_energy0 = [corrected_erasing_coefficient(d_tunnel, erase_voltage, C_control*ratio, C_tunnel, 
                                              electron_energy=0.0) for ratio in C_ratio_range]
    T_energy03 = [corrected_erasing_coefficient(d_tunnel, erase_voltage, C_control*ratio, C_tunnel, 
                                               electron_energy=0.3) for ratio in C_ratio_range]
    T_energy06 = [corrected_erasing_coefficient(d_tunnel, erase_voltage, C_control*ratio, C_tunnel, 
                                               electron_energy=0.6) for ratio in C_ratio_range]
    plt.plot(C_ratio_range, T_energy0, 'b-', linewidth=2, label='E=0.0 eV')
    plt.plot(C_ratio_range, T_energy03, 'r--', linewidth=2, label='E=0.3 eV')
    plt.plot(C_ratio_range, T_energy06, 'g:', linewidth=3, label='E=0.6 eV')
    for energy, style, color in zip([0.0, 0.3, 0.6], ['-', '--', ':'], ['b', 'r', 'g']):
        viable_ratio = C_ratio_range[np.array([corrected_erasing_coefficient(d_tunnel, erase_voltage, 
                                                                            C_control*ratio, C_tunnel, 
                                                                            electron_energy=energy) 
                                              for ratio in C_ratio_range]) > 1e-8]
        if len(viable_ratio) > 0:
            plt.scatter(viable_ratio[0], 1e-8, s=100, c=color, marker='*', 
                        label=f'E={energy}eV @ ratio={viable_ratio[0]:.1f}')

    plt.title('Erasing: Effect of Capacitance Ratio on Transmission Coefficient (V_erase=-12V, d_tunnel=20nm)', fontsize=14)
    plt.xlabel('Capacitance Ratio (C_control/C_tunnel)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)
    plt.savefig('corrected_erase_analysis.png', dpi=300)
    plt.show()
if __name__ == "__main__":
    main_analysis()
