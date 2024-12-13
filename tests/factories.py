import random

import factory
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from apps.posts.models import Post, PostImage
from apps.profiles.models import Profile
from django.db.models.signals import post_save
from faker import Factory as FakerFactory

faker = FakerFactory.create()
User = get_user_model()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda x: faker.first_name().lower())
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: "test@blog.com")
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    bio = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    avatar = factory.LazyAttribute(lambda x: faker.image_url())
    gender = factory.LazyAttribute(lambda x: "Other")
    country = factory.LazyAttribute(lambda x: faker.country_code())

    class Meta:
        model = Profile


@factory.django.mute_signals(post_save)
class PostFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory("tests.factories.UserFactory")
    title = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    slug = factory.LazyAttribute(lambda x: get_random_string(length=6))
    body = factory.LazyAttribute(lambda x: faker.paragraph(nb_sentences=5))
    banner_image = factory.LazyAttribute(lambda x: faker.image_url())
    upvotes = factory.LazyAttribute(lambda x: random.randint(0, 100))
    downvotes = factory.LazyAttribute(lambda x: random.randint(0, 100))

    class Meta:
        model = Post

    @factory.post_generation
    def set_upvoted_by(self, create, extracted, **kwargs):
        if extracted:
            self.upvoted_by.set(extracted)

    @factory.post_generation
    def set_downvoted_by(self, create, extracted, **kwargs):
        if extracted:
            self.downvoted_by.set(extracted)

    @factory.post_generation
    def set_bookmarked_by(self, create, extracted, **kwargs):
        if extracted:
            self.bookmarked_by.set(extracted)


@factory.django.mute_signals(post_save)
class PostImageFactory(factory.django.DjangoModelFactory):
    image = factory.LazyAttribute(lambda x: faker.image_url())
    post = factory.SubFactory("tests.factories.PostFactory")

    class Meta:
        model = PostImage
