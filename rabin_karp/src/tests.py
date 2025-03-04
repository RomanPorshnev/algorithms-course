from main import RabinKarp


def test_1():
    rk = RabinKarp("drain gang", "drain")
    rk.hashing()
    assert rk.get_ans() == "0"


def test_2():
    rk = RabinKarp("bladee ecco2k whitearmor", "ecco2k")
    rk.hashing()
    assert rk.get_ans() == "7"


def test_3():
    rk = RabinKarp("i'm fresh - thaiboy digital", "thaiboy digital")
    rk.hashing()
    assert rk.get_ans() == "12"


def test_4():
    rk = RabinKarp("abacaba", "aba")
    rk.hashing()
    assert rk.get_ans() == "0 4"


def test_5():
    rk = RabinKarp("abababab", "ab")
    rk.hashing()
    assert rk.get_ans() == "0 2 4 6"


def test_6():
    rk = RabinKarp("agsdfksahfaks", "ab")
    rk.hashing()
    assert rk.get_ans() == ""
