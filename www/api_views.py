from .models import Item
from .serializers import ItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile, ItemAssignment
from .serializers import ProfileSerializer, ItemAssignmentSerializer
from rest_framework import status
from django.http import JsonResponse
from .tasks import send_email_task
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_details(request, item_id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = Profile.objects.get(owner=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_items(request):
    item_assignments = ItemAssignment.objects.filter(requestor=request.user, status='out')
    serializer = ItemAssignmentSerializer(item_assignments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def set_item_status(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.status = 'broken'
        item.save()
        subject = f"{item} Out of Order"
        message = f"Report: {item} is out of order\nLocation: {item.location}."
        recipient_list = [item.department.head.email]
        send_email_task.delay(subject, message, recipient_list)
        return JsonResponse({'success': True}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def change_profile_pic(request):
    user = request.user
    user.profile.profile_pic = request.FILES['profile_pic']
    user.profile.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def change_password(request):
    user = request.user
    form = PasswordChangeForm(user, request.data)

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
