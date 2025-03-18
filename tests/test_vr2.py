from proper.Hasher import VR2Hasher


def test_vr2_keys(vr2_env):
    hasher = VR2Hasher(hash_seed=vr2_env["vr2_seed"], calculate_randoms=False, vr2_keys=vr2_env["vr2_keys"])
    assert hasher.keys == vr2_env["vr2_keys"]


def test_hash_empty(vr2_env):
    hasher = VR2Hasher(
        hash_seed=vr2_env["vr2_seed"],
        calculate_randoms=False,
        vr2_keys=vr2_env["vr2_keys"],
    )
    assert hasher.hash("") == 0x80000290


def test_hash_test23(vr2_env):
    hasher = VR2Hasher(
        hash_seed=vr2_env["vr2_seed"],
        calculate_randoms=False,
        vr2_keys=vr2_env["vr2_keys"],
    )
    assert hasher.get_keys() == vr2_env["vr2_keys"]
    assert hasher.hash("test23") == 0x968a01bb


def test_hash_test23_mt(vr2_env):
    hasher = VR2Hasher(
        hash_seed=vr2_env["vr2_seed"],
        calculate_randoms=True,
        encryption_string=vr2_env["access_token"],
    )
    
    assert hasher.get_keys() == vr2_env["vr2_keys"]
    assert hasher.hash("test23") == 0x968A01BB


def test_hash_test23_mt_seeded(vr2_env):
    hasher = VR2Hasher(
        hash_seed=vr2_env["vr2_seed"],
        calculate_randoms=True,
        mt_seed_array=vr2_env["mt_state_array_seeds"],
        encryption_string=vr2_env["access_token"],
    )
    assert hasher.get_keys() == vr2_env["vr2_keys"]
    assert hasher.hash("test23") == 0x968A01BB


def test_hash_test23_enc_string(vr2_env):
    hasher = VR2Hasher(
        hash_seed=vr2_env["vr2_seed"],
        calculate_randoms=False,
        encryption_string=vr2_env["access_token"],
    )
    assert hasher.get_keys() == vr2_env["vr2_keys"]
    assert hasher.hash("test23") == 0x968A01BB
