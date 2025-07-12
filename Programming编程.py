import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
# Physical constants
m0 = 9.1093837e-31 # Electron mass (kg)
hbar = 1.0545718e-34 # Reduced Planck constant (J·s)
e_charge = 1.60217662e-19 # Electron charge (C)
def programming_coefficient(d_tun, V_prog, C_control, C_tunnel,
                           electron_energy=0.0, # Electron energy (eV)
                           phi_b=3.2, # Barrier height (eV)
                           m_star_ratio=0.42): # Effective mass ratio
    d_tun_m = d_tun * 1e-9
    C_control_F = C_control * 1e-15
    C_tunnel_F = C_tunnel * 1e-15
    C_total = C_control_F + C_tunnel_F
    V_tun = V_prog * (C_control_F / C_total)  # Voltage division
    E_tun = V_tun / d_tun_m  # Electric field strength (V/m)
    m_star = m_star_ratio * m0
    phi_b_J = phi_b * e_charge
    E_J = electron_energy * e_charge
    delta_energy = max(phi_b_J - E_J, 1e-20)
    energy_term = delta_energy ** 1.5  # (V0-E)^(3/2)
    K = (4 * np.sqrt(2 * m_star)) / (3 * hbar * e_charge * E_tun)
    exponent = -K * energy_term
    return np.exp(exponent)
def main_programming_analysis():
    # Fixed parameters (consistent with erase phase)
    d_control = 40 # Control oxide thickness (nm)
    d_tunnel = 20 # Tunnel oxide thickness (nm)
    C_control = 40 # Control gate capacitance (fF)
    C_tunnel = 20 # Tunnel capacitance (fF)
    prog_voltage = 12 # Programming voltage (V)
    plt.figure(figsize=(12, 18))
    plt.subplot(3, 1, 1)
    d_tun_range = np.linspace(7, 25, 100)
    energy_levels = [0.0, 0.3, 0.6] # Electron energy (eV)
    line_styles = ['b-', 'r--', 'g:'] # Line styles
    for energy, style in zip(energy_levels, line_styles):
        T_values = [programming_coefficient(d, prog_voltage, C_control, C_tunnel, 
                                          electron_energy=energy) 
                   for d in d_tun_range]
        plt.plot(d_tun_range, T_values, style, linewidth=2, label=f'E = {energy} eV')
    plt.title('Programming: Effect of Tunnel Oxide Thickness on Transmission Coefficient (V_prog=12V)', fontsize=14)
    plt.xlabel('Tunnel Oxide Thickness (nm)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.subplot(3, 1, 2)
    V_prog_range = np.linspace(5, 25, 100)
    for energy, style in zip(energy_levels, line_styles):
        T_values = [programming_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                          electron_energy=energy) 
                   for V in V_prog_range]
        plt.plot(V_prog_range, T_values, style, linewidth=2, label=f'E = {energy} eV')
    plt.title('Programming: Effect of Programming Voltage on Transmission Coefficient (d_tunnel=20nm)', fontsize=14)
    plt.xlabel('Programming Voltage (V)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.subplot(3, 1, 3)
    C_ratio_range = np.linspace(2, 8, 100)
    for energy, style in zip(energy_levels, line_styles):
        T_values = [programming_coefficient(d_tunnel, prog_voltage, C_control*ratio, C_tunnel, 
                                          electron_energy=energy) 
                   for ratio in C_ratio_range]
        plt.plot(C_ratio_range, T_values, style, linewidth=2, label=f'E = {energy} eV')
    plt.title('Programming: Effect of Capacitance Ratio on Transmission Coefficient (V_prog=12V, d_tunnel=20nm)', fontsize=14)
    plt.xlabel('Capacitance Ratio (C_control/C_tunnel)', fontsize=12)
    plt.ylabel('Transmission Coefficient T', fontsize=12)
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.figtext(0.5, 0.01, r'$T_{\text{prog}} = e^{-\frac{4\sqrt{2m}}{3\hbar e E_{\text{field}}}} (V_0-E)^{\frac{3}{2}}$', 
               fontsize=14, ha='center', bbox=dict(facecolor='white', alpha=0.8))
    plt.tight_layout(rect=(0, 0.05, 1, 0.98))
    plt.subplots_adjust(hspace=0.35)
    plt.savefig('programming_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("\nKey parameter threshold analysis (T > 1e-6):")
    for energy in energy_levels:
        T_values_d = [programming_coefficient(d, prog_voltage, C_control, C_tunnel, 
                                           electron_energy=energy) 
                     for d in d_tun_range]
        viable_d = d_tun_range[np.array(T_values_d) > 1e-6]
        max_d = viable_d[-1] if len(viable_d) > 0 else "N/A"
        T_values_V = [programming_coefficient(d_tunnel, V, C_control, C_tunnel, 
                                           electron_energy=energy) 
                     for V in V_prog_range]
        viable_V = V_prog_range[np.array(T_values_V) > 1e-6]
        min_V = viable_V[0] if len(viable_V) > 0 else "N/A"
        T_values_C = [programming_coefficient(d_tunnel, prog_voltage, C_control*ratio, C_tunnel, 
                                           electron_energy=energy) 
                     for ratio in C_ratio_range]
        viable_C = C_ratio_range[np.array(T_values_C) > 1e-6]
        min_C = viable_C[0] if len(viable_C) > 0 else "N/A"
        print(f"E={energy}eV: Max thickness={max_d:.1f}nm | Min voltage={min_V:.1f}V | Min capacitance ratio={min_C:.1f}")
if __name__ == "__main__":
    main_programming_analysis()
