import pytest


def test_user_full_name(base_user):
    assert base_user.get_full_name == f"{base_user.first_name} {base_user.last_name}"


def test_base_user_email_is_normalized(base_user):
    email = "test@BLOG.COM"
    assert base_user.email == email.lower()


def test_super_user_email_is_normalized(super_user):
    email = "test@BLOG.COM"
    assert super_user.email == email.lower()


def test_super_user_is_not_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superusers must have is_staff=True"


def test_super_user_is_not_superuser(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superusers must have is_superuser=True"


def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "Base User Account: An email address is required"


def test_create_user_with_no_username(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "Users must submit a username"


def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "Users must submit a first name"


def test_create_user_with_no_lastname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "Users must submit a last name"


def test_create_superuser_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser Account: An email address is required"


def test_create_superuser_with_no_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=True, password=None)
    assert str(err.value) == "Superusers must have a password"


def test_user_email_incorrect(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="testblog.com")
    assert str(err.value) == "You must provide a valid email address"
