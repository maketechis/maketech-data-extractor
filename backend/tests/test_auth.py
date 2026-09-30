from app.services.auth import hash_password,verify_password
def test_password_hash_roundtrip():
    hashed=hash_password("a-secure-test-password")
    assert verify_password("a-secure-test-password",hashed)
    assert not verify_password("wrong",hashed)
