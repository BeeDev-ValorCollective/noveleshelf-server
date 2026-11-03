
import json
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from userApp.models import UserPushToken


logger = logging.getLogger(__name__)

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"
EXPO_BATCH_SIZE = 100


def send_expo_push_notifications(user_ids, title, body, data=None):
    """
    Send Expo push notifications to all active devices
    belonging to the specified users.

    Returns the number of messages accepted by Expo.
    Acceptance does not guarantee delivery to a device.
    """

    tokens = list(
        UserPushToken.objects
        .filter(
            user_id__in=user_ids,
            is_active=True,
        )
        .values_list("token", flat=True)
        .distinct()
    )

    if not tokens:
        logger.info(
            "No active push tokens found for notification: %s",
            title,
        )
        return 0

    messages = [
        {
            "to": token,
            "title": title,
            "body": body,
            "sound": "default",
            "channelId": "default",
            "data": data or {},
        }
        for token in tokens
    ]

    accepted_count = 0

    for start in range(0, len(messages), EXPO_BATCH_SIZE):
        batch = messages[start:start + EXPO_BATCH_SIZE]

        request = Request(
            EXPO_PUSH_URL,
            data=json.dumps(batch).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=10) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            tickets = result.get("data", [])

            if isinstance(tickets, dict):
                tickets = [tickets]

            for index, ticket in enumerate(tickets):
                if ticket.get("status") == "ok":
                    accepted_count += 1
                else:
                    details = ticket.get("details") or {}

                    logger.warning(
                        "Expo rejected push notification: %s",
                        ticket.get("message", "Unknown error"),
                    )

                    if details.get("error") == "DeviceNotRegistered":
                        UserPushToken.objects.filter(
                            token=batch[index]["to"]
                        ).update(is_active=False)

        except (HTTPError, URLError, TimeoutError, OSError) as error:
            logger.error(
                "Expo push request failed: %s",
                error,
            )

        except (ValueError, KeyError, TypeError) as error:
            logger.error(
                "Invalid Expo push response: %s",
                error,
            )

    logger.info(
        "Expo accepted %s of %s push messages.",
        accepted_count,
        len(messages),
    )

    return accepted_count
