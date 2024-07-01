from urllib.parse import urlparse
from django.conf import settings

class TrackLastPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only store the referer if it's a GET request
        if request.method == 'GET' and 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
            if self.is_safe_url(referer, allowed_hosts={request.get_host()}):
                request.session['previous_page'] = referer

        return response

    def is_safe_url(self, url, allowed_hosts):
        """Return True if the url is a safe redirection."""
        parsed_url = urlparse(url)
        return (not parsed_url.netloc or parsed_url.netloc in allowed_hosts) and parsed_url.scheme in ('http', 'https')
