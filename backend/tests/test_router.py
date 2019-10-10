from router import Router


def test_is_singleton():
    assert Router() is Router()



