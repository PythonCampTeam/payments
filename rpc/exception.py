def handling(ecxeption):
    """Raises if the arguments InvalidRequestError
    """
    body = ecxeption.json_body
    err = body.get('error', {})
    error = "Status is: {}, message is: {}".format(ecxeption.http_status,
                                                   err.get('message'))
    return error
