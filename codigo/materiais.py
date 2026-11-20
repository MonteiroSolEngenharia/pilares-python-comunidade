"""
codigo/materiais.py

Leis constitutivas de materiais no Estado-Limite Último (ELU).
Base do curso Pilares em Python (Prof. Ricardo Corsini) — Aula 02.

Convenções:
- Unidades: MPa (= N/mm²), deformações adimensionais (1‰ = 0.001).
- Compressão positiva, tração negativa (concreto não resiste à tração aqui).
- Este módulo calcula TENSÃO a partir de DEFORMAÇÃO. Ele NÃO valida se o
  estado de deformação é admissível (ex.: eps_c > eps_cu). Essa verificação
  é responsabilidade de outra camada (estado-limite / integração).
"""

import numpy as np


def parametros_concreto(fck, gamma_c=1.40):
    """
    Calcula os parâmetros de cálculo do concreto a partir de fck (MPa).

    Retorna um dict com:
        fcd, eta_c, n, eps_c2, eps_cu, sigma_plat
    """
    fcd = fck / gamma_c

    # Fator de redução eta_c
    if fck <= 40:
        eta_c = 1.0
    else:
        eta_c = (40.0 / fck) ** (1.0 / 3.0)

    # Parâmetros de forma do diagrama (faixa até 50 MPa)
    if fck <= 50:
        n = 2.0
        eps_c2 = 0.0020
        eps_cu = 0.0035
    else:
        # Faixa 50 < fck <= 90 MPa (fórmulas da apostila/NBR 6118)
        n = 1.4 + 23.4 * ((90.0 - fck) / 100.0) ** 4
        eps_c2 = 0.0020 + 0.000085 * (fck - 50.0) ** 0.53
        eps_cu = 0.0026 + 0.035 * ((90.0 - fck) / 100.0) ** 4

    sigma_plat = 0.85 * eta_c * fcd

    return {
        "fck": fck,
        "fcd": fcd,
        "eta_c": eta_c,
        "n": n,
        "eps_c2": eps_c2,
        "eps_cu": eps_cu,
        "sigma_plat": sigma_plat,
    }


def tensao_concreto(eps_c, params):
    """
    Tensão do concreto (MPa) em função da deformação eps_c (adimensional).
    Vetorizado: eps_c pode ser escalar ou array numpy.

    ATENÇÃO: não verifica se eps_c > eps_cu (estado inválido). Isso deve
    ser tratado pela camada de estado-limite.
    """
    eps_c = np.asarray(eps_c, dtype=float)

    n = params["n"]
    eps_c2 = params["eps_c2"]
    sigma_plat = params["sigma_plat"]

    # Ramo curvo: 0 < eps_c < eps_c2
    ramo_curvo = sigma_plat * (1.0 - (1.0 - eps_c / eps_c2) ** n)

    sigma = np.where(
        eps_c <= 0.0,
        0.0,
        np.where(eps_c < eps_c2, ramo_curvo, sigma_plat),
    )

    return sigma


def tensao_aco(eps_s, fyk, Es=210000.0, gamma_s=1.15):
    """
    Tensão do aço (MPa) — elastoplástico perfeito, simétrico.
    Vetorizado: eps_s pode ser escalar ou array numpy.
    """
    eps_s = np.asarray(eps_s, dtype=float)
    fyd = fyk / gamma_s
    sigma = np.clip(Es * eps_s, -fyd, fyd)
    return sigma


def eps_yd(fyk, Es=210000.0, gamma_s=1.15):
    """Deformação de escoamento de cálculo do aço."""
    fyd = fyk / gamma_s
    return fyd / Es


if __name__ == "__main__":
    # Conferência manual rápida (ver também codigo/testes/test_materiais.py)
    p30 = parametros_concreto(30)
    print("C30 sigma_plat:", round(p30["sigma_plat"], 2), "MPa (esperado ~18.21)")
    print("C30 sigma_c(0.001):", round(float(tensao_concreto(0.001, p30)), 2), "MPa (esperado ~13.66)")

    fyd = 500 / 1.15
    print("CA-50 fyd:", round(fyd, 2), "MPa (esperado ~434.78)")
    print("CA-50 eps_yd:", round(eps_yd(500), 6), "(esperado ~0.002070)")