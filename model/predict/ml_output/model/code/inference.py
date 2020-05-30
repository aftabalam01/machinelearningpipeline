""" inference.py """
import base64
import json
import numpy


def input_handler(data, context):
    """ Pre-process request input before it is sent to TensorFlow Serving REST API
    Args:
        data (obj): the request data, in format of dict or string
        context (Context): an object containing request and configuration details
    Returns:
        (dict): a JSON-serializable dict that contains request body and headers
    """
    if context.request_content_type == 'application/x-image':
        payload = data.read()
        encoded_image = base64.b64encode(payload).decode('utf-8')
        instance = [{"b64": encoded_image}]
        return json.dumps({"instances": instance})
    elif context.request_content_type == 'application/x-npy':
        payload = numpy.load(data)
        encoded_image = base64.b64encode(payload).decode('utf-8')
        instance = [{"b64": encoded_image}]
        return json.dumps({"instances": instance})
    elif context.request_content_type == 'application/json':
        # pass through json (assumes it's correctly formed)
        d = data.read().decode('utf-8')
        return d if len(d) else ''
    elif context.request_content_type == 'text/csv':
        return json.dumps({
            'instances': [float(x) for x in data.read().decode('utf-8').split(',')]
        })
    else:
        _return_error(415, 'Unsupported content type "{}"'.format(context.request_content_type or 'Unknown'))


def output_handler(response, context):
    """Post-process TensorFlow Serving output before it is returned to the client.
    Args:
        data (obj): the TensorFlow serving response
        context (Context): an object containing request and configuration details
    Returns:
        (bytes, string): data to return to client, response content type
    """
    if response.status_code != 200:
        _return_error(response.status_code, response.content.decode('utf-8'))
    response_content_type = context.accept_header
    prediction = response.content
    return prediction


def _return_error(code, message):
    raise ValueError('Error: {}, {}'.format(str(code), message))