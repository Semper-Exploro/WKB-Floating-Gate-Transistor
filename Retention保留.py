import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, m_e, e
import warnings
class FloatingGateRetention:
    def __init__(self):
        self.hbar = hbar  # 约化普朗克常数 (J·s)
        self.m_e = m_e    # 电子质量 (kg)
        self.V0 = 3.20 * e  # 势垒高度 (J)
        self.E = 1.0 * e    # 电子能量 (J)
        self.m_eff = 0.42 * m_e  # 有效质量
        self.d_tun = 20e-9  # 隧穿氧化层厚度 (20nm)
        self.d_control = 40e-9  # 控制氧化层厚度 (40nm)
        self.d_fg = 10e-9   # 浮栅厚度 (10nm)
    def tunneling_factor(self, d, V_barrier):
        k = np.sqrt(2 * self.m_eff * (V_barrier - self.E)) / self.hbar
        return np.exp(-2 * k * d)
    def phase_accumulation(self):
        k_mid = np.sqrt(2 * self.m_eff * self.E) / self.hbar
        return k_mid * self.d_fg
    def calculate_denominator(self, T3, T1, T2):
        small_val = 1e-100  # 避免除零错误
        try:
            T1 = max(T1, small_val)
            T3 = max(T3, small_val)
            inv_T1 = 1 / T1
            term1 = (inv_T1 - T1/4) * np.exp(1j * T2)
            term2 = (T1/4 + inv_T1) * np.exp(-1j * T2)
            part1 = T3 * (term2 - term1)/4 
            part2 = (term1 + term2) / T3
            if abs(part2) > 1e100:
                log_part2 = np.log(np.abs(part2)) + 1j * np.angle(part2)
                denominator = np.exp(log_part2)
                return denominator
            return part1 + part2
        except FloatingPointError:
            return 1e10 * small_val
    def transmission_coefficient(self):
        T3 = self.tunneling_factor(self.d_tun, self.V0)
        T1 = self.tunneling_factor(self.d_control, self.V0)
        T2 = self.phase_accumulation()
        denominator = self.calculate_denominator(T3, T1, T2)
        trans_coeff = np.abs(1 / denominator)**2
        if trans_coeff < 1e-300:
            return 1e-300
        return trans_coeff
    def analyze_thickness_impact(self):
        d_range = np.linspace(7e-9, 25e-9, 200)  # 7-25nm
        T_values = []
        for d in d_range:
            self.d_tun = d
            tc = self.transmission_coefficient()
            T_values.append(tc)
        plt.figure()
        valid_idx = np.array(T_values) > 0
        plt.semilogy(np.array(d_range)[valid_idx] * 1e9, np.array(T_values)[valid_idx], 'b-')
        plt.xlabel('Tunnel Oxide Thickness (nm)')
        plt.ylabel('Transmission Coefficient (log scale)')
        plt.title('Impact of Tunnel Oxide Thickness')
        plt.grid(True, which="both", ls="-")
        plt.show()
        return d_range, T_values
    def analyze_energy_impact(self):
        """分析电子能量影响"""
        E_range = np.linspace(0.1 * e, 0.95 * self.V0, 200)  # 避免等于V0
        T_values = []
        for energy in E_range:
            self.E = energy
            tc = self.transmission_coefficient()
            T_values.append(tc)
        plt.figure()
        plt.plot(E_range / e, T_values, 'r-')
        plt.xlabel('Electron Energy (eV)')
        plt.ylabel('Transmission Coefficient')
        plt.title('Impact of Electron Energy')
        plt.grid(True)
        plt.show()
        return E_range / e, T_values
    def analyze_floating_gate_impact(self):
        d_range = np.linspace(5e-9, 30e-9, 200)  # 5-30nm
        T_values = []
        for d in d_range:
            self.d_fg = d
            tc = self.transmission_coefficient()
            T_values.append(tc)
        plt.figure()
        plt.plot(d_range * 1e9, T_values, 'g-')
        plt.xlabel('Floating Gate Thickness (nm)')
        plt.ylabel('Transmission Coefficient')
        plt.title('Impact of Floating Gate Thickness')
        plt.ylim(bottom=1e-150) # y轴下限拓展到1e-150
        plt.grid(True)
        plt.show()
        return d_range * 1e9, T_values
if __name__ == "__main__":
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    model = FloatingGateRetention()
    T_default = model.transmission_coefficient()
    print(f"Default Transmission Coefficient: {T_default:.3e}")
    model.analyze_thickness_impact() # 隧穿氧化层厚度影响
    model.analyze_energy_impact() # 电子能量影响
    model.analyze_floating_gate_impact() # 浮栅厚度影响
