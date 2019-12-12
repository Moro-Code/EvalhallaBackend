


def generate_amqp_uri(**kwargs):
    host =  kwargs["AMQP_HOST"]
    port = kwargs["AMQP_PORT"]
    user = kwargs["AMQP_USER"]
    password = kwargs["AMQP_PASSWORD"]
    vhost = kwargs["AMQP_VHOST"]
    return f"amqp://{user}:{password}@{host}:{port}/{vhost}"