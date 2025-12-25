from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError


def get_client_ip(request):
    return (
        request.META.get("REMOTE_ADDR")
        or (
            request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            if request.META.get("HTTP_X_FORWARDED_FOR") else None
        ) or request.META.get("HTTP_CF_CONNECTING_IP")
        or request.META.get("HTTP_X_REAL_IP")
    )

def get_country_from_ip(ip):
    if not ip:
        return "Unknown"

    try:
        geoip = GeoIP2()
        country = geoip.country(ip)
        return country.get("country_name", "Unknown")
    except AddressNotFoundError:
        return "Unknown"
    except Exception:
        return "Unknown"