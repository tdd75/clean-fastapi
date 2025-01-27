from app.infrastructure.helper.password_helper import hash_password, verify_password, gen_otp


class TestHashPassword:
    def test_hash_password_returns_different_hash_each_time(self):
        password = 'secret123'
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2
        assert hash1.startswith('$argon2')


class TestVerifyPassword:
    def test_verify_password_success(self):
        password = 'strongpass!'
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_failure(self):
        password = 'password1'
        hashed = hash_password(password)

        assert verify_password('wrongpassword', hashed) is False

    def test_verify_password_logs_on_exception(self, caplog):
        with caplog.at_level('ERROR'):
            result = verify_password('123', 'invalid-hash')
            assert result is False
            assert any('Traceback' not in record.message for record in caplog.records)


class TestGenOtp:
    def test_gen_otp_length(self):
        otp = gen_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_gen_otp_custom_length(self):
        otp = gen_otp(8)
        assert len(otp) == 8
        assert otp.isdigit()

    def test_gen_otp_randomness(self):
        otp1 = gen_otp()
        otp2 = gen_otp()
        assert otp1 != otp2
