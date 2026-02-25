from flask import url_for


def add_pagination_to_response(response, route, pagination_object):
    """ Adding some pagination metadata to the response
    """
    if pagination_object.has_next:
        response['next'] = url_for(route, page=pagination_object.next_num)
    if pagination_object.has_prev:
        response['prev'] = url_for(route, page=pagination_object.prev_num)
    if pagination_object.pages:
        response['total_pages'] = pagination_object.pages
    if pagination_object.total:
        response['total_records'] = pagination_object.total
    return response
