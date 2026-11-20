"""
codigo/testes/test_materiais.py

Testes unitários (pytest) para codigo/materiais.py — Aula 02.
Rodar com: pytest codigo/testes/test_materiais.py -v
"""

import pytest
from materiais import parametros_concreto, tensao_concreto, tensao_aco, eps_yd


def test_parametros_concreto_c30_eta_c_igual_1():
    p = parametros_concreto(30)
    assert p["eta_c"] == pytest.approx(1.0)
    assert p["n"] == 2.0
    assert p["eps_c2"] == pytest.approx(0.0020)
    assert p["eps_cu"] == pytest.approx(0.0035)


def test_parametros_concreto_c30_sigma_plat():
    p = parametros_concreto(30)
    assert p["sigma_plat"] == pytest.approx(18.21, abs=0.05)


def test_parametros_concreto_acima_40_reduz_eta_c():
    p = parametros_concreto(60)
    assert p["eta_c"] < 1.0


def test_tensao_concreto_c30_em_eps_0001():
    p = parametros_concreto(30)
    sigma = tensao_concreto(0.001, p)
    assert float(sigma) == pytest.approx(13.66, abs=0.05)


def test_tensao_concreto_nula_em_tracao():
    p = parametros_concreto(30)
    sigma = tensao_concreto(-0.001, p)
    assert float(sigma) == pytest.approx(0.0)


def test_tensao_concreto_patamar_constante_apos_eps_c2():
    p = parametros_concreto(30)
    sigma_no_c2 = float(tensao_concreto(p["eps_c2"], p))
    sigma_apos = float(tensao_concreto(p["eps_c2"] + 0.0005, p))
    assert sigma_apos == pytest.approx(sigma_no_c2, abs=1e-9)
    assert sigma_apos == pytest.approx(p["sigma_plat"], abs=1e-9)


def test_tensao_aco_ca50_fyd():
    sigma = tensao_aco(0.01, fyk=500)  # deformação grande -> escoamento
    assert float(sigma) == pytest.approx(434.78, abs=0.05)


def test_tensao_aco_simetrico_em_compressao():
    sigma_pos = tensao_aco(0.01, fyk=500)
    sigma_neg = tensao_aco(-0.01, fyk=500)
    assert float(sigma_neg) == pytest.approx(-float(sigma_pos))


def test_eps_yd_ca50():
    assert eps_yd(500) == pytest.approx(0.002070, abs=1e-5)


def test_tensao_aco_regime_elastico_antes_do_escoamento():
    eps = 0.001  # menor que eps_yd (~0.00207)
    sigma = tensao_aco(eps, fyk=500)
    assert float(sigma) == pytest.approx(210000 * eps, abs=0.5)