import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from urllib.parse import quote

from currencyApp.views.reward_views import credit_quill_purchase
from currencyApp.models import QuillBundle, QuillPurchase
from currencyApp.serializers import QuillBundleSerializer

stripe.api_key = settings.STRIPE_RESTRICTED_KEY


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_quill_bundles(request):
    bundles = QuillBundle.objects.filter(is_active=True).order_by('sort_order', 'quills')
    return Response(QuillBundleSerializer(bundles, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quill_checkout(request):
    bundle_id = request.data.get('bundle_id')
    return_path = request.data.get('return_path', '')

    if not bundle_id:
        return Response({'error': 'bundle_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bundle = QuillBundle.objects.get(id=bundle_id, is_active=True)
    except QuillBundle.DoesNotExist:
        return Response({'error': 'Quill bundle not found or inactive'}, status=status.HTTP_404_NOT_FOUND)

    success_url = f'{settings.FRONTEND_URL}/purchase-complete?session_id={{CHECKOUT_SESSION_ID}}'
    if return_path:
        success_url += f'&return_path={quote(return_path)}'

    try:
        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': bundle.name},
                    'unit_amount': bundle.price_cents,
                },
                'quantity': 1,
                
            }],
            managed_payments={"enabled": False},
            metadata={
                'user_id': str(request.user.id),
                'quill_bundle_id': str(bundle.id),
            },
            success_url=success_url,
            cancel_url=f'{settings.FRONTEND_URL}/purchase-quills',
        )
    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    return Response({'checkout_url': session.url}, status=status.HTTP_201_CREATED)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({'error': 'Invalid payload or signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object'].to_dict()
        metadata = session.get('metadata', {}) or {}
        user_id = metadata.get('user_id')
        quill_bundle_id = metadata.get('quill_bundle_id')

        if user_id and quill_bundle_id:
            from userApp.models import User
            try:
                user = User.objects.get(id=user_id)
                result = credit_quill_purchase(
                    user=user,
                    quill_bundle_id=quill_bundle_id,
                    stripe_session_id=session['id'],
                    stripe_event_id=event['id'],
                    stripe_payment_intent_id=session.get('payment_intent', ''),
                    amount_paid_cents=session.get('amount_total', 0),
                    currency=session.get('currency', 'usd'),
                )
                if not result['success']:
                    print(f"Quill purchase credit failed for event {event['id']}: {result['error']}")
            except User.DoesNotExist:
                pass

    # Always acknowledge receipt -- even on our own internal failures,
    # so Stripe doesn't keep retrying an event we can never fulfill.
    return JsonResponse({'received': True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_quill_purchase_status(request):
    session_id = request.query_params.get('session_id')
    if not session_id:
        return Response({'error': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    purchase = QuillPurchase.objects.filter(
        stripe_checkout_session_id=session_id, user=request.user
    ).first()

    if purchase and purchase.status == 'completed':
        return Response({'completed': True})
    return Response({'completed': False})
