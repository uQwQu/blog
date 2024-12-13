def test_profile_str(profile):
    assert profile.__str__() == f"{profile.user.first_name}'s Profile"
