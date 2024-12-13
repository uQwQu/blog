import pytest
from pytest_factoryboy import register

from tests.factories import ProfileFactory, UserFactory, PostFactory, PostImageFactory

register(UserFactory)
register(ProfileFactory)
register(PostFactory)
register(PostImageFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def profile(db, profile_factory):
    user_profile = profile_factory.create()
    return user_profile


@pytest.fixture
def post(db, post_factory):
    post = post_factory.create()
    return post


@pytest.fixture
def post_image(db, post_image_factory):
    post_image = post_image_factory.create()
    return post_image
