# Post
def test_post_str(post):
    assert post.__str__() == post.slug


# PostImage
def test_post_image_str(post_image):
    assert post_image.__str__() == post_image.image


def test_post_image_author(post_image):
    assert post_image.author() == post_image.post.author.username
