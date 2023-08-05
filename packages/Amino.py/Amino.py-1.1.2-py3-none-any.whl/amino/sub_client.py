import json
import base64
import random

import requests
from time import timezone
from time import time as timestamp
from typing import BinaryIO

from . import client
from .lib.util import exceptions, headers, device, objects
from cryptography.fernet import Fernet
from string import hexdigits

device = device.DeviceGenerator()
headers.sid = client.Client().sid

class SubClient(client.Client):
    def __init__(self, comId: str, profile: str, devKey: str = None):
        client.Client.__init__(self)

        if not comId: raise exceptions.NoCommunity

        self.comId = comId
        self.devKey = devKey
        self.profile = self.get_user_info(userId=profile.userId)

    def post_blog(self, title: str, content: str, categoriesList: list = None, backgroundColor: str = None, images: list = None, fansOnly: bool = False):
        if images:
            images_list = []
            for item in images:
                content = content.replace(item.replace_key, f"[IMG={item.replace_key}]")
                images_list.append(item.media_list_item)

        else: images_list = None

        data = {
            "address": None,
            "content": content,
            "mediaList": images_list,
            "title": title,
            "extensions": {},
            "latitude": 0,
            "longitude": 0,
            "eventSource": "GlobalComposeMenu",
            "timestamp": int(timestamp() * 1000)
        }

        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/blog", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def post_wiki(self, title: str, content: str, icon: str = None, keywords: str = None, backgroundColor: str = None, images: list = None, fansOnly: bool = False):
        if images:
            images_list = []
            for item in images:
                content = content.replace(item.replace_key, f"[IMG={item.replace_key}]")
                images_list.append(item.media_list_item)

        data = {
            "label": title,
            "content": content,
            "eventSource": "GlobalComposeMenu",
            "timestamp": int(timestamp() * 1000)
        }

        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/item", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def edit_blog(self, blogId: str, title: str = None, body: str = None, categoriesList: list = None, backgroundColor: str = None, images: list = None, fansOnly: bool = False):
        if images:
            images_list = []
            for item in images:
                body = body.replace(item.replace_key, f"[IMG={item.replace_key}]")
                images_list.append(item.media_list_item)

        else: images_list = None

        data = {
            "address": None,
            "mediaList": images_list,
            "latitude": 0,
            "longitude": 0,
            "eventSource": "PostDetailView",
            "timestamp": int(timestamp() * 1000)
        }

        if title: data["title"] = title
        if body: data["content"] = body
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList
        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def delete_blog(self, blogId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/blog/{blogId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def repost_blog(self, blogId: str, content: str = None):
        """
        refObjectType: 1 is blog, 2 is favorite
        """
        data = json.dumps({
            "content": content,
            "refObjectId": blogId,
            "refObjectType": 1,
            "type": 2,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/blog", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def check_in(self, tz: str = -timezone // 1000):
        data = json.dumps({
            "timezone": tz,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/check-in", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def repair_check_in(self, method: int = 0):
        data = {"timestamp": int(timestamp() * 1000)}
        if method == 0: data["repairMethod"] = "1"  # Coins
        if method == 1: data["repairMethod"] = "2"  # Amino+

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/check-in/repair", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def lottery(self, tz: str = -timezone // 1000):
        data = json.dumps({
            "timezone": tz,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/check-in/lottery", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.lotteryLog(json.loads(response.text)["lotteryLog"]).lotteryLog

    def edit_profile(self, nickname: str = None, content: str = None, icon: str = None, chatRequestPrivilege: str = None, mediaList: list = None, backgroundImage: str = None, backgroundColor: str = None, titles: list = None):
        data = {"timestamp": int(timestamp() * 1000)}

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = icon
        if content: data["content"] = content
        if mediaList: data["mediaList"] = mediaList
        if chatRequestPrivilege: data["extensions"] = {"privilegeOfChatInviteRequest": chatRequestPrivilege}
        if backgroundImage: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if titles: data["extensions"] = {"customTitles": titles}

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.userId}", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def vote_poll(self, blogId: str, optionId: str):
        data = json.dumps({
            "value": 1,
            "eventSource": "PostDetailView",
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/poll/option/{optionId}/vote", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None, isGuest: bool = False):
        data = {
            "content": message,
            "stickerId": None,
            "type": 0,
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["respondTo"] = replyTo

        if isGuest: comType = "g-comment"
        else: comType = "comment"

        if userId:
            data["eventSource"] = "UserProfileView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/{comType}", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/{comType}", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/item/{wikiId}/{comType}", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        if userId: response = requests.delete(f"{self.api}/x{self.comId}/s/user-profile/{userId}/comment/{commentId}", headers=headers.Headers().headers)
        elif blogId: response = requests.delete(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}", headers=headers.Headers().headers)
        elif wikiId: response = requests.delete(f"{self.api}/x{self.comId}/s/item/{wikiId}/comment/{commentId}", headers=headers.Headers().headers)

        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def like_blog(self, blogId: str = None, blogIds: list = None, wikiId: str = None):
        data = {
            "value": 4,
            "timestamp": int(timestamp() * 1000)
        }

        if blogId:
            data["eventSource"] = "UserProfileView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/vote?cv=1.2", headers=headers.Headers(data=data).headers, data=data)

        elif blogIds:
            data["targetIdList"] = blogIds
            response = requests.post(f"{self.api}/x{self.comId}/s/feed/vote", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self. comId}/s/item/{wikiId}/vote?cv=1.2", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def unlike_blog(self, blogId: str = None, wikiId: str = None):
        if blogId: response = requests.delete(f"{self.api}/x{self.comId}/s/blog/{blogId}/vote?eventSource=UserProfileView", headers=headers.Headers().headers)
        elif wikiId: response = requests.delete(f"{self.api}/x{self.comId}/s/item/{wikiId}/vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType

        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None):
        data = {
            "value": 1,
            "timestamp": int(timestamp() * 1000)
        }

        if blogId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)
        elif userId:
            data["eventSource"] = "UserProfileView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)
        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def unlike_comment(self, blogId: str, commentId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def upvote_comment(self, blogId: str, commentId: str):
        data = json.dumps({
            "value": 1,
            "eventSource": "PostDetailView",
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def downvote_comment(self, blogId: str, commentId: str):
        data = json.dumps({
            "value": -1,
            "eventSource": "PostDetailView",
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=-1", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def unvote_comment(self, blogId: str, commentId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment/{commentId}/vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def reply_wall(self, userId: str, commentId: str, message: str):
        data = json.dumps({
            "content": message,
            "stackedId": None,
            "respondTo": commentId,
            "type": 0,
            "eventSource": "UserProfileView",
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/comment", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    # TODO : Fix stay online object, returning Invalid Request

    def send_active_obj(self):
        data = json.dumps({
            "userActiveTimeChunkList": [{
                "start": int(timestamp()),
                "end": int(timestamp()) + int(30)
            }],
            "optInAdsFlags": 2147483647,
            "timezone": -timezone // 1000
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/community/stats/user-active-time", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def activity_status(self, status: int):
        """
        :param int status: 1 is Online, 2 is Offline
        """
        data = json.dumps({
            "onlineStatus": status,
            "duration": 86400,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.userId}/online-status", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    # TODO : Finish this

    def watch_ad(self):
        response = requests.post(f"{self.api}/g/s/wallet/ads/video/start", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def check_notifications(self):
        response = requests.post(f"{self.api}/x{self.comId}/s/notification/checked", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def delete_notification(self, notificationId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/notification/{notificationId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def clear_notifications(self):
        response = requests.delete(f"{self.api}/x{self.comId}/s/notification", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def start_chat(self, userIds: list, message: str):
        data = json.dumps({
            "type": 0,
            "inviteeUids": userIds,
            "initialMessageContent": message,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def invite_to_chat(self, userIds: list, chatId: str):
        data = json.dumps({
            "uids": userIds,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/invite", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def add_to_favorites(self, userId: str):
        response = requests.post(f"{self.api}/x{self.comId}/s/user-group/quick-access/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def send_coins(self, coins: int, blogId: str = None, chatId: str = None, objectId: str = None, transactionId: str = None):
        transactionId2 = f"{''.join(random.sample([lst for lst in hexdigits[:-6]], 8))}-{''.join(random.sample([lst for lst in hexdigits[:-6]], 4))}-{''.join(random.sample([lst for lst in hexdigits[:-6]], 4))}-{''.join(random.sample([lst for lst in hexdigits[:-6]], 4))}-{''.join(random.sample([lst for lst in hexdigits[:-6]], 12))}"

        if transactionId:
            devReq = requests.get("https://pastebin.com/raw/adzikvR4").text.split("\r\n")
            if self.devKey is None: raise exceptions.DeveloperKeyRequired
            elif self.devKey.encode() == Fernet(devReq[0].encode()).decrypt(devReq[2].encode()): transactionId2 = transactionId
            else: raise exceptions.InvalidDeveloperKey

        data = {
            "coins": coins,
            "tippingContext": {"transactionId": transactionId2},
            "timestamp": int(timestamp() * 1000)
        }

        if chatId: response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/tipping", headers=headers.Headers(data=json.dumps(data)).headers, data=json.dumps(data))
        elif blogId: response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/tipping", headers=headers.Headers(data=json.dumps(data)).headers, data=json.dumps(data))
        elif objectId:
            data["objectId"] = objectId
            data["objectType"] = 2
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/tipping", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def thank_tip(self, chatId: str, userId: str):
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users/{userId}/thank", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def follow(self, userId: str = None, userIds: list = None):
        if userId: response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/member", headers=headers.Headers().headers)

        elif userIds:
            data = json.dumps({"targetUidList": userIds, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.id}/joined", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def unfollow(self, userId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/user-profile/{self.profile.userId}/joined/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def block(self, userId: str):
        response = requests.post(f"{self.api}/x{self.comId}/s/block/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def unblock(self, userId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/block/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def visit(self, userId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}?action=visit", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def flag(self, reason: str, flagType: int, userId: str = None, blogId: str = None, wikiId: str = None, asGuest: bool = False):
        data = {
            "flagType": flagType,
            "message": reason,
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["objectId"] = userId
            data["objectType"] = 0

        if blogId:
            data["objectId"] = blogId
            data["objectType"] = 1

        if wikiId:
            data["objectId"] = wikiId
            data["objectType"] = 2

        if asGuest: flg = "g-flag"
        else: flg = "flag"

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/{flg}", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def send_message(self, chatId: str, message: str = None, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None, clientRefId: int = int(timestamp() / 10 % 1000000000)):
        mentions = []

        if messageType or embedId or embedType or embedLink or embedTitle or embedContent or embedImage:
            devReq = requests.get("https://pastebin.com/raw/adzikvR4").text.split("\r\n")
            if self.devKey is None: raise exceptions.DeveloperKeyRequired
            elif self.devKey.encode() == Fernet(devReq[0].encode()).decrypt(devReq[2].encode()): pass
            else: raise exceptions.InvalidDeveloperKey

        if mentionUserIds:
            for mention_uid in mentionUserIds:
                mentions.append({"uid": mention_uid})

        if embedImage:
            embedImage = [[100, self.upload_media(embedImage), None]]

        data = {
            "type": messageType,
            "content": message,
            "clientRefId": clientRefId,
            "attachedObject": {
                "objectId": embedId,
                "objectType": embedType,
                "link": embedLink,
                "title": embedTitle,
                "content": embedContent,
                "mediaList": embedImage
            },
            "extensions": {"mentionedArray": mentions},
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["replyMessageId"] = replyTo

        if stickerId:
            data["content"] = None
            data["stickerId"] = stickerId
            data["type"] = 3

        if file:
            data["content"] = None
            if fileType == "audio":
                data["type"] = 2
                data["mediaType"] = 110

            elif fileType == "image":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/jpg"
                data["mediaUhqEnabled"] = True

            elif fileType == "gif":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/gif"
                data["mediaUhqEnabled"] = True

            else: raise exceptions.SpecifyType

            data["mediaUploadValue"] = base64.b64encode(file.read()).decode()

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None):
        data = {
            "adminOpName": 102,
            "adminOpNote": {"content": reason},
            "timestamp": int(timestamp() * 1000)
        }

        data = json.dumps(data)
        if not asStaff: response = requests.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}", headers=headers.Headers().headers)
        else: response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}/admin", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def mark_as_read(self, chatId: str, messageId: str):
        data = json.dumps({
            "messageId": messageId,
            "timestamp": int(timestamp() * 1000)
        })
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/mark-as-read", headers=headers.Headers().headers, data=data)

        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def edit_chat(self, chatId: str, doNotDisturb: bool = None, pinChat: bool = None, title: str = None, icon: str = None, backgroundImage: str = None, content: str = None, announcement: str = None, coHosts: list = None, keywords: list = None, pinAnnouncement: bool = None, publishToGlobal: bool = None, canTip: bool = None, viewOnly: bool = None, canInvite: bool = None, fansOnly: bool = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **title** : Title of the Chat.
            - **content** : Content of the Chat.
            - **icon** : Icon of the Chat.
            - **backgroundImage** : Url of the Background Image of the Chat.
            - **announcement** : Announcement of the Chat.
            - **pinAnnouncement** : If the Chat Announcement should Pinned or not.
            - **coHosts** : List of User IDS to be Co-Host.
            - **keywords** : List of Keywords of the Chat.
            - **viewOnly** : If the Chat should be on View Only or not.
            - **canTip** : If the Chat should be Tippable or not.
            - **canInvite** : If the Chat should be Invitable or not.
            - **fansOnly** : If the Chat should be Fans Only or not.
            - **publishToGlobal** : If the Chat should show on Public Chats or not.
            - **doNotDisturb** : If the Chat should Do Not Disturb or not.
            - **pinChat** : If the Chat should Pinned or not.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **1600** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **1613** (:meth:`UserNotJoined <amino.lib.util.exceptions.UserNotJoined>`) : Sorry, this user has not joined.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = {
            "type": 1,
            "timestamp": int(timestamp() * 1000)
        }

        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if announcement: data["extensions"] = {"announcement": announcement}
        if pinAnnouncement: data["extensions"] = {"pinAnnouncement": pinAnnouncement}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}

        if publishToGlobal: data["publishToGlobal"] = 0
        if not publishToGlobal: data["publishToGlobal"] = 1

        res = []

        if doNotDisturb:
            data = json.dumps({"alertOption": 2, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if not doNotDisturb:
            data = json.dumps({"alertOption": 1, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/alert", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if pinChat:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/pin", headers=headers.Headers().headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if not pinChat:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/unpin", headers=headers.Headers().headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if backgroundImage:
            data = json.dumps({"media": [100, backgroundImage, None], "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}/background", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if coHosts:
            data = json.dumps({"uidList": coHosts, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/co-host", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if not viewOnly:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/view-only/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if viewOnly:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/view-only/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if not canInvite:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/members-can-invite/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if canInvite:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/members-can-invite/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if not canTip:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/tipping-perm-status/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        if canTip:
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/tipping-perm-status/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
                else: res.append(response)

            else: res.append(response.status_code)

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService)
            elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied)
            elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists)
            elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined)
            else: res.append(response)

        else: res.append(response.status_code)

        return res

    def transfer_host(self, chatId: str, userIds: list):
        data = json.dumps({
            "uidList": userIds,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/transfer-organizer", headers=headers.Headers().headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def transfer_organizer(self, chatId: str, userIds: list):
        self.transfer_host(chatId, userIds)

    def kick(self, userId: str, chatId: str, allowRejoin: bool = True):
        if allowRejoin: allowRejoin = 1
        if not allowRejoin: allowRejoin = 0
        response = requests.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{userId}?allowRejoin={allowRejoin}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def join_chat(self, chatId: str):
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def leave_chat(self, chatId: str):
        response = requests.delete(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member/{self.profile.userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def subscribe(self, userId: str, autoRenew: str = False):
        lst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        data = json.dumps({
            "paymentContext": {
                "transactionId": f"{''.join(random.sample(lst, 8))}-{''.join(random.sample(lst, 4))}-{''.join(random.sample(lst, 4))}-{''.join(random.sample(lst, 4))}-{''.join(random.sample(lst, 12))}",
                "isAutoRenew": autoRenew
            },
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/influencer/{userId}/subscribe", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def promotion(self, noticeId: str, type: str = "accept"):
        response = requests.post(f"{self.api}/x{self.comId}/s/notice/{noticeId}/{type}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def vc_permission(self, chatId: str, permission: int):
        """Voice Chat Join Permissions
        1 - Open to Everyone
        2 - Approval Required
        3 - Invite Only
        """
        data = json.dumps({
            "vvChatJoinType": permission,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/vvchat-permission", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def get_vc_reputation_info(self, chatId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.vcReputation(json.loads(response.text)).vcReputation

    def claim_vc_reputation(self, chatId: str):
        response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/avchat-reputation", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.vcReputation(json.loads(response.text)).vcReputation

    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):
        if type == "recent": response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=recent&start={start}&size={size}", headers=headers.Headers().headers)
        elif type == "banned": response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=banned&start={start}&size={size}", headers=headers.Headers().headers)
        elif type == "featured": response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=featured&start={start}&size={size}", headers=headers.Headers().headers)
        elif type == "leaders": response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=leaders&start={start}&size={size}", headers=headers.Headers().headers)
        elif type == "curators": response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=curators&start={start}&size={size}", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileCountList(json.loads(response.text)).userProfileCountList

    def get_online_users(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/live-layer?topic=ndtopic:x{self.comId}:online-members&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileCountList(json.loads(response.text)).userProfileCountList

    def get_online_favorite_users(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-group/quick-access?type=online&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileCountList(json.loads(response.text)).userProfileCountList

    def get_user_info(self, userId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfile(json.loads(response.text)["userProfile"]).userProfile

    def get_user_following(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}/joined?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_user_followers(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}/member?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_user_visitors(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}/visitors?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.visitorsList(json.loads(response.text)).visitorsList

    def get_user_checkins(self, userId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/check-in/stats/{userId}?timezone={-timezone // 1000}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userCheckIns(json.loads(response.text)).userCheckIns

    def get_user_blogs(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/blog?type=user&q={userId}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.blogList(json.loads(response.text)["blogList"]).blogList

    def get_user_wikis(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.wikiList(json.loads(response.text)["itemList"]).wikiList

    def get_user_achievements(self, userId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}/achievements", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userAchievements(json.loads(response.text)["achievements"]).userAchievements

    def get_influencer_fans(self, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/influencer/{userId}/fans?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.influencerFans(json.loads(response.text)).influencerFans

    def get_blocked_users(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/block?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def search_users(self, nickname: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=name&q={nickname}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_saved_blogs(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/bookmark?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userSavedBlogs(json.loads(response.text)["bookmarkList"]).userSavedBlogs

    def get_leaderboard_info(self, type: str, start: int = 0, size: int = 25):
        if "24" in type or "hour" in type: response = requests.get(f"{self.api}/g/s-x{self.comId}/community/leaderboard?rankingType=1&start={start}&size={size}", headers=headers.Headers().headers)
        elif "7" in type or "day" in type: response = requests.get(f"{self.api}/g/s-x{self.comId}/community/leaderboard?rankingType=2&start={start}&size={size}", headers=headers.Headers().headers)
        elif "rep" in type: response = requests.get(f"{self.api}/g/s-x{self.comId}/community/leaderboard?rankingType=3&start={start}&size={size}", headers=headers.Headers().headers)
        elif "check" in type: response = requests.get(f"{self.api}/g/s-x{self.comId}/community/leaderboard?rankingType=4", headers=headers.Headers().headers)
        elif "quiz" in type: response = requests.get(f"{self.api}/g/s-x{self.comId}/community/leaderboard?rankingType=5&start={start}&size={size}", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_wiki_info(self, wikiId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/item/{wikiId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.getWikiInfo(json.loads(response.text)).getWikiInfo

    def get_recent_wiki_items(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/item?type=catalog-all&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.wikiList(json.loads(response.text)["itemList"]).wikiList

    def get_wiki_categories(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/item-category?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.wikiCategoryList(json.loads(response.text)["itemCategoryList"]).wikiCategoryList

    def get_wiki_category(self, categoryId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/item-category/{categoryId}?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.wikiCategory(json.loads(response.text)).wikiCategory

    def get_tipped_users(self, blogId: str = None, wikiId: str = None, chatId: str = None, start: int = 0, size: int = 25):
        if blogId: response = requests.get(f"{self.api}/x{self.comId}/s/blog/{blogId}/tipping/tipped-users-summary?start={start}&size={size}", headers=headers.Headers().headers)
        elif wikiId: response = requests.get(f"{self.api}/x{self.comId}/s/item/{wikiId}/tipping/tipped-users-summary?start={start}&size={size}", headers=headers.Headers().headers)
        elif chatId: response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/tipping/tipped-users-summary?start={start}&size={size}", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType
        if response.status_code != 200: return json.loads(response.text)
        return objects.tippedUsersSummary(json.loads(response.text)).tippedUsersSummary

    def get_chat_threads(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread?type=joined-me&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.threadList(json.loads(response.text)["threadList"]).threadList

    def get_public_chat_threads(self, type: str = "recommended", start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.threadList(json.loads(response.text)["threadList"]).threadList

    def get_chat_thread(self, chatId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.thread(json.loads(response.text)["thread"]).thread

    def get_chat_messages(self, chatId: str, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.messageList(json.loads(response.text)["messageList"]).messageList

    def get_message_info(self, chatId: str, messageId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/message/{messageId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.message(json.loads(response.text)["message"]).message

    def get_blog_info(self, blogId: str = None, wikiId: str = None):
        if blogId:
            response = requests.get(f"{self.api}/x{self.comId}/s/blog/{blogId}", headers=headers.Headers().headers)
            if response.status_code != 200: return json.loads(response.text)
            return objects.getBlogInfo(json.loads(response.text)).getBlogInfo

        elif wikiId:
            response = requests.get(f"{self.api}/x{self.comId}/s/item/{wikiId}", headers=headers.Headers().headers)
            if response.status_code != 200: return json.loads(response.text)
            return objects.getWikiInfo(json.loads(response.text)).getWikiInfo

        else: raise exceptions.SpecifyType

    def get_blog_comments(self, blogId: str = None, wikiId: str = None, sorting: str = "newest", start: int = 0, size: int = 25):
        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"

        if blogId: response = requests.get(f"{self.api}/x{self.comId}/s/blog/{blogId}/comment?sort={sorting}&start={start}&size={size}", headers=headers.Headers().headers)
        elif wikiId: response = requests.get(f"{self.api}/x{self.comId}/s/item/{wikiId}/comment?sort={sorting}&start={start}&size={size}", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType

        if response.status_code != 200: return json.loads(response.text)
        return objects.commentList(json.loads(response.text)["commentList"]).commentList

    def get_blog_categories(self, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/blog-category?size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.blogCategoryList(json.loads(response.text)["blogCategoryList"]).blogCategoryList

    def get_wall_comments(self, userId: str, sorting: str = "newest", start: int = 0, size: int = 25):
        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile/{userId}/comment?sort={sorting}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.commentList(json.loads(response.text)["commentList"]).commentList

    def get_recent_blogs(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/feed/blog-all?pagingType=t&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.blogList(json.loads(response.text)["blogList"]).blogList

    def get_chat_users(self, chatId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["memberList"]).userProfileList

    def get_notifications(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/notification?pagingType=t&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.notificationList(json.loads(response.text)["notificationList"]).notificationList

    # TODO : Get notice to finish this
    def get_notices(self, start: int = 0, size: int = 25):
        """
        :param start: Start of the List (Start: 0)
        :param size: Amount of Notices to Show
        :return: Notices List
        """
        response = requests.get(f"{self.api}/x{self.comId}/s/notice?type=usersV2&status=1&start={start}&size={size}", headers=headers.Headers().headers)
        response = json.loads(response.text)
        if response["api:statuscode"] == 0: return response["noticeList"]
        else: return response

    def get_sticker_pack_info(self, sticker_pack_id: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/sticker-collection/{sticker_pack_id}?includeStickers=true", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.stickerCollection(json.loads(response.text)["stickerCollection"]).stickerCollection

    # TODO : Finish this
    def get_store_chat_bubbles(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/store/items?sectionGroupId=chat-bubble&start={start}&size={size}", headers=headers.Headers().headers)
        response = json.loads(response.text)
        if response["api:statuscode"] == 0:
            del response["api:message"], response["api:statuscode"], response["api:duration"], response["api:timestamp"]
            return response
        else: return response

    # TODO : Finish this
    def get_store_stickers(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/store/items?sectionGroupId=sticker&start={start}&size={size}", headers=headers.Headers().headers)
        response = json.loads(response.text)
        if response["api:statuscode"] == 0:
            del response["api:message"], response["api:statuscode"], response["api:duration"], response["api:timestamp"]
            return response
        else: return response

    def get_community_stickers(self):
        response = requests.get(f"{self.api}/x{self.comId}/s/sticker-collection?type=community-shared", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.communityStickerCollection(json.loads(response.text)).communityStickerCollection

    def get_sticker_collection(self, collectionId: str):
        response = requests.get(f"{self.api}/x{self.comId}/s/sticker-collection/{collectionId}?includeStickers=true", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.stickerCollection(json.loads(response.text)["stickerCollection"]).stickerCollection

    #
    # MODERATION MENU
    #

    def moderation_history(self, userId: str = None, blogId: str = None, size: int = 25):
        if userId: response = requests.get(f"{self.api}/x{self.comId}/s/admin/operation?objectId={userId}&objectType=0&pagingType=t&size={size}", headers=headers.Headers().headers)
        elif blogId: response = requests.get(f"{self.api}/x{self.comId}/s/admin/operation?objectId={blogId}&objectType=1&pagingType=t&size={size}", headers=headers.Headers().headers)
        else: response = requests.get(f"{self.api}/x{self.comId}/s/admin/operation?pagingType=t&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.adminLogList(json.loads(response.text)["adminLogList"]).adminLogList

    def feature(self, time: int, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        if chatId:
            if time == 1: time = 3600
            if time == 1: time = 7200
            if time == 1: time = 10800

        else:
            if time == 1: time = 86400
            elif time == 2: time = 172800
            elif time == 3: time = 259200
            else: raise exceptions.SpecifyType

        data = {
            "adminOpName": 114,
            "adminOpValue": {
                "featuredDuration": time
            },
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["adminOpValue"] = {"featuredType": 4}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["adminOpValue"] = {"featuredType": 1}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["adminOpValue"] = {"featuredType": 1}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/item/{wikiId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif chatId:
            data["adminOpValue"] = {"featuredType": 5}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/admin", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def unfeature(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        data = {
            "adminOpName": 114,
            "adminOpValue": {},
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/item/{wikiId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif chatId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/admin", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def hide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            },
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["adminOpName"] = 18
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/item/{wikiId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/admin", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def unhide(self, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, reason: str = None):
        data = {
            "adminOpNote": {
                "content": reason
            },
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["adminOpName"] = 19
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/blog/{blogId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/item/{wikiId}/admin", headers=headers.Headers(data=data).headers, data=data)

        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            response = requests.post(f"{self.api}/x{self.comId}/s/chat/thread/{chatId}/admin", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def edit_titles(self, userId: str, titles: list, colors: list):
        tlt = []
        for titles in titles:
            for colors in colors:
                tlt.append({"title": titles, "color": colors})

        data = json.dumps({
            "adminOpName": 207,
            "adminOpValue": {
                "titles": tlt
            },
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/admin", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    # TODO : List all warning texts
    def warn(self, userId: str, reason: str = None):
        data = json.dumps({
            "uid": userId,
            "title": "Custom",
            "content": reason,
            "attachedObject": {
                "objectId": userId,
                "objectType": 0
            },
            "penaltyType": 0,
            "adminOpNote": {},
            "noticeType": 7,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/notice", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    # TODO : List all strike texts
    def strike(self, userId: str, time: int, title: str = None, reason: str = None):
        if time == 1: time = 86400
        elif time == 2: time = 10800
        elif time == 3: time = 21600
        elif time == 4: time = 43200
        elif time == 5: time = 86400
        else: raise exceptions.SpecifyType

        data = json.dumps({
            "uid": userId,
            "title": title,
            "content": reason,
            "attachedObject": {
                "objectId": userId,
                "objectType": 0
            },
            "penaltyType": 1,
            "penaltyValue": time,
            "adminOpNote": {},
            "noticeType": 4,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/notice", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def ban(self, userId: str, reason: str, banType: int = None):
        data = json.dumps({
            "reasonType": banType,
            "note": {
                "content": reason
            },
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/ban", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def unban(self, userId: str, reason: str):
        data = json.dumps({
            "note": {
                "content": reason
            },
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/unban", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def reorder_featured_users(self, userIds: list):
        data = json.dumps({
            "uidList": userIds,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/x{self.comId}/s/user-profile/featured/reorder", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code == 200: return response.status_code
        else: return json.loads(response.text)

    def get_banned_users(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=banned&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileCountList(json.loads(response.text)).userProfileCountList

    def get_hidden_blogs(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/feed/blog-disabled?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.blogList(json.loads(response.text)["blogList"]).blogList

    def get_featured_users(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{self.comId}/s/user-profile?type=featured&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileCountList(json.loads(response.text)).userProfileCountList
