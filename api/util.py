import traceback

def _json_exception(e: Exception, status_code=500):
    return {
        'error': 'internal server error',
        'debug': str(e),
        'type': type(e).__name__,
        'traceback': ''.join(traceback.format_tb(e.__traceback__)),
    }