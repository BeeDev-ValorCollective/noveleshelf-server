import logging
from django.utils import timezone

logger = logging.getLogger('cron')


def deactivate_unverified_users():
    from userApp.models import User
    from cronApp.models import CronLog

    try:
        expired_users = User.objects.filter(
            is_verified=False,
            is_active=True,
            verification_grace_ends__lt=timezone.now()
        )

        count = expired_users.count()
        expired_users.update(is_active=False)

        message = f'Deactivated {count} unverified users past grace period'
        logger.info(message)
        print(message)

        CronLog.objects.create(
            job_name='deactivate_unverified_users',
            status='success',
            message=message,
            records_affected=count
        )

    except Exception as e:
        error_message = f'Error deactivating unverified users: {str(e)}'
        logger.error(error_message)
        print(error_message)

        CronLog.objects.create(
            job_name='deactivate_unverified_users',
            status='failure',
            message=error_message,
            records_affected=0
        )


def flush_expired_tokens():
    from django.core.management import call_command
    from cronApp.models import CronLog

    try:
        call_command('flushexpiredtokens')
        message = 'Expired tokens flushed successfully'
        logger.info(message)
        print(message)

        CronLog.objects.create(
            job_name='flush_expired_tokens',
            status='success',
            message=message,
            records_affected=0
        )

    except Exception as e:
        error_message = f'Error flushing expired tokens: {str(e)}'
        logger.error(error_message)
        print(error_message)

        CronLog.objects.create(
            job_name='flush_expired_tokens',
            status='failure',
            message=error_message,
            records_affected=0
        )