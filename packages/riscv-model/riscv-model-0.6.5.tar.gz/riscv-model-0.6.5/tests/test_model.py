from riscvmodel.program.tests import *
from riscvmodel.program.tests_atomic import *
from riscvmodel.model import Model
from riscvmodel.variant import RV32I, RV32A

import pytest


def check_model(model: Model, check: dict):
    diff = []
    for key, value in check.items():
        if isinstance(key, int):
            if model.state.intreg[key].unsigned() != value:
                diff.append("x{} mismatch: expected {:08x}, got {:08x}".format(key, value, model.state.intreg[key].unsigned()))
    if len(diff) > 0:
        msg = "Check failed\n{}".format("\n  ".join(diff))
        pytest.fail(msg)


def test_model_addi():
    pgm = ADDITest()
    m = Model(RV32I)
    m.execute(pgm)
    check_model(m, pgm.expects())


def test_model_lr_sc():
    """Test if load-reserved and store-conditional sequence works"""
    pgm = LRSCTest()
    m   = Model(RV32A)
    m.execute(pgm)
    check_model(m, pgm.expects())