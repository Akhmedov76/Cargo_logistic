from api.chats.models import Chat


def get_or_create_chat(user1, user2):
    chat = Chat.objects.filter(participants=user1).filter(participants=user2).first()
    if chat:
        return chat
    chat = Chat.objects.create()
    chat.participants.set([user1, user2])
    return chat
