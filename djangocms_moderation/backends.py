import uuid


def uuid4_backend(**kwargs):
    return uuid.uuid4()


def sequential_number_backend(**kwargs):
    """
    This backed uses moderation request's primary key to produce readable
    semi-sequential numbers
    """
    return "{}".format(kwargs['moderation_request'].pk)
