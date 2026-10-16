import os

INGRESS_GTPL_PATH = 'grocy/rootfs/etc/nginx/templates/ingress.gtpl'

def test_ingress_headers_forwarded():
    """Verify that X-Ingress-Path and Authorization headers are correctly forwarded."""
    assert os.path.exists(INGRESS_GTPL_PATH), f"File not found: {INGRESS_GTPL_PATH}"

    with open(INGRESS_GTPL_PATH, 'r') as f:
        content = f.read()

    assert 'fastcgi_param HTTP_X_INGRESS_PATH $http_x_ingress_path;' in content, "X-Ingress-Path header not forwarded"
    assert 'fastcgi_param HTTP_AUTHORIZATION $http_authorization;' in content, "Authorization header not forwarded"

def test_no_cookie_stripping():
    """Verify that there are no directives stripping user session cookies."""
    assert os.path.exists(INGRESS_GTPL_PATH), f"File not found: {INGRESS_GTPL_PATH}"

    with open(INGRESS_GTPL_PATH, 'r') as f:
        content = f.read()

    assert 'fastcgi_pass_request_headers off;' not in content, "Headers are stripped"
    assert 'fastcgi_hide_header Set-Cookie;' not in content, "Set-Cookie header is hidden/stripped"
