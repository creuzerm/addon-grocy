import pytest

def test_php_fpm_gtpl():
    with open("grocy/rootfs/etc/php82/templates/php-fpm.gtpl", "r") as f:
        content = f.read()

    assert "listen = /var/run/php82-fpm-{{ .name }}.sock" in content
    assert "listen.owner = root" in content
    assert "listen.group = root" in content
    assert "listen.mode = 0660" in content

def test_nginx_direct_gtpl():
    with open("grocy/rootfs/etc/nginx/templates/direct.gtpl", "r") as f:
        content = f.read()

    assert "fastcgi_pass unix:/var/run/php82-fpm-www.sock;" in content

def test_nginx_ingress_gtpl():
    with open("grocy/rootfs/etc/nginx/templates/ingress.gtpl", "r") as f:
        content = f.read()

    assert "fastcgi_pass unix:/var/run/php82-fpm-ingress.sock;" in content

def test_php_fpm_s6_run():
    with open("grocy/rootfs/etc/s6-overlay/s6-rc.d/init-php-fpm/run", "r") as f:
        content = f.read()

    # Check that port parameter is removed
    assert 'port "^9002"' not in content
    assert 'port "^9001"' not in content

def test_nginx_s6_run():
    with open("grocy/rootfs/etc/s6-overlay/s6-rc.d/nginx/run", "r") as f:
        content = f.read()

    # Check that we wait for sockets instead of bashio::net.wait_for 9002
    assert "bashio::net.wait_for 9002" not in content
    assert "while [ ! -S /var/run/php82-fpm-ingress.sock ]; do" in content
    assert "while [ ! -S /var/run/php82-fpm-www.sock ]; do" in content
