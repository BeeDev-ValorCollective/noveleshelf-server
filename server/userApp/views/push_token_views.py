from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from userApp.models import UserPushToken


class PushTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        platform = request.data.get('platform')

        if not token:
            return Response(
                {
                    'detail': 'Push token is required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if platform not in ['android', 'ios', None, '']:
            return Response(
                {
                    'detail': (
                        'Platform must be '
                        '"android" or "ios".'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # A token uniquely identifies a device/app
        # installation. If the same device was
        # previously associated with another user,
        # transfer it to the currently logged-in user.
        push_token, created = (
            UserPushToken.objects.update_or_create(
                token=token,
                defaults={
                    'user': request.user,
                    'platform': platform or None,
                    'is_active': True,
                }
            )
        )

        return Response(
            {
                'id': push_token.id,
                'token': push_token.token,
                'platform': push_token.platform,
                'is_active': push_token.is_active,
                'created': created,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )

    def delete(self, request):
        token = request.data.get('token')

        if not token:
            return Response(
                {
                    'detail': 'Push token is required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        push_token = (
            UserPushToken.objects
            .filter(
                user=request.user,
                token=token
            )
            .first()
        )

        if not push_token:
            return Response(
                {
                    'detail': 'Push token not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        push_token.is_active = False
        push_token.save(
            update_fields=[
                'is_active',
                'updated_at',
            ]
        )

        return Response(
            {
                'detail': (
                    'Push token deactivated.'
                )
            },
            status=status.HTTP_200_OK
        )