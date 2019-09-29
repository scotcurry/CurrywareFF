from stats.models import OAuthInfo
from django.db.models import Count


def check_user_exists():
    total_record_count = OAuthInfo.objects.annotate(records=Count('xoauth_yahoo_guid'))
    total_records = total_record_count[0].records
    if total_records > 0:
        return True
    else:
        return False


def get_oauth_info():
    oauth_record = OAuthInfo.objects.all()
    return oauth_record[0]
