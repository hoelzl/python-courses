from ..msg_utils import generate_id


def test_generate_id_generates_different_ids():
    assert generate_id() != generate_id()
