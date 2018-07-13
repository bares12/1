# -*- coding: utf-8 -*-

from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from LineAPI.akad.ttypes import ChatRoomAnnouncementContents
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
from gtts import gTTS
from threading import Thread
from io import StringIO
from multiprocessing import Pool
from googletrans import Translator
from urllib.parse import urlencode
from wikiapi import WikiApi
import subprocess as cmd
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, wikipedia, urllib, urllib.parse, atexit, asyncio, traceback
_session = requests.session()
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    with open("token.txt","r") as tokens:
        token = tokens.read()
    print (str(token))
except Exception as e:
    print (str(e))
    
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
imagesOpen = codecs.open("image.json","r","utf-8")
stickersOpen = codecs.open("sticker.json","r","utf-8")

client = LINE()
#client = LINE("")
cl = client
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
clientMID = client.profile.mid
myBot = [clientMID]
loop = asyncio.get_event_loop()
botStart = time.time()
admin = [clientMID]
temp_flood = {}
groupName = {}
groupImage = {}

read = json.load(readOpen)
settings = json.load(settingsOpen)
images = json.load(imagesOpen)
stickers = json.load(stickersOpen)

settings["myProfile"]["displayName"] = clientProfile.displayName
settings["myProfile"]["statusMessage"] = clientProfile.statusMessage
settings["myProfile"]["pictureStatus"] = clientProfile.pictureStatus
cont = client.getContact(clientMID)
settings["myProfile"]["videoProfile"] = cont.videoProfile
coverId = client.getProfileDetail()["result"]["objectId"]
settings["myProfile"]["coverId"] = coverId

with open("/root/moeself/temp.json", "r", encoding="utf_8_sig") as f:
    anu = json.loads(f.read())
    anu.update(settings)
    settings = anu

## -*- Script Start -*- ##
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print ('Time process : {} seconds'.format(str(time2 - time1)))
        return ret
    return wrap

def autoRestart():
    if settings["autoRestart"] == True:
        if time.time() - botStart > int(settings["timeRestart"]):
            backupData()
            restartBot()

def logError(text):
    client.log("[ ERROR ] " + str(text))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = hasil + ", " + inihari.strftime('%d') + " - " + bln + " - " + inihari.strftime('%Y') + " | " + inihari.strftime('%H:%M:%S')
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

#message.createdTime -> 00:00:00
def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))

def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def load():
    global images
    global stickers
    with open("image.json","r") as fp:
        images = json.load(fp)
    with open("sticker.json","r") as fp:
        stickers = json.load(fp)

def sendSticker(to, version, packageId, stickerId):
    contentMetadata = {
        'STKVER': version,
        'STKPKGID': packageId,
        'STKID': stickerId
    }
    client.sendMessage(to, '', contentMetadata, 7)

def sendImage(to, path, name="image"):
    try:
        if settings["server"] == "VPS":
            client.sendImageWithURL(to, str(path))
    except Exception as error:
        logError(error)

def delExpire():
    if temp_flood != {}:
        for tmp in temp_flood:
            if temp_flood[tmp]["expire"] == True:
                if time.time() - temp_flood[tmp]["time"] >= 3*10:
                    temp_flood[tmp]["expire"] = False
                    temp_flood[tmp]["time"] = time.time()
                    try:
                        client.sendMessage(tmp, "Bot kembali aktif")
                    except Exception as error:
                        logError(error)

def sendMention(to, mid, firstmessage='', lastmessage=''):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        client.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)

def mentionSiders(to, firstmessage, lastmessage):
    try:
        mid = []
        if read["ROM"][to] == {} and read["readMember"] != {}:
            for ar in read["readMember"][to]:
                mid.append(ar)
        elif read["ROM"][to] == {} and read["readMember"][to] == {}:
            pass
        else:
            for ars in read["readMember"][to]:
                if ars not in read["ROM"][to]:
                    mid.append(ars)
        arrData = ""
        textx = str(firstmessage)
        arr = []
        if mid != []:
            for i in mid:
                textx += str("\n? ")
                mention = "@x "
                slen = str(len(textx))
                elen = str(len(textx) + len(mention) - 1)
                arrData = {'S':slen, 'E':elen, 'M':i}
                arr.append(arrData)
                textx += mention
            textx += str(lastmessage)
            client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
        else:
            textx += str(lastmessage)
            client.sendMessage(to, textx)
    except:
        try:
            ret_ = str(firstmessage)
            sider = {}
            sider["name"] = ""
            if read["ROM"][to] == {} and read["readMember"][to] != {}:
                for ar in read["readMember"][to]:
                    contact = client.getContact(ar)
                    sider["name"] += "\n? {}".format(str(contact.displayName))
            elif read["ROM"][to] == {} and read["readMember"][to] == {}:
                pass
            else:
                for ars in read["readMember"][to]:
                    if ars not in read["ROM"][to]:
                        contact = client.getContact(ars)
                        sider["name"] += "\n? {}".format(str(contact.displayName))
            ret_ += str(sider["name"])
            ret_ += str(lastmessage)
            client.sendMessage(to, str(ret_))
        except Exception as error:
            logError(error)

def mentionMembers(to, mid):
    try:
        group = client.getGroup(to)
        mids = [mem.mid for mem in group.members]
        jml = len(mids)
        arrData = ""
        if mid[0] == mids[0]:
            textx = "???[ Mention {} User ]\n".format(str(jml))
        else:
            textx = ""
        arr = []
        for i in mid:
            no = mids.index(i) + 1
            textx += "? {}. ".format(str(no))
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
        if no == jml:
            textx += "???[ Success ]"
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def userMentioned(to):
    try:
        mid = []
        for lu in settings["userMentioned"][to]:
            mid.append(lu)
        arrData = ""
        textx = "???[ List User ]\n".format(str(len(mid)))
        arr = []
        no = 0 + 1
        for i in mid:
            textx += "? {}. ".format(str(no))
            mention = "@x "
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
            textx += "#{}x\n".format(str(settings["userMentioned"][to][i]))
            no += 1
        textx += "???[ Total {} User ]".format(str(len(mid)))
        settings["userMentioned"][to] = {}
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)

def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = client.genOBSParams({'oid': clientMID, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        client.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile {}".format(str(e)))

def changeProfileVideo(to):
    if settings['changeProfileVideo']['picture'] == None:
        return client.sendMessage(to, "Foto tidak ditemukan")
    elif settings['changeProfileVideo']['video'] == None:
        return client.sendMessage(to, "Video tidak ditemukan")
    else:
        path = settings['changeProfileVideo']['video']
        files = {'file': open(path, 'rb')}
        obs_params = client.genOBSParams({'oid': client.getProfile().mid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return client.sendMessage(to, "Gagal update profile")
        path_p = settings['changeProfileVideo']['picture']
        settings['changeProfileVideo']['status'] = False
        client.updateProfilePicture(path_p, 'vp')

def cloneProfile(mid):
    contact = client.getContact(mid)
    if contact.videoProfile == None:
        client.cloneContactProfile(mid)
    else:
        profile = client.getProfile()
        profile.displayName, profile.statusMessage = contact.displayName, contact.statusMessage
        client.updateProfile(profile)
        pict = client.downloadFileURL('http://dl.profile.line-cdn.net/' + contact.pictureStatus, saveAs="tmp/pict.bin")
        vids = client.downloadFileURL( 'http://dl.profile.line-cdn.net/' + contact.pictureStatus + '/vp', saveAs="tmp/video.bin")
        changeVideoAndPictureProfile(pict, vids)
    coverId = client.getProfileDetail(mid)['result']['objectId']
    client.updateProfileCoverById(coverId)

def backupProfile():
    profile = client.getContact(clientMID)
    settings['myProfile']['displayName'] = profile.displayName
    settings['myProfile']['pictureStatus'] = profile.pictureStatus
    settings['myProfile']['statusMessage'] = profile.statusMessage
    settings['myProfile']['videoProfile'] = profile.videoProfile
    coverId = client.getProfileDetail()['result']['objectId']
    settings['myProfile']['coverId'] = str(coverId)

def restoreProfile():
    profile = client.getProfile()
    profile.displayName = settings['myProfile']['displayName']
    profile.statusMessage = settings['myProfile']['statusMessage']
    if settings['myProfile']['videoProfile'] == None:
        profile.pictureStatus = settings['myProfile']['pictureStatus']
        client.updateProfileAttribute(8, profile.pictureStatus)
        client.updateProfile(profile)
    else:
        client.updateProfile(profile)
        pict = client.downloadFileURL('http://dl.profile.line-cdn.net/' + settings['myProfile']['pictureStatus'], saveAs="tmp/pict.bin")
        vids = client.downloadFileURL( 'http://dl.profile.line-cdn.net/' + settings['myProfile']['pictureStatus'] + '/vp', saveAs="tmp/video.bin")
        changeVideoAndPictureProfile(pict, vids)
    coverId = settings['myProfile']['coverId']
    client.updateProfileCoverById(coverId)

def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weaks, days = divmod(days,7)
    if days == 0:
        return '%02d Jam %02d Menit %02d Detik' % (hours, mins, secs)
    elif days > 0 and weaks == 0:
        return '%02d Hari %02d Jam %02d Menit %02d Detik' %(days, hours, mins, secs)
    elif days > 0 and weaks > 0:
        return '%02d Minggu %02d Hari %02d Jam %02d Menit %02d Detik' %(weaks, days, hours, mins, secs)

def speedtest(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weaks, days = divmod(days,7)
    if days == 0:
        return '%02d' % (secs)
    elif days > 0 and weaks == 0:
        return '%02d' %(secs)
    elif days > 0 and weaks > 0:
        return '%02d' %(secs)

def a2():
    now2 = datetime.now()
    nowT = datetime.strftime(now2,"%M")
    if nowT[14:] in ["10","20","30","40","50","00"]:
        return False
    else:
        return True

def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd

def removeCmd(cmd, text):
	key = settings["keyCommand"]
	if settings["setKey"] == False: key = ''
	rmv = len(key + cmd) + 1
	return text[rmv:]

def myhelp():
    key = settings["keyCommand"]
    key = key.title()
    if settings['setKey'] == False: key = ''
    helpMessage = "???[ Help Message ]" + "\n" + \
                  "? Use?" + key + "?for the Prefix" + "\n" + \
                  "? " + key + "Myself" + "\n" + \
                  "? " + key + "Settings" + "\n" + \
                  "? " + key + "Media" + "\n" + \
                  "? " + key + "Group" + "\n" + \
                  "? " + key + "Memegen" + "\n" + \
                  "? " + key + "Translate" + "\n" + \
                  "? " + key + "TextSpeech" + "\n" + \
                  "???[ Status Command ]" + "\n" + \
                  "? " + key + "Speed" + "\n" + \
                  "? " + key + "Status" + "\n" + \
                  "? " + key + "About" + "\n" + \
                  "? " + key + "Runtime" + "\n" + \
                  "? " + key + "ErrorLog" + "\n" + \
                  "? " + key + "ResetLogError" + "\n" + \
                  "? " + key + "Restart" + "\n" + \
                  "???[ Key Command ]" + "\n" + \
                  "? " + key + "ChangeKey: ?new key?" + "\n" + \
                  "? MyKey" + "\n" + \
                  "? SetKey on/off" + "\n" + \
                  "? Mute" + "\n" + \
                  "? UnMute" + "\n" + \
                  "? Logoutz" + "\n" + \
                  "???[ Jangan Typo ]"
    return helpMessage

def helpsettings():
    key = settings["keyCommand"]
    key = key.title()
    if settings['setKey'] == False: key = ''
    helpSettings = "???[ Settings Command ]" + "\n" + \
                  "? " + key + "AutoAdd on/off" + "\n" + \
                  "? " + key + "AutoJoin on/off" + "\n" + \
                  "? " + key + "AutoRead on/off" + "\n" + \
                  "? " + key + "AutoReply on/off" + "\n" + \
                  "? " + key + "AutoLeave on/off" + "\n" + \
                  "? " + key + "AutoRestart on/off" + "\n" + \
                  "? " + key + "AutoJoinTicket on/off" + "\n" + \
                  "? " + key + "DetectMention on/off" + "\n" + \
                  "? " + key + "CheckContact on/off" + "\n" + \
                  "? " + key + "CheckPost on/off" + "\n" + \
                  "? " + key + "CheckSticker on/off" + "\n" + \
                  "? " + key + "ResponGroupCall on/off" + "\n" + \
                  "? " + key + "LeaveMessage on/off" + "\n" + \
                  "? " + key + "WelcomeMessage on/off" + "\n" + \
                  "? " + key + "GetReader on/off" + "\n" + \
                  "???[ Message Set Command ]" + "\n" + \
                  "? " + key + "AutoAdd" + "\n" + \
                  "? " + key + "AutoAddSticker" + "\n" + \
                  "? " + key + "DelAutoAddSticker" + "\n" + \
                  "? " + key + "SetAutoAdd: ?text?" + "\n" + \
                  "? " + key + "AutoReply" + "\n" + \
                  "? " + key + "AutoReplySticker" + "\n" + \
                  "? " + key + "DelAutoReplySticker" + "\n" + \
                  "? " + key + "SetAutoReply: ?text?" + "\n" + \
                  "? " + key + "DetectMention" + "\n" + \
                  "? " + key + "DetectMentionSticker" + "\n" + \
                  "? " + key + "DelDetectMentionSticker" + "\n" + \
                  "? " + key + "SetDetectMention: ?text?" + "\n" + \
                  "? " + key + "LeaveMessage" + "\n" + \
                  "? " + key + "LeaveSticker" + "\n" + \
                  "? " + key + "DelLeaveSticker" + "\n" + \
                  "? " + key + "SetLeaveMessage: ?text?" + "\n" + \
                  "? " + key + "WelcomeMessage" + "\n" + \
                  "? " + key + "WelcomeSticker" + "\n" + \
                  "? " + key + "DelWelcomeSticker" + "\n" + \
                  "? " + key + "SetWelcomeMessage: ?text?" + "\n" + \
                  "? " + key + "GetReader" + "\n" + \
                  "? " + key + "GetReaderSticker" + "\n" + \
                  "? " + key + "DelGetReaderSticker" + "\n" + \
                  "? " + key + "SetGetReaderMessage: ?text?" + "\n" + \
                  "???[ Jangan Typo ]"
    return helpSettings

def myself():
    key = settings["keyCommand"]
    key = key.title()
    if settings['setKey'] == False: key = ''
    mySelf =      "???[ MySelf Command ]" + "\n" + \
                  "? " + key + "Me" + "\n" + \
                  "? " + key + "Gift" + "\n" + \
                  "? " + key + "ChangeName: ?text?" + "\n" + \
                  "? " + key + "ChangeBio: ?text?" + "\n" + \
                  "? " + key + "MyProfile" + "\n" + \
                  "? " + key + "MyMid" + "\n" + \
                  "? " + key + "MyName" + "\n" + \
                  "? " + key + "MyBio" + "\n" + \
                  "? " + key + "MyPicture" + "\n" + \
                  "? " + key + "MyVideo" + "\n" + \
                  "? " + key + "MyCover" + "\n" + \
                  "? " + key + "GetMid ?mention?" + "\n" + \
                  "? " + key + "GetProfile ?mention?" + "\n" + \
                  "? " + key + "GetName ?mention?" + "\n" + \
                  "? " + key + "GetBio ?mention?" + "\n" + \
                  "? " + key + "GetPicture ?mention?" + "\n" + \
                  "? " + key + "GetVideo ?mention?" + "\n" + \
                  "? " + key + "GetCover ?mention?" + "\n" + \
                  "? " + key + "GetContact ?mention?" + "\n" + \
                  "? " + key + "CloneProfile ?mention?" + "\n" + \
                  "? " + key + "MidGetContact ?mid?" + "\n" + \
                  "? " + key + "MidClone ?mid?" + "\n" + \
                  "? " + key + "RestoreProfile" + "\n" + \
                  "? " + key + "BackupProfile" + "\n" + \
                  "???[ Mimic Command ]" + "\n" + \
                  "? " + key + "Mimic on/off" + "\n" + \
                  "? " + key + "MimicList" + "\n" + \
                  "? " + key + "MimicAdd ?mention?" + "\n" + \
                  "? " + key + "MimicDel ?mention?" + "\n" + \
                  "???[ Spesial Self Special Command ]" + "\n" + \
                  "? " + key + "AddImage ?name?" + "\n" + \
                  "? " + key + "ChangeImage ?name?" + "\n" + \
                  "? " + key + "DelImage ?name?" + "\n" + \
                  "? " + key + "SendImage ?number? ?name?" + "\n" + \
                  "? " + key + "ListImage" + "\n" + \
                  "? " + key + "AddSticker ?name?" + "\n" + \
                  "? " + key + "ChangeSticker ?name?" + "\n" + \
                  "? " + key + "DelSticker ?name?" + "\n" + \
                  "? " + key + "SendSticker ?number? ?name?" + "\n" + \
                  "? " + key + "ListSticker" + "\n" + \
                  "???[ Spesial Self Command ]" + "\n" + \
                  "? " + key + "Leave" + "\n" + \
                  "? " + key + "Siapa Yang Tag" + "\n" + \
                  "? " + key + "RemoveAllChat" + "\n" + \
                  "? " + key + "ChangeProfilePicture" + "\n" + \
                  "? " + key + "ChangeGroupPicture" + "\n" + \
                  "? " + key + "ChangeVideoProfile" + "\n" + \
                  "? " + key + "Abort" + "\n" + \
                  "? " + key + "CreateAnnounce ?text?|?link?" + "\n" + \
                  "? " + key + "Abroadcast ?text?|?link?" + "\n" + \
                  "? " + key + "Gbroadcast ?text?" + "\n" + \
                  "? " + key + "Fbroadcast ?text?" + "\n" + \
                  "? " + key + "AllBroadcast ?text?" + "\n" + \
                  "? " + key + "SpamTag ?number? ?mention?" + "\n" + \
                  "? " + key + "Spam ?number? ?on/off? ?text?" + "\n" + \
                  "???[ Kicker Command ]" + "\n" + \
                  "? " + key + "Crash" + "\n" + \
                  "? " + key + "Kick ?mention?" + "\n" + \
                  "???[ Jangan Typo ]"
    return mySelf

def mymedia():
    key = settings["keyCommand"]
    key = key.title()
    if settings['setKey'] == False: key = ''
    myMedia =     "???[ Media Command ]" + "\n" + \
                  "? " + key + "1cak" + "\n" + \
                  "? " + key + "Kalender" + "\n" + \
                  "? " + key + "Quotes" + "\n" + \
                  "? " + key + "TopNews" + "\n" + \
                  "? " + key + "Asking ?query?" + "\n" + \
                  "? " + key + "Anime ?query?" + "\n" + \
                  "? " + key + "IdLine ?userid?" + "\n" + \
                  "? " + key + "Quran ?search?" + "\n" + \
                  "? " + key + "Wikipedia ?search?" + "\n" + \
                  "? " + key + "Lyric ?song?" + "\n" + \
                  "? " + key + "Music ?song?" + "\n" + \
                  "? " + key + "MusicSearch ?search?" + "\n" + \
                  "? " + key + "ImageSearch ?search?" + "\n" + \
                  "? " + key + "YoutubeSearch ?search?" + "\n" + \
                  "? " + key + "YoutubeMp3 ?link?" + "\n" + \
                  "? " + key + "YoutubeMp4 ?link?" + "\n" + \
                  "? " + key + "YoutubeDownload ?link?" + "\n" + \
                  "? " + key + "YoutubeInfo ?link?" + "\n" + \
                  "? " + key + "GithubProfile ?username?" + "\n" + \
                  "? " + key + "ProfileIg ?username?" + "\n" + \
                  "? " + key + "PostIg ?username?" + "\n" + \
                  "? " + key + "StoryIg ?username?" + "\n" + \
                  "? " + key + "PictureIg ?link?" + "\n" + \
                  "? " + key + "VideoIg ?link?" + "\n" + \
                  "? " + key + "CheckIp ?ip?" + "\n" + \
                  "? " + key + "CheckDate ?date of birth?" + "\n" + \
                  "? " + key + "CheckTimezone ?location?" + "\n" + \
                  "? " + key + "CheckPraytime ?location?" + "\n" + \
                  "? " + key + "CheckWeather ?location?" + "\n" + \
                  "? " + key + "CheckLocation ?location?" + "\n" + \
                  "? " + key + "CheckWebsite ?link?|fp=T/F" + "\n" + \
                  "? " + key + "CheckImage ?link?" + "\n" + \
                  "? " + key + "CheckGif ?link?" + "\n" + \
                  "? " + key + "CheckVideo ?link?" + "\n" + \
                  "? " + key + "CheckAudio ?link?" + "\n" + \
                  "? " + key + "SearchMovie ?query?" + "\n" + \
                  "? " + key + "SearchMovie2 ?query?" + "\n" + \
                  "? " + key + "SearchAnime ?query?" + "\n" + \
                  "? " + key + "SearchManga ?query?" + "\n" + \
                  "? " + key + "SearchCharacter ?query?" + "\n" + \
                  "? " + key + "SearchPorn ?query?" + "\n" + \
                  "? " + key + "Suggestion ?query?" + "\n" + \
                  "? " + key + "Deviantart ?search?" + "\n" + \
                  "? " + key + "ImageText ?text?" + "\n" + \
                  "? " + key + "DirectSolidFiles ?link?" + "\n" + \
                  "? " + key + "ShortURL ?link?" + "\n" + \
                  "???[ Jangan Typo ]"
    return myMedia

def myinfo():
    key = settings["keyCommand"]
    key = key.title()
    if settings['setKey'] == False: key = ''
    myInfo =      "???[ Group Command ]" + "\n" + \
                  "? " + key + "GroupInfo" + "\n" + \
                  "? " + key + "GroupName" + "\n" + \
                  "? " + key + "GroupCreator" + "\n" + \
                  "? " + key + "GroupPicture" + "\n" + \
                  "? " + key + "GroupId" + "\n" + \
                  "? " + key + "GroupTicket" + "\n" + \
                  "? " + key + "OpenQR" + "\n" + \
                  "? " + key + "CloseQR" + "\n" + \
                  "? " + key + "ChangeGroupName: ?text?" + "\n" + \
                  "? " + key + "RejectAll" + "\n" + \
                  "? " + key + "CancelAll" + "\n" + \
                  "? " + key + "GroupList" + "\n" + \
                  "? " + key + "GroupInfo ?number?" + "\n" + \
                  "? " + key + "ListPending" + "\n" + \
                  "? " + key + "PendingList?number?" + "\n" + \
                  "? " + key + "ListMember" + "\n" + \
                  "? " + key + "MemberList ?number?" + "\n" + \
                  "? " + key + "Friendlist" + "\n" + \
                  "? " + key + "Friendinfo ?number?" + "\n" + \
                  "? " + key + "Blocklist" + "\n" + \
                  "???[ Special Group Command ]" + "\n" + \
                  "? " + key + "GetAnnounce" + "\n" + \
                  "? " + key + "Locate ?mention?" + "\n" + \
                  "? " + key + "Lurking reset" + "\n" + \
                  "? " + key + "Lurking" + "\n" + \
                  "? " + key + "LockGroupQR" + "\n" + \
                  "? " + key + "UnlockGroupQR" + "\n" + \
                  "? " + key + "LockGroupName" + "\n" + \
                  "? " + key + "UnlockGroupName" + "\n" + \
                  "? " + key + "BackupGroupName" + "\n" + \
                  "? " + key + "Mention" + "\n" + \
                  "? " + key + "MentionMid ?text?" + "\n" + \
                  "? " + key + "MentionContact" + "\n" + \
                  "? " + key + "InviteGroupCall ?number?" + "\n" + \
                  "? " + key + "InviteGroupVideoCall ?number?" + "\n" + \
                  "???[ Jangan Typo ]"
    return myInfo

def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = stickers
        f = codecs.open('sticker.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = images
        f = codecs.open('image.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False

async def clientBot(op):
    try:
        if settings["restartPoint"] != None:
            client.sendMessage(settings["restartPoint"], "Bot kembali aktif")
            settings["restartPoint"] = None

        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"]:
                client.findAndAddContactsByMid(op.param1)
            msgSticker = settings["messageSticker"]["listSticker"]["addSticker"]
            if msgSticker != None:
                sid = msgSticker["STKID"]
                spkg = msgSticker["STKPKGID"]
                sver = msgSticker["STKVER"]
                sendSticker(op.param1, sver, spkg, sid)
            if "@!" in settings["addPesan"]:
                msg = settings["addPesan"].split("@!")
                return sendMention(op.param1, op.param1, msg[0], msg[1])
            sendMention(op.param1, op.param1, "Halo", ", {}".format(str(settings['addPesan'])))
            arg = "   New Friend : {}".format(str(client.getContact(op.param1).displayName))
            print (arg)

        if op.type == 11:
            print ("[ 11 ] NOTIFIED UPDATE GROUP")
            if op.param3 == "1" and settings["protectGroupName"] == True and op.param2 not in myBot:
                if op.param1 in groupName:
                    G = client.getGroup(op.param1)
                    G.name = groupName[op.param1]
                    client.updateGroup(G)
                    client.sendMessage(op.param1,"Nama groupnya jangan di ubah-ubah -_-")
            if op.param3 == "4" and settings["protectGroupQr"] == True and op.param2 not in myBot:
                group = client.getGroup(op.param1)
                group.preventedJoinByTicket = True
                contact = client.getContact(op.param2)
                client.updateGroup(group)
                client.sendMessage(op.param1,"Jangan mainin qr -_-")

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
            group = client.getGroup(op.param1)
            contact = client.getContact(op.param2)
            if settings["autoJoin"] and clientMID in op.param3:
                client.acceptGroupInvitation(op.param1)
                sendMention(op.param1, op.param2, "Halo", ", makasih sudah invite saya")

        if op.type == 15:
            print ("[ 15 ]  NOTIFIED LEAVE GROUP")
            if settings["leaveMessage"] == True:
                if "{gname}" in settings['leavePesan']:
                    gName = client.getGroup(op.param1).name
                    msg = settings['leavePesan'].replace("{gname}", gName)
                    msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                    if msgSticker != None:
                        sid = msgSticker["STKID"]
                        spkg = msgSticker["STKPKGID"]
                        sver = msgSticker["STKVER"]
                        sendSticker(op.param2, sver, spkg, sid)
                    if "@!" in settings['leavePesan']:
                        msg = msg.split("@!")
                        return sendMention(op.param2, op.param2, msg[0], msg[1])
                    return sendMention(op.param2, op.param2, "Halo ", msg)
                msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                sendMention(op.param1, op.param2, "", ", {}".format(str(settings['leavePesan'])))

        if op.type == 17:
            print ("[ 17 ]  NOTIFIED ACCEPT GROUP INVITATION")
            if settings["welcomeMessage"] == True:
                group = client.getGroup(op.param1)
                contact = client.getContact(op.param2)
                msgSticker = settings["messageSticker"]["listSticker"]["welcomeSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                if "{gname}" in settings['welcomePesan'].lower():
                    gName = group.name
                    msg = settings['welcomePesan'].replace("{gname}", gName)
                    if "@!" in msg:
                        msg = msg.split("@!")
                        return sendMention(op.param1, op.param2, msg[0], msg[1])
                    sendMention(op.param1, op.param2, "Halo", msg)
                else:
                    sendMention(op.param1, op.param2, "Halo", ", {}".format(str(settings['welcomePesan'])))
                arg = "   Group Name : {}".format(str(group.name))
                arg += "\n   User Join : {}".format(str(contact.displayName))
                print (arg)

        if op.type == 19:
            print ("[ 19 ] NOTIFIED KICKOUT FROM GROUP")
            group = client.getGroup(op.param1)
            contact = client.getContact(op.param2)
            victim = client.getContact(op.param3)
            arg = "   Group Name : {}".format(str(group.name))
            arg += "\n   Executor : {}".format(str(contact.displayName))
            arg += "\n   Victim : {}".format(str(victim.displayName))
            print (arg)

        if op.type == 22:
            print ("[ 22 ] NOTIFIED INVITE INTO ROOM")
            if settings["autoLeave"] == True:
                client.sendMessage(op.param1, "Goblok ngapain invite gw")
                client.leaveRoom(op.param1)

        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                client.sendMessage(op.param1, "Goblok ngapain invite gw")
                client.leaveRoom(op.param1)

        if op.type in [25, 26]:
            if op.type == 25: print ("[ 25 ] SEND MESSAGE")
            else: print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = str(msg.text)
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            cmd = command(text)
            isValid = True
            setKey = settings["keyCommand"].title()
            if settings["setKey"] == False: setKey = ''
            if isValid != False:
                if msg.toType == 0 and sender != clientMID: to = sender
                else: to = receiver
                if receiver in temp_flood:
                    if temp_flood[receiver]["expire"] == True:
                        if cmd == "open" and sender == clientMID:
                            temp_flood[receiver]["expire"] = False
                            temp_flood[receiver]["time"] = time.time()
                            client.sendMessage(to, "Bot kembali aktif")
                        return
                    elif time.time() - temp_flood[receiver]["time"] <= 5:
                        temp_flood[receiver]["flood"] += 1
                        if temp_flood[receiver]["flood"] >= 20:
                            temp_flood[receiver]["flood"] = 0
                            temp_flood[receiver]["expire"] = True
                            ret_ = "Spam terdeteksi, Bot akan silent selama 30 detik pada ruangan ini atau ketik {}Open untuk mengaktifkan kembali.".format(setKey)
                            client.sendMessage(to, str(ret_))
                    else:
                         temp_flood[receiver]["flood"] = 0
                         temp_flood[receiver]["time"] = time.time()
                else:
                    temp_flood[receiver] = {
    	                "time": time.time(),
    	                "flood": 0,
    	                "expire": False
                    }
                if msg.toType == 0 and settings["autoReply"] and sender != clientMID:
                    contact = client.getContact(sender)
                    rjct = ["auto", "ngetag"]
                    validating = [a for a in rjct if a.lower() in text.lower()]
                    if validating != []: return
                    if contact.attributes != 32:
                        msgSticker = settings["messageSticker"]["listSticker"]["replySticker"]
                        if msgSticker != None:
                            sid = msgSticker["STKID"]
                            spkg = msgSticker["STKPKGID"]
                            sver = msgSticker["STKVER"]
                            sendSticker(to, sver, spkg, sid)
                        if "@!" in settings["replyPesan"]:
                            msg_ = settings["replyPesan"].split("@!")
                            sendMention(to, sender, "[ Auto Reply ]\n" + msg_[0], msg_[1])
                        sendMention(to, sender, "[ Auto Reply ]\nHalo", settings["replyPesan"])
                if msg.contentType == 0 and sender not in clientMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        gInfo = client.getGroup(receiver)
                        members = gInfo.members
                        if len(members) == len(mentionees): return
                        elif "list user" in text.lower(): return
                        elif len(mentionees) >= 50: return
                        for mention in mentionees:
                            if clientMID in mention["M"]:
                                rjct = ["auto", "ngetag"]
                                validating = [a for a in rjct if a.lower() in text.lower()]
                                if validating != []: return
                                if to not in settings["userMentioned"]:
                                    settings["userMentioned"][to] = {}
                                if sender not in settings["userMentioned"][to]:
                                    settings["userMentioned"][to][sender] = 1
                                else:
                                    settings["userMentioned"][to][sender] = settings["userMentioned"][to][sender] + 1
                                if settings["detectMention"] == True:
                                    msgSticker = settings["messageSticker"]["listSticker"]["mentionSticker"]
                                    if msgSticker != None:
                                        sid = msgSticker["STKID"]
                                        spkg = msgSticker["STKPKGID"]
                                        sver = msgSticker["STKVER"]
                                        sendSticker(to, sver, spkg, sid)
                                    if "@!" in settings["mentionPesan"]:
                                        msg_ = settings["mentionPesan"].split("@!")
                                        return sendMention(to, sender, "[ Auto Respond ]\n" + msg_[0], msg_[1])
                                    sendMention(receiver, sender, "[ Auto Respond ]\nOi", "{}".format(str(settings['mentionPesan'])))
                                break
                if msg.contentType == 6:
                    if settings["responGc"] == True and sender != clientMID:
                        contact = client.getContact(sender)
                        if msg.toType == 0:
                            if msg.contentMetadata["GC_EVT_TYPE"] == "I":
                                sendMention(to, sender, "Oit asw",", kalau mau telponan di pc aja gosah telponan group banyak yang nguping")
                                arg = "   Info : Invited Group Call"
                                arg += "\n   Executor : {}".format(str(contact.displayName))
                                print (arg)
                        elif msg.toType == 2:
                            group = client.getGroup(to)
                            if msg.contentMetadata["GC_EVT_TYPE"] == "S":
                                arg = "   Info : Started Group Call"
                                arg += "\n   Group Name : {}".format(str(group.name))
                                arg += "\n   Executor : {}".format(str(contact.displayName))
                                print (arg)
                                sendMention(to, sender, "-_-", ", gosah nyalain fcg kalo gak ada yang masuk u kek jones ae")
                            elif msg.contentMetadata["GC_EVT_TYPE"] == "E":
                                sendMention(to, sender, "Nah gitu kek", ", sekarang kan jadi tenang ini group")
                                arg = "   Info : Ended Group Call"
                                arg += "\n   Group Name : {}".format(str(group.name))
                                arg += "\n   Executor : {}".format(str(contact.displayName))
                                print (arg)
                elif msg.contentType == 13:
                    try:
                        client.getContact(msg.contentMetadata["mid"])
                    except:
                        client.removeMessage(msg_id)
                        client.sendMessage(to, "Gak mempan :v")
                        print ("Crash contact detected...")
                        return
                if msg.contentType == 0:
                    if settings["autoRead"] == True:
                        client.sendChatChecked(to, msg_id)
                    if to in read["readPoint"]:
                        if sender not in read["ROM"][to] and sender not in clientMID:
                            read["ROM"][to][sender] = True
                    if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                        client.sendMessage(to,text)
                    if text.lower() == "restarttz" and sender == "udd76b08e9178df926daf94371e9015f1":
                        try:
                            client.sendMessage(to, "Mencoba restart...")
                            client.sendMessage(to, "Mohon tunggu beberapa saat...")
                        except: pass
                        settings["restartPoint"] = to
                        restartBot()
                    if settings["publicMode"] == False and sender != clientMID:
                    	return
                    if to not in settings["botMute"] and to not in settings["botOff"]:
                        if cmd == "logoutz" and sender == clientMID:
                            client.sendMessage(to, "See you >_<")
                            sys.exit("Logout")
                        if cmd == "help":
                            helpMessage = myhelp()
                            client.sendMessage(to, str(helpMessage))
                        if cmd == "settings":
                            helpSettings = helpsettings()
                            client.sendMessage(to, str(helpSettings))
                        if cmd == "myself":
                            mySelf = myself()
                            client.sendMessage(to, str(mySelf))
                        if cmd == "media":
                            myMedia = mymedia()
                            client.sendMessage(to, str(myMedia))
                        if cmd == "group":
                            myInfo = myinfo()
                            client.sendMessage(to, str(myInfo))
                        if cmd == "translate":
                            ret_ = "[ Help Translate ]"
                            ret_ += "\nHow to use ?"
                            ret_ += "\nUse command :\n{}tr *lang* *text*".format(setKey)
                            ret_ += "\n\nExample :"
                            ret_ += "\n{}tr id rifky cool".format(setKey)
                            ret_ += "\n\nHow to find language?"
                            ret_ += "\nUse command :\n{}tr language".format(setKey)
                            client.sendMessage(msg.to,str(ret_))
                        if cmd == "textspeech":
                            ret_ = "[ Help Text To Speech ]"
                            ret_ += "\nHow to use ?"
                            ret_ += "\nUse command :\n{}say *lang* *text*".format(setKey)
                            ret_ += "\n\nExample :"
                            ret_ += "\n{}say id rifky ganteng".format(setKey)
                            ret_ += "\n\nHow to find language?"
                            ret_ += "\nUse command :\n{}say language".format(setKey)
                            client.sendMessage(msg.to,str(ret_))
                        if cmd == "memegen":
                            ret_ = "[ Help MemeGen ]"
                            ret_ += "\nHow to use ?"
                            ret_ += "\nUse command :\n{}creatememe *text*|*text*|*template*".format(setKey)
                            ret_ += "\n\nExample :"
                            ret_ += "\n{}creatememe rifky|ganteng|buzz".format(setKey)
                            ret_ += "\n\nHow to find template?"
                            ret_ += "\nUse command :\n{}template memegen".format(setKey)
                            client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("changekey: ") and sender == clientMID:
                            key = removeCmd("changekey:", text)
                            settings["keyCommand"] = str(key).lower()
                            client.sendMessage(to, "Changed to : [{}]".format(str(key).lower()))
                        elif cmd == "speed":
                            start = time.time()
                            client.sendMessage(to, "Menghitung kecepatan...")
                            elapsed_time = time.time() - start
                            client.sendMessage(to, "[ Speed ]\nKecepatan mengirim pesan {} detik".format(str(elapsed_time)))
                        elif cmd == "speedtest":
                            start = time.time()
                            client.sendMessage(to, "Start speedtest...")
                            speed = time.time() - start
                            ping = speed * 1000
                            client.sendMessage(to, "The result is {}Ms !".format(str(speedtest(ping))))
                        elif cmd == "crash" and sender == clientMID:
                            client.sendContact(to, "ub621484bd88d2486744123db00551d5e',")
                        elif cmd == "leave":
                            if msg.toType == 2:
                                client.sendMessage(to, "Selamat Tinggal :D")
                                client.leaveGroup(to)
                        elif cmd == "removeallchat" and sender == clientMID:
                            client.removeAllMessages(op.param2)
                            client.sendMessage(to, "Berhasil menghapus semua chat")
                        elif cmd == "restart" and sender == clientMID:
                            try:
                                client.sendMessage(to, "Mencoba restart...")
                                client.sendMessage(to, "Mohon tunggu beberapa saat...")
                            except: pass
                            settings["restartPoint"] = to
                            restartBot()
                        elif cmd == "runtime":
                            timeNow = time.time()
                            runtime = timeNow - botStart
                            runtime = format_timespan(runtime)
                            client.sendMessage(to, "Bot already running on {}".format(str(runtime)))
                        elif cmd == "errorlog":
                            with open('errorLog.txt', 'r') as fp:
                                isi = fp.read()
                            client.sendMessage(to, str(isi))
                        elif cmd == "resetlogerror":
                           with open("errorLog.txt","w") as fp:
                               fp.write("")
                           client.sendMessage(to,"Berhasil reset log error")
                        elif cmd.startswith("kick ") and sender == clientMID:
                           targets = []
                           key = eval(msg.contentMetadata["MENTION"])
                           key["MENTIONEES"] [0] ["M"]
                           for x in key["MENTIONEES"]:
                               targets.append(x["M"])
                           for target in targets:
                               try:
                                   client.kickoutFromGroup(to,[target])
                                   #time.sleep(1)
                               except Exception as e:
                                   client.sendMessage(to, str(e))
                        elif cmd.startswith("mentionmid "):
                            contact = removeCmd("mentionmid", text)
                            sendMention(to, contact)
                        elif cmd == "mentioncontact":
                            if msg.toType == 0:
                                sendMention(to, to)
                                client.sendContact(to, to)
                        elif cmd == "me":
                            contact = client.getContact(clientMID)
                            image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            name = contact.displayName
                            client.sendMessage(to, contentMetadata={'countryCode': 'ID', 'i-installUrl': 'line://ti/p/~moepoi', 'a-packageName': 'com.spotify.music', 'linkUri': 'line://ti/p/~moepoi', 'subText': 'Just Newbie :v', 'a-installUrl': 'line://ti/p/~moepoi', 'type': 'mt', 'previewUrl': image, 'a-linkUri': 'line://ti/p/~moepoi', 'text': name, 'id': 'mt000000000a6b79f9', 'i-linkUri': 'line://ti/p/~moepoi'}, contentType=19)
                        elif cmd == "mymid":
                            h = client.getContact(clientMID)
                            client.sendMessage(msg.to,"[ Mid User ]\n" + h.mid)
                        elif cmd == "myprofile":
                            contact = client.getContact(clientMID)
                            cu = client.getProfileCoverURL(clientMID)
                            path = str(cu)
                            image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            client.sendMessage(msg.to,"Nama :\n" + contact.displayName + "\n\nBio :\n" + contact.statusMessage)
                            client.sendImageWithURL(msg.to,image)
                            client.sendImageWithURL(msg.to,path)
                        elif cmd == "myname":
                            h = client.getContact(clientMID)
                            client.sendMessage(msg.to,"???[ Name ]\n" + "? " + h.displayName)
                        elif cmd == "mybio":
                            h = client.getContact(clientMID)
                            client.sendMessage(msg.to,"???[ Bio ]\n" + "? " +h.statusMessage)
                        elif cmd == "mypicture":
                            h = client.getContact(clientMID)
                            client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus)
                        elif cmd == "myvideo":
                            h = client.getContact(clientMID)
                            if h.videoProfile == None:
                            	return client.sendMessage(to, "Anda tidak memiliki video profile")
                            client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus + "/vp")
                        elif cmd == "mycover":
                            h = client.getContact(clientMID)
                            cu = client.getProfileCoverURL(clientMID)
                            path = str(cu)
                            client.sendImageWithURL(msg.to, path)
                        elif cmd.startswith("changename: "):
                            string = removeCmd("changename:", text)
                            if len(string) <= 10000000000:
                                profile = client.getProfile()
                                profile.displayName = string
                                client.updateProfile(profile)
                                client.sendMessage(to,"Changed " + string + "")
                        elif cmd.startswith("changebio: "):
                            string = removeCmd("changebio:", text)
                            if len(string) <= 10000000000:
                                profile = client.getProfile()
                                profile.statusMessage = string
                                client.updateProfile(profile)
                                client.sendMessage(msg.to,"Changed " + string)
                        elif cmd.startswith("locate "):
                            if 'MENTION' in msg.contentMetadata.keys() != None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                G = client.getGroupIdsJoined()
                                cgroup = client.getGroups(G)
                                groups = client.groups
                                ngroup = ""
                                ngroup += "???[ Found In Group ]"
                                no = 0 + 1
                                num = 0
                                for mention in mentionees:
                                    for x in range(len(cgroup)):
                                        gMembMids = [contact.mid for contact in cgroup[x].members]
                                        if mention['M'] in gMembMids:
                                            ngroup += "\n? {}. {} | {}".format(str(no), str(cgroup[x].name), str(len(cgroup[x].members)))
                                            no += 1
                                            num += 1
                                    ngroup += "\n???[ Total {} Groups ]".format(str(num))
                                    client.sendMessage(to, str(ngroup))
                                if ngroup == "":
                                    client.sendMessage(to, "NOT FOUND")
                        elif cmd.startswith("getmid "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                ret_ = "[ Mid User ]"
                                for ls in lists:
                                    ret_ += "\n{}".format(str(ls))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("getpicture "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = "http://dl.profile.line.naver.jp/" + client.getContact(ls).pictureStatus
                                    client.sendImageWithURL(to, str(path))
                        elif cmd.startswith("getvideo "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    if contact.videoProfile == None:
                                    	continue
                                    path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus + "/vp"
                                    client.sendVideoWithURL(to, str(path))
                        elif cmd.startswith("getcover "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        path = client.getProfileCoverURL(ls)
                                        path = str(path)
                                        client.sendImageWithURL(to, str(path))
                        elif cmd.startswith("getname "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    client.sendMessage(to, "[ Display Name ]\n{}".format(str(contact.displayName)))
                        elif cmd.startswith("getbio "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    client.sendMessage(to, "[ Status Message ]\n{}".format(str(contact.statusMessage)))
                        elif cmd.startswith("getprofile "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    cu = client.getProfileCoverURL(ls)
                                    path = str(cu)
                                    image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                                    client.sendMessage(msg.to,"Nama :\n" + contact.displayName + "\nMid :\n" + contact.mid + "\n\nBio :\n" + contact.statusMessage)
                                    client.sendImageWithURL(msg.to,image)
                                    client.sendImageWithURL(msg.to,path)
                        elif cmd.startswith("getcontact "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    mi_d = contact.mid
                                    client.sendContact(to, mi_d)
                        elif cmd.startswith("midgetcontact "):
                            mid = removeCmd("midgetcontact", text)
                            if mid is not None:
                                listMid = mid.split("*")
                                if len(listMid) > 1:
                                    for a in listMid:
                                        client.sendContact(to,a)
                                else:
                                    client.sendContact(to,mid)
                        elif cmd.startswith("midclone ") and sender == clientMID:
                            target = removeCmd("midclone", text)
                            if target is not None:
                                cloneProfile(target)
                                client.sendContact(to,clientMID)
                                client.sendMessage(to,"Berhasil clone member")
                        elif cmd.startswith("cloneprofile ") and sender == clientMID:
                            if sender in clientMID:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    if len(lists) != []:
                                        ls = random.choice(lists)
                                        cloneProfile(ls)
                                        client.sendContact(to,clientMID)
                                        client.sendMessage(to,"Berhasil clone member")
                        elif cmd == "restoreprofile" and sender == clientMID:
                            if sender in clientMID:
                                try:
                                    restoreProfile()
                                    client.sendContact(to,clientMID)
                                    client.sendMessage(to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                                except Exception as e:
                                    client.sendMessage(to, "Gagal restore profile")
                                    client.sendMessage(msg.to, str(e))
                        elif cmd == "backupprofile" and sender == clientMID:
                            if sender in clientMID:
                                try:
                                    backupProfile()
                                    client.sendMessage(to, "Berhasil backup profile")
                                except Exception as e:
                                    client.sendMessage(to, "Gagal backup profile")
                                    client.sendMessage(msg.to, str(e))
                        elif cmd.startswith("mimicadd ") and sender == clientMID:
                            targets = []
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                try:
                                    settings["mimic"]["target"][target] = True
                                    client.sendMessage(msg.to,"Target ditambahkan!")
                                    break
                                except:
                                    client.sendMessage(msg.to,"Added Target Fail !")
                                    break
                        elif cmd.startswith("mimicdel ") and sender == clientMID:
                            targets = []
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                try:
                                    del settings["mimic"]["target"][target]
                                    client.sendMessage(msg.to,"Target dihapuskan!")
                                    break
                                except:
                                    client.sendMessage(msg.to,"Deleted Target Fail !")
                                    break
                        elif cmd == "mimiclist":
                            if settings["mimic"]["target"] == {}:
                                client.sendMessage(msg.to,"Tidak Ada Target")
                            else:
                                mc = "???[ Mimic List ]"
                                for mi_d in settings["mimic"]["target"]:
                                    mc += "\n? "+client.getContact(mi_d).displayName
                                client.sendMessage(msg.to,mc + "\n???[ Finish ]")
                        elif cmd.startswith("mimic ") and sender == clientMID:
                            mic = removeCmd("mimic", text)
                            if mic == "on":
                                if settings["mimic"]["status"] == False:
                                    settings["mimic"]["status"] = True
                                    client.sendMessage(msg.to,"Berhasil mengaktifkan mimic")
                            elif mic == "off":
                                if settings["mimic"]["status"] == True:
                                    settings["mimic"]["status"] = False
                                    client.sendMessage(msg.to,"Berhasil menonaktifkan mimic")
                        elif cmd.startswith("youtubeinfo "):
                            url = removeCmd("youtubeinfo", text)
                            params = {"vid": url}
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("http://api.ntcorp.us/yt/download?{}".format(urllib.parse.urlencode(params)))
                                try:
                                    data = json.loads(r.text)
                                    path = data["info"]["thumbnail"]
                                    if settings["server"] == "VPS":
                                        client.sendImageWithURL(to, str(path))
                                    else:
                                        urllib.urlretrieve(path, "res.jpg")
                                        client.sendImage(to, "res.jpg")
                                    ret_ = "???[ Youtube Info ]"
                                    ret_ += "\n? Judul : {}".format(str(data["info"]["title"]))
                                    ret_ += "\n? Saluran : {}".format(str(data["info"]["channel"].replace("+"," ")))
                                    ret_ += "\n? Penonton : {}".format(str(data["info"]["view_count"]))
                                    ret_ += "\n???[ Finish ]"
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "URL tidak valid")
                        elif cmd.startswith("youtubemp3 "):
                            link = removeCmd("youtubemp3", text)
                            r = _session.get('http://api.corrykalam.net/apiytmp3.php?link='+link)
                            data = r.text
                            client.sendAudioWithURL(to,str(data))
                        elif cmd.startswith("youtubemp4 "):
                            link = removeCmd("youtubemp4", text)
                            r = _session.get('http://api.corrykalam.net/apimp4.php?link='+link)
                            data = r.text
                            client.sendVideoWithURL(to,str(data))
                        elif cmd.startswith("youtubedownload "):
                            url = removeCmd("youtubedownload", text)
                            params = {"url": url}
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("http://www.saveitoffline.com/process/?{}".format(urllib.parse.urlencode(params)))
                                try:
                                    data = json.loads(r.text)
                                    ret_ = "???[ Youtube Download ]"
                                    ret_ += "\n? Judul : {}".format(str(data["title"]))
                                    for res in data["urls"]:
                                        ret_ += "\n???[ {} ]".format(str(res["label"]))
                                        ret_ += "\n? {}".format(str(res["id"]))
                                        ret_ += "\n???[ Finish ]"
                                    try:
                                        path = data["thumbnail"]
                                        if settings["server"] == "VPS":
                                            client.sendImageWithURL(to, str(path))
                                        else:
                                            urllib.urlretrieve(path, "res.jpg")
                                            client.sendImage(to, "res.jpg")
                                    except:
                                        pass
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "URL tidak valid")
                        elif cmd.startswith("youtubesearch "):
                            search = removeCmd("youtubesearch", text)
                            params = {"search_query": search}
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://www.youtube.com/results", params = params)
                                soup = BeautifulSoup(r.content, "html5lib")
                                ret_ = "???[ Youtube Result ]"
                                datas = []
                                for data in soup.select(".yt-lockup-title > a[title]"):
                                    if "&lists" not in data["href"]:
                                        datas.append(data)
                                for data in datas:
                                    ret_ += "\n???[ {} ]".format(str(data["title"]))
                                    ret_ += "\n? https://www.youtube.com{}".format(str(data["href"]))
                                ret_ += "\n???[ Total {} ]".format(len(datas))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("wikipedia "):
                            search = removeCmd("wikipedia", text)
                            wiki = WikiApi({'locale':'id'})
                            results = wiki.find(search)
                            for a in results:
                                ret_ = "???[ Wikipedia ]"
                                article = wiki.get_article(a)
                                if article.image is not None: client.sendImageWithURL(to,str(article.image))
                                ret_ += "\n? Judul : {}".format(str(article.heading))
                                ret_ += "\n? URL : {}".format(str(article.url))
                                ret_ += "\n???[ Ringkasan ]\n{}".format(str(article.summary.replace("^","")))
                                client.sendMessage(to,ret_)
                        elif cmd.startswith("lyric "):
                            search = removeCmd("lyric", text)
                            params = {'songname': search}
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                                try:
                                    data = json.loads(r.text)
                                    for song in data:
                                        songs = song[5]
                                        lyric = songs.replace('ti:','Title - ')
                                        lyric = lyric.replace('ar:','Artist - ')
                                        lyric = lyric.replace('al:','Album - ')
                                        removeString = "[1234567890.:]"
                                        for char in removeString:
                                            lyric = lyric.replace(char,'')
                                        ret_ = "???[ Lyric ]"
                                        ret_ += "\n? Nama lagu : {}".format(str(song[0]))
                                        ret_ += "\n? Durasi : {}".format(str(song[1]))
                                        ret_ += "\n? Link : {}".format(str(song[4]))
                                        ret_ += "\n???[ Finish ]\n{}".format(str(lyric))
                                        client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Lirik tidak ditemukan")
                        elif cmd.startswith("music "):
                            search = removeCmd("music", text)
                            params = {'songname': search}
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://ide.fdlrcn.com/workspace/yumi-apis/joox?" + urllib.parse.urlencode(params))
                                try:
                                    data = json.loads(r.text)
                                    for song in data:
                                        ret_ = "???[ Music ]"
                                        ret_ += "\n? Nama lagu : {}".format(str(song[0]))
                                        ret_ += "\n? Durasi : {}".format(str(song[1]))
                                        ret_ += "\n? Link : {}".format(str(song[4]))
                                        ret_ += "\n???[ Waiting Audio ]"
                                        client.sendMessage(to, str(ret_))
                                        client.sendMessage(to, "Mohon bersabar musicnya lagi di upload")
                                        client.sendAudioWithURL(to, song[3])
                                except:
                                        client.sendMessage(to, "Musik tidak ditemukan")
                        elif cmd.startswith("musicsearch "):
                            text_ = removeCmd("musicsearch", text)
                            cond = text_.split("|")
                            search = str(cond[0])
                            params = {'q': search}
                            session = _session
                            r = session.get("http://api.ntcorp.us/joox/search?" + urllib.parse.urlencode(params))
                            data = r.text
                            data = json.loads(data)
                            if len(cond) == 1:
                                if data["result"] != []:
                                    no = 0
                                    ret_ = "???[ Music Search ]"
                                    for music in data["result"]:
                                        no += 1
                                        ret_ += "\n? " + str(no) + ". " + str(music["single"]) + " by " + str(music["artist"])
                                    ret_ += "\n???[ Finish ]\n\nType %sMusicsearch %s|?number?" %(setKey, str(search))
                                    client.sendMessage(to,ret_)
                                else:
                                    client.sendMessage(to,"Sorry, no result for " + str(search))
                            elif len(cond) == 2:
                                num = int(cond[1])
                                if num <= len(data):
                                    music = data["result"][num - 1]
                                    path = "http://api.ntcorp.us/joox/d/mp3/" + str(music["sid"])
                                    ret_ = "???[ Music Details ]"
                                    ret_ += "\n? Single : " + str(music["single"])
                                    ret_ += "\n? Artist : " + str(music["artist"])
                                    ret_ += "\n? Album  : " + str(music["album"])
                                    ret_ += "\n? Played : " + str(music["played"])
                                    ret_ += "\n???[ Finish ]"
                                    client.sendAudioWithURL(to,path)
                                    client.sendMessage(to, ret_)
                                else:
                                    client.sendMessage(to,"Sorry, index out of range")
                        elif cmd.startswith("imagesearch "):
                            start = time.time()
                            search = removeCmd("imagesearch", text)
                            url = "https://xeonwz.herokuapp.com/images/google.api?q=" + urllib.parse.quote(search)
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get(url)
                                data = r.text
                                data = json.loads(data)
                                if data["status"] == True:
                                    items = data["content"]
                                    path = random.choice(items)
                                    a = items.index(path)
                                    b = len(items)
                                    client.sendImageWithURL(to, str(path))
                                    elapsed_time = time.time() - start
                                    client.sendMessage(to,"[Image Result]\nGot image in %s seconds" %(elapsed_time))
                        elif cmd.startswith("deviantart "):
                            start = time.time()
                            search = removeCmd("deviantart", text)
                            with _session as web:
                                web.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://xeonwz.herokuapp.com/images/deviantart.api?q={}".format(urllib.parse.quote(search)))
                                data = r.text
                                data = json.loads(data)
                                if data["status"] == True:
                                    path = random.choice(data["content"])
                                    client.sendImageWithURL(to, str(path))
                                    elapsed_time = time.time() - start
                                    client.sendMessage(to,"[Image Result]\nGot image in %s seconds" %(elapsed_time))
                                else:
                                    client.sendMessage(to, "Hasil pencarian tidak ditemukan")
                        elif cmd.startswith("githubprofile "):
                            username = removeCmd("githubprofile", text)
                            r = _session.get("https://api.github.com/users/" + username)
                            data = r.text
                            profile = json.loads(data)
                            if profile != [] and "message" not in profile:
                                ret_ = "???[ Github Profile ]"
                                ret_ += "\n? Username : " + str(profile["login"])
                                ret_ += "\n? Full Name : " + str(profile["name"])
                                ret_ += "\n? Type : " + str(profile["type"])
                                if profile["company"] is None:
                                    ret_ += "\n? Company : None"
                                else:
                                    ret_ += "\n? Company : " + str(profile["company"])
                                if profile["blog"] is None:
                                    ret_ += "\n? Website : None"
                                else:
                                    ret_ += "\n? Website : " + str(profile["blog"])
                                if profile["location"] is None:
                                    ret_ += "\n? Location : None"
                                else:
                                    ret_ += "\n? Location : " + str(profile["location"])
                                if profile["email"] is None:
                                    ret_ += "\n? Email : None"
                                else:
                                    ret_ += "\n? Email : " + str(profile["email"])
                                if profile["bio"] is None:
                                    ret_ += "\n? Biography : None"
                                else:
                                    ret_ += "\n? Biography : " + str(profile["bio"])
                                ret_ += "\n? Public Repository : " + format_number(str(profile["public_repos"]))
                                ret_ += "\n? Public Gists : " + format_number(str(profile["public_gists"]))
                                ret_ += "\n? Followers : " + format_number(str(profile["followers"]))
                                ret_ += "\n? Following : " + format_number(str(profile["following"]))
                                ret_ += "\n? Created At : " + str(profile["created_at"])
                                ret_ += "\n? Updated At : " + str(profile["updated_at"])
                                ret_ += "\n? Url Github : https://github.com/" + username
                                ret_ += "\n???[ finish ]"
                                client.sendImageWithURL(to,str(profile["avatar_url"]))
                                client.sendMessage(to,ret_)
                            elif "message" in profile:
                                client.sendMessage(to,"User tidak di temukan")
                        elif cmd.startswith("profileig "):
                            try:
                                instagram = removeCmd("profileig", text)
                                response = _session.get("https://www.instagram.com/"+instagram+"?__a=1")
                                data = response.json()
                                namaIG = str(data['user']['full_name'])
                                bioIG = str(data['user']['biography'])
                                mediaIG = str(data['user']['media']['count'])
                                verifIG = str(data['user']['is_verified'])
                                usernameIG = str(data['user']['username'])
                                followerIG = str(data['user']['followed_by']['count'])
                                profileIG = data['user']['profile_pic_url_hd']
                                privateIG = str(data['user']['is_private'])
                                followIG = str(data['user']['follows']['count'])
                                link = "Link: " + "https://www.instagram.com/" + instagram
                                text = "???[ Instagram User info ]" + "\n? Name : "+namaIG+"\n? Username : "+usernameIG+"\n? Biography : "+bioIG+"\n? Follower : "+followerIG+"\n? Following : "+followIG+"\n? Post : "+mediaIG+"\n? Verified : "+verifIG+"\n? Private : "+privateIG+"" "\n???[ " + link + " ]"
                                client.sendImageWithURL(msg.to, profileIG)
                                client.sendMessage(msg.to, str(text))
                            except Exception as e:
                                    client.sendMessage(msg.to, str(e))
                        elif cmd.startswith("postig "):
                            user = removeCmd("postig", text)
                            profile = "https://www.instagram.com/" + user
                            with _session as x:
                                x.headers['user-agent'] = 'Mozilla/5.0'
                                end_cursor = ''
                                for count in range(1, 50):
                                    r = x.get(profile, params={'max_id': end_cursor})
                                    data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                                    j    = json.loads(data)
                                    for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']:
                                        if node['is_video']:
                                            page = 'https://www.instagram.com/p/' + node['code']
                                            r = x.get(page)
                                            url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                                            print(url)
                                            client.sendVideoWithURL(msg.to,url)
                                        else:
                                            print (node['display_src'])
                                            client.sendImageWithURL(msg.to,node['display_src'])
                                    end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
                        elif cmd.startswith("pictureig "):
                            cari = removeCmd("pictureig", text)
                            try:
                                respon = _session.get(cari+"?__a=1")
                                data = respon.json()
                                ig_url = data['graphql']['shortcode_media']['display_url']
                                client.sendImageWithURL(msg.to,ig_url)
                            except:
                                client.sendMessage(msg.to,"Error")
                        elif cmd.startswith("videoig "):
                            cari = removeCmd("videoig", text)
                            try:
                                respon = _session.get(cari+"?__a=1")
                                data = respon.json()
                                ig_url = data['graphql']['shortcode_media']['video_url']
                                client.sendVideoWithURL(msg.to,ig_url)
                            except:
                                client.sendMessage(msg.to,"Error")
                        elif cmd.startswith("checkdate "):
                            tanggal = removeCmd("checkdate", text)
                            r = _session.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                            data=r.text
                            data=json.loads(data)
                            lahir = data["data"]["lahir"]
                            usia = data["data"]["usia"]
                            ultah = data["data"]["ultah"]
                            zodiak = data["data"]["zodiak"]
                            client.sendMessage(msg.to,"???[ Date Of Birth Information ]\n"+"? Date Of Birth : "+lahir+"\n? Age : "+usia+"\n? Birthday : "+ultah+"\n? Zodiak : "+zodiak+"\n???[ Information Done ]")
                        elif cmd == "kalender":
                            tz = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.now(tz=tz)
                            day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                            hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                            bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                            hr = timeNow.strftime("%A")
                            bln = timeNow.strftime("%m")
                            for i in range(len(day)):
                                if hr == day[i]: hasil = hari[i]
                            for k in range(0, len(bulan)):
                                if bln == str(k): bln = bulan[k-1]
                            readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : " + timeNow.strftime('%H:%M:%S')
                            client.sendMessage(msg.to, readTime)
                        elif cmd.startswith("checkpraytime "):
                            location = removeCmd("checkpraytime", text)
                            with _session as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                r = web.get("http://api.corrykalam.net/apisholat.php?lokasi={}".format(urllib2.quote(location)))
                                data = r.text
                                data = json.loads(data)
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                if data[1] != "Subuh : " and data[2] != "Dzuhur : " and data[3] != "Ashar : " and data[4] != "Maghrib : " and data[5] != "Isya : ":
                                    ret_ = "???[ Jadwal Sholat ]"
                                    ret_ += "\n? Daerah : " + data[0]
                                    ret_ += "\n? Tanggal : " + datetime.strftime(timeNow,'%Y-%m-%d')
                                    ret_ += "\n? " + data[1]
                                    ret_ += "\n? " + data[2]
                                    ret_ += "\n? " + data[3]
                                    ret_ += "\n? " + data[4]
                                    ret_ += "\n? " + data[5]
                                    ret_ += "\n???[ Success ]"
                                else:
                                    ret_ = "[Prayer Schedule] Error : Location not found"
                                client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("checkweather "):
                            location = removeCmd("checkweather", text)
                            with _session as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                r = web.get("http://api.corrykalam.net/apicuaca.php?kota={}".format(urllib2.quote(location)))
                                data = r.text
                                data = json.loads(data)
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.now(tz=tz)
                                if "result" not in data:
                                    ret_ = "???[ Weather Status ]"
                                    ret_ += "\n? Location : " + data[0].replace("Temperatur di kota ","")
                                    ret_ += "\n? Suhu : " + data[1].replace("Suhu : ","") + "�C"
                                    ret_ += "\n? Kelembaban : " + data[2].replace("Kelembaban : ","") + "%"
                                    ret_ += "\n? Tekanan udara : " + data[3].replace("Tekanan udara : ","") + "HPa"
                                    ret_ += "\n? Kecepatan angin : " + data[4].replace("Kecepatan angin : ","") + "m/s"
                                    ret_ += "\n???[ Time Status ]"
                                    ret_ += "\n? Tanggal : " + datetime.strftime(timeNow,'%Y-%m-%d')
                                    ret_ += "\n? Jam : " + datetime.strftime(timeNow,'%H:%M:%S') + " WIB"
                                    ret_ += "\n???[ Success ]"
                                else:
                                    ret_ = "[Weather Status] Error : Location not found"
                                client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("checklocation "):
                            location = removeCmd("checklocation", text)
                            with _session as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                r = web.get("http://api.corrykalam.net/apiloc.php?lokasi={}".format(urllib2.quote(location)))
                                data = r.text
                                data = json.loads(data)
                                if data[0] != "" and data[1] != "" and data[2] != "":
                                    link = "https://www.google.co.id/maps/@{},{},15z".format(str(data[1]), str(data[2]))
                                    ret_ = "???[ Location Status ]"
                                    ret_ += "\n? Location : " + data[0]
                                    ret_ += "\n? Google Maps : " + link
                                    ret_ += "\n???[ Success ]"
                                else:
                                    ret_ = "[Details Location] Error : Location not found"
                                client.sendMessage(msg.to,str(ret_))
                        elif cmd == "1cak":
                            r = _session.get('http://api-1cak.herokuapp.com/random')
                            data = r.text
                            data = json.loads(data)
                            img = data["img"]
                            client.sendMessage(to,"???[ 1cak Result ]\n? Title: %s\n? Url: %s\n? Id: %s\n? Votes: %s\n? NSFW: %s\n???[ Finish ]" %(str(data["title"].replace('FACEBOOK Comments', ' ')), str(data["url"]), str(data["id"]), str(data["votes"]), str(data["nsfw"])))
                        elif cmd.startswith("checkwebsite "):
                            text = removeCmd("checkwebsite", text)
                            cond = text.split("|")
                            web = cond[0]
                            if cond[1].startswith("fp="):
                                fp = cond[1].replace("fp=","")
                                if fp == "T":
                                    fullpage = "&fullpage=1"
                                elif fp == "F":
                                    fullpage = ""
                            path = "http://api.screenshotlayer.com/api/capture?access_key={}&url={}{}&format=JPG".format(settings["access_key"],urllib.parse.quote(web),fullpage)
                            client.sendImageWithURL(to,str(path))
                        elif cmd.startswith("checkimage "):
                            path = removeCmd("checkimage", text)
                            if path is not None:
                                client.sendImageWithURL(to,path)
                        elif cmd.startswith("checkgif "):
                            path = removeCmd("checkgif", text)
                            if path is not None:
                                client.sendGIFWithURL(to,path)
                        elif cmd.startswith("checkvideo "):
                            path = removeCmd("checkvideo", text)
                            if path is not None:
                                client.sendVideoWithURL(to,path)
                        elif cmd.startswith("checkaudio "):
                            path = removeCmd("checkaudio", text)
                            if path is not None:
                                client.sendAudioWithURL(to,path)
                        elif cmd.startswith("shorturl "):
                            try:
                                url = removeCmd("shorturl", text)
                                r = _session.get("http://tiny-url.info/api/v1/create?apikey=A942F93B8B88C698786A&provider=bit_ly&format=json&url={}".format(str(url)))
                                data = r.text
                                data = json.loads(data)
                                anu = data["shorturl"]
                                ret_ = "?Shorten?"
                                ret_ += "\n\nShort url : {}".format(str(anu))
                                client.sendMessage(to, str(ret_))
                            except:
                                try:
                                    url = removeCmd("shorturl", text)
                                    r = _session.get("http://tiny-url.info/api/v1/create?apikey=A942F93B8B88C698786A&provider=bit_ly&format=json&url=http://{}".format(str(url)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["shorturl"]
                                    ret_ = "?Shorten?"
                                    ret_ += "\n\nShort URL : {}".format(str(anu))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "URL invalid !")
                        elif cmd.startswith("directsolidfiles "):
                            try:
                                link = removeCmd("directsolidfiles", text)
                                with _session as web:
                                    web.headers["user-agent"] = random.choice(settings["userAgent"])
                                    r = web.get("http://api.corrykalam.net/solidfiles.php?url={}".format(str(link)))
                                    data = r.text
                                    client.sendMessage(to, str(data))
                            except:
                                    client.sendMessage(to, "URL invalid !")
                        elif cmd == 'gift':
                            cl.sendMessage(to, text=None, contentMetadata={'PRDID': '350d37d6-bfc9-44cb-a0d1-cf17ae3657db','PRDTYPE': 'THEME','MSGTPL': '5'}, contentType=9)
                        elif cmd == "quotes":
                            try:
                                with _session as web:
                                    r = web.get("https://talaikis.com/api/quotes/random/")
                                    try:
                                        data = json.loads(r.text)
                                        ret_ = "???[ Random Quotes ]"
                                        ret_ += "\n? Penulis : {}".format(data["author"])
                                        ret_ += "\n? Kategori : {}".format(data["cat"])
                                        ret_ += "\n???[ Kutipan ]\n{}".format(data["quote"])
                                        client.sendMessage(to, str(ret_))
                                    except:
                                        client.sendMessage(to, "Tidak ada hasil ditemukan")
                            except Exception as error:
                                client.logError(error, to)
                        elif cmd.startswith("checktimezone "):
                            location = removeCmd("checktimezone", text)
                            with _session as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://time.siswadi.com/timezone/{}".format(urllib2.quote(location)))
                                data = json.loads(r.text)
                                ret_ = "???[ Zona waktu ]\n? {}".format(data["data"]["timezone"])
                                ret_ += "\n???[ Waktu ]\n" + "? Tanggal {}".format(data["time"]["date"])
                                ret_ += " Jam {}".format(data["time"]["time"])
                                ret_ += "\n???[ Lokasi ]\n? {}".format(data["location"]["address"])
                                ret_ += "\n???[ Finish ]"
                                client.sendMessage(msg.to,str(ret_))
                        elif cmd.startswith("quran "):
                            query = removeCmd("quran", text)
                            with _session as web:
                                r = web.get("http://ariapi.herokuapp.com/api/quran/search?q={}&key=beta".format(urllib.parse.quote(query)))
                                data = r.text
                                data = json.loads(data)
                                ret_ = "??????[ Hasil Pencarian ]??????"
                                no = 0
                                for anu in data["result"]["matches"]:
                                    no += 1
                                    ret_ += "\n\n{}.".format(str(no))
                                    ret_ += "Qur'an Surah : {}".format(str(anu["quransurah"]["latin"]))
                                    ret_ += "\n{}\n".format(str(anu["text"]))
                                ret_ += "\n?????[ Total Pencarian : {} ]?????".format(str(len(data["result"]["matches"])))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("searchmovie "):
                            query = removeCmd("searchmovie", text)
                            with _session as web:
                                try:
                                    r = web.get("https://xeonwz.herokuapp.com/movie/search.api?q={}".format(urllib.parse.quote(query)))
                                    data = r.text
                                    data = json.loads(data)
                                    text_ = "??????[ Hasil Pencarian ]??????"
                                    for anu in data["content"]:
                                        text_ += "\n\nTitle : {}".format(str(anu["title"]))
                                        text_ += "\nUrl : {}".format(str(anu["url"]))
                                    client.sendMessage(to, str(text_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("searchmovie2 "):
                            kata = removeCmd("searchmovie2", text)
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/movie/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]
                                    ret_ = "?Movie?"
                                    no = 1
                                    for s in anu:
                                        hmm = s
                                        cum = hmm['title']
                                        ret_ += "\n\n{}. {}".format(str(no), str(cum))
                                        no += 1
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("anime "):
                            judul = removeCmd("anime", text)
                            with _session as web:
                                try:
                                    r = web.get("https://kitsu.io/api/edge/anime?filter[text]={}".format(str(judul)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["data"][0]
                                    title = anu["attributes"]["titles"]["en_jp"]
                                    synopsis = anu["attributes"]["synopsis"]
                                    id = anu["id"]
                                    link = anu["links"]["self"]
                                    ret_ = "?About Anime?"
                                    ret_ += "\n\nTitle : {}\nSynopsis : {}\nId : {}\nLink : {}".format(str(title), str(synopsis), str(id), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("searchanime "):
                            kata = removeCmd("searchanime", text)
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["anime"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "?Anime?"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("searchmanga "):
                            kata = removeCmd("searchmanga", text)
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["manga"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "?Manga?"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("searchcharacter "):
                            kata = removeCmd("searchcharacter", text)
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["character"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "?Character?"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Tidak ada hasil ditemukan")
                        elif cmd.startswith("suggestion "):
                            kata = removeCmd("suggestion", text)
                            with _session as web:
                                try:
                                    r = web.get("http://api.ntcorp.us/se/v1/?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    ret_ = "?Suggestions?"
                                    no = 1
                                    anu = data["result"]["suggestions"]
                                    if len(anu) >= 5:
                                        for s in range(5):
                                            hmm = anu[s]
                                            ret_ += "\n\n{}. {}".format(str(no), str(hmm))
                                            no += 1
                                    else:
                                        for s in anu:
                                            hmm = s
                                            ret_ += "\n\n{}. {}".format(str(no), str(hmm))
                                            no += 1
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Suggestion not found !")
                        elif cmd.startswith("searchporn "):
                            kata = removeCmd("searchporn", text)
                            with _session as web:
                                try:
                                    r = web.get("https://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    ret_ = "?Porn?"
                                    no = 1
                                    anu = data["videos"]
                                    if len(anu) >= 5:
                                        for s in range(5):
                                            hmm = anu[s]
                                            title = hmm['video']['title']
                                            duration = hmm['video']['duration']
                                            views = hmm['video']['views']
                                            link = hmm['video']['embed_url']
                                            ret_ += "\n\n{}. Title : {}\n    Duration : {}\n    Views : {}\n    Link : {}".format(str(no), str(title), str(duration), str(views), str(link))
                                            no += 1
                                    else:
                                        for s in anu:
                                            hmm = s
                                            title = hmm['video']['title']
                                            duration = hmm['video']['duration']
                                            views = hmm['video']['views']
                                            link = hmm['video']['embed_url']
                                            ret_ += "\n\n{}. Title : {}\n    Duration : {}\n    Views : {}\n    Link : {}".format(str(no), str(title), str(duration), str(views), str(link))
                                            no += 1
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Porn Not Found !")
                        elif cmd == "topnews":
                             try:
                                 api_key = "a53cb61cee4d4c518b69473893dba73b"
                                 r = _session.get("https://newsapi.org/v2/top-headlines?country=id&apiKey={}".format(str(api_key)))
                                 data = r.text
                                 data = json.loads(data)
                                 ret_ = "?Top News?"
                                 no = 1
                                 anu = data["articles"]
                                 if len(anu) >= 5:
                                     for s in range(5):
                                         syit = anu[s]
                                         sumber = syit['source']['name']
                                         author = syit['author']
                                         judul = syit['title']
                                         url = syit['url']
                                         ret_ += "\n\n{}. Judul : {}\n    Sumber : {}\n    Penulis : {}\n    Link : {}".format(str(no), str(judul), str(sumber), str(author), str(url))
                                         no += 1
                                 else:
                                     for s in anu:
                                         syit = s
                                         sumber = syit['source']['name']
                                         author = syit['author']
                                         judul = syit['title']
                                         url = syit['url']
                                         ret_ += "\n\n{}. Judul : {}\n    Sumber : {}\n    Penulis : {}\n    Link : {}".format(str(no), str(judul), str(sumber), str(author), str(url))
                                         no += 1
                                 client.sendMessage(to, str(ret_))
                             except:
                                 client.sendMessage(to, "Porn Not Found !")
                        elif cmd.startswith("asking "):
                            kata = removeCmd("asking", text)
                            sch = kata.replace(" ","+")
                            with _session as web:
                                urlz = "http://lmgtfy.com/?q={}".format(str(sch))
                                r = _session.get("http://tiny-url.info/api/v1/create?apikey=A942F93B8B88C698786A&provider=cut_by&format=json&url={}".format(str(urlz)))
                                data = r.text
                                data = json.loads(data)
                                url = data["shorturl"]
                                ret_ = "?Ask?"
                                ret_ += "\n\nLink : {}".format(str(url))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("storyig "):
                            query = removeCmd("storyig", text)
                            with _session as web:
                                r = web.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(urllib.parse.quote(query)))
                                data = r.text
                                data = json.loads(data)
                                for anu in data["url"]:
                                     if anu ["tipe"] == 1:
                                          client.sendImageWithURL(to, str(anu["link"]))
                                     elif anu ["tipe"] == 2:
                                          client.sendVideoWithURL(to, str(anu["link"]))
                        elif cmd.startswith("checkip "):
                            search = removeCmd("checkip", text)
                            r = _session.get("https://ipapi.co/" + search + "/json")
                            data = r.text
                            data = json.loads(data)
                            if "error" not in data:
                                ret_ = "???[ Ip Checker ]"
                                ret_ += "\n? Ip : {}".format(data["ip"])
                                ret_ += "\n? City : {}".format(data["city"])
                                ret_ += "\n? Region : {}".format(data["region"])
                                ret_ += "\n? Region Code : {}".format(data["region_code"])
                                ret_ += "\n? Country : {}".format(data["country"])
                                ret_ += "\n? Country Name : {}".format(data["country_name"])
                                ret_ += "\n? Postal : {}".format(data["postal"])
                                ret_ += "\n? Latitude : {}".format(data["latitude"])
                                ret_ += "\n? Longitude : {}".format(data["longitude"])
                                ret_ += "\n? Timezone : {}".format(data["timezone"])
                                ret_ += "\n? ASN Code : {}".format(data["asn"])
                                ret_ += "\n? Organization : {}".format(data["org"])
                                ret_ += "\n???[ Success ]"
                                client.sendMessage(msg.to,str(ret_))
                            else:
                                client.sendMessage(to, "IP not found !")
                        elif cmd.startswith("idline "):
                            a = removeCmd("idline", text)
                            b = client.findContactsByUserid(a)
                            line = b.mid
                            client.sendMessage(msg.to,"http://line.me/ti/p/~" + a)
                            client.sendContact(to, line)
                        elif cmd.startswith("say "):
                            text_ = removeCmd("say", text)
                            cond = text_.split(" ")
                            bahasa = cond[0]
                            say = text_.replace(bahasa + " ","")
                            if bahasa in ["af", "sq", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ny", "zh", "zh", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "gl", "ka", "de", "el", "gu", "ht", "ha", "iw", "hi", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "lo", "la", "lv", "lt", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "fa", "pl", "pt", "pa", "ro", "ru", "sr", "st", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "yi", "yo", "zu"]:
                                tts = gTTS(text=say,lang=bahasa)
                                tts.save("hasil.mp3")
                                client.sendAudio(msg.to,"hasil.mp3")
                            elif bahasa == "language":
                                f = open('country.txt','r')
                                lines = f.readlines()
                                panjang = len(lines)
                                lists = ""
                                for a in lines:
                                    lists += str(a)
                                client.sendMessage(to,"[List Language]\n" + str(lists))
                            else:
                                client.sendMessage(receiver,"[Auto Respond] Language not found")
                        elif cmd.startswith("tr "):
                            text_ = removeCmd("tr", text)
                            cond = text_.split(" ")
                            bahasa = cond[0]
                            text = text_.replace(bahasa + " ","")
                            if bahasa in ["af", "sq", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ny", "zh", "zh", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "gl", "ka", "de", "el", "gu", "ht", "ha", "iw", "hi", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "lo", "la", "lv", "lt", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "fa", "pl", "pt", "pa", "ro", "ru", "sr", "st", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "yi", "yo", "zu"]:
                                translator = Translator()
                                hasil = translator.translate(text,dest=bahasa)
                                A = hasil.text
                                client.sendMessage(to, A)
                            elif bahasa == "language":
                                f = open('country.txt','r')
                                lines = f.readlines()
                                panjang = len(lines)
                                lists = ""
                                for a in lines:
                                    lists += str(a)
                                client.sendMessage(to,"[List Language]\n" + str(lists))
                            else:
                                client.sendMessage(receiver,"[Auto Respond] Language not found")
                        elif cmd.startswith("creatememe "):
                            text_ = removeCmd("creatememe", text)
                            cond = text_.split("|")
                            list_template = ["10guy","afraid","blb","both","buzz","chosen","doge","elf","ermg","fa","fetch","fry","fwp","ggg","icanhas","interesting","iw","keanu","live","ll","mordor","morpheus","officiespace","oprah","philosoraptor","remembers","sb","ss","success","toohigh","wonka","xy","yallgot","yuno"]
                            if cond[0] is not None and cond[1] is not None:
                                up = str(cond[0])
                                down = str(cond[1])
                                if len(cond) > 2:
                                    if cond[2] is not None and cond[2] in list_template:
                                        template = str(cond[2])
                                    elif cond[2] is not None and cond[2] not in list_template:
                                        template = None
                                        client.sendMessage(to,"Template tidak valid")
                                else:
                                    template = random.choice(list_template)
                                if template is not None:
                                    client.sendImageWithURL(to,"https://memegen.link/{}/{}/{}.jpg".format(template,up,down))
                            else:
                                client.sendMessage(to,"Error")
                        elif cmd == "template memegen":
                            f = open('memeGen.txt','r')
                            lines = f.readlines()
                            panjang = len(lines)
                            lists = ""
                            for a in lines:
                                lists += str(a)
                            client.sendMessage(to,"Template List :\n%s" %(lists))
                        elif cmd.startswith("imagetext "):
                            text_ = removeCmd("imagetext", text)
                            web = _session
                            web.headers["User-Agent"] = random.choice(settings["userAgent"])
                            font = random.choice(["arial","comic"])
                            r = web.get("http://api.img4me.com/?text=%s&font=%s&fcolor=FFFFFF&size=35&bcolor=000000&type=jpg" %(urllib.parse.quote(text_),font))
                            data = str(r.text)
                            if "Error" not in data:
                                path = data
                                client.sendImageWithURL(to,path)
                            else:
                                client.sendMessage(to,"[RESULT] %s" %(data.replace("Error: ")))
                        elif cmd in ["mention me", "who's tag me", "siapa yang tag"] and sender == clientMID:
                            if to in settings["userMentioned"]:
                                if settings["userMentioned"][to] != {}:
                                    userMentioned(to)
                                else:
                                    client.sendMessage(to, "Tidak ada yang ngetag")
                            else:
                                client.sendMessage(to, "Tidak ada yang ngetag")
                        elif cmd == "changeprofilepicture" and sender == clientMID:
                            settings["changePicture"] = True
                            client.sendMessage(to, "Silahkan kirim gambarnya")
                        elif cmd == "changeprofilecover" and sender == clientMID:
                            settings["changeCover"] = True
                            client.sendMessage(to, "Silahkan kirim gambarnya")
                        elif cmd == "changevideoprofile" and sender == clientMID:
                            settings['changeProfileVideo']['status'] = True
                            settings['changeProfileVideo']['stage'] = 1
                            client.sendMessage(to, "Silahkan kirimkan video yang ingin anda jadikan profile")
                        elif cmd == "abort" and sender == clientMID:
                            settings['changePicture'] = False
                            settings['changeCover'] = False
                            settings['changeProfileVideo']['stage'] = 0
                            settings['changeProfileVideo']['status'] = False
                            if to in settings['changeGroupPicture']:
                            	settings['changeGroupPicture'].remove(to)
                            client.sendMessage(to, "Operasi dibatalkan")
                        elif cmd == "changegrouppicture":
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                                client.sendMessage(to, "Silahkan kirim gambarnya")
                        elif cmd == "mention":
                            if msg.toType == 0:
                                sendMention(to, to)
                            elif msg.toType == 2:
                                group = client.getGroup(to)
                                contact = [mem.mid for mem in group.members]
                                ct1, ct2, ct3, ct4, ct5, jml = [], [], [], [], [], len(contact)
                                if jml <= 100:
                                    mentionMembers(to, contact)
                                elif jml > 100 and jml <= 200:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, jml):
                                        ct2 += [contact[b]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                elif jml > 200 and jml <= 300:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, jml):
                                        ct3 += [contact[c]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                elif jml > 300 and jml <= 400:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, 299):
                                        ct3 += [contact[c]]
                                    for d in range(300, jml):
                                        ct4 += [contact[d]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                elif jml > 400 and jml <= 500:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, 299):
                                        ct3 += [contact[c]]
                                    for d in range(300, 399):
                                        ct4 += [contact[d]]
                                    for e in range(400, jml):
                                        ct4 += [contact[e]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                        elif cmd == "lurking on":
                            tz = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.now(tz=tz)
                            day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                            hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                            bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                            hr = timeNow.strftime("%A")
                            bln = timeNow.strftime("%m")
                            for i in range(len(day)):
                                if hr == day[i]: hasil = hari[i]
                            for k in range(0, len(bulan)):
                                if bln == str(k): bln = bulan[k-1]
                            readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                            if to in read["readPoint"]:
                                client.sendMessage(to, "Lurking sudah aktif ketik {}Lurking untuk menampilkan hasil".format(str(setKey)))
                            else:
                                try:
                                    read["readPoint"][to] = True
                                    read["readMember"][to] = {}
                                    read["readTime"][to] = readTime
                                    read["ROM"][to] = {}
                                    client.sendMessage(to, "Set reading point:\n" + readTime)
                                except:
                                    pass
                        elif cmd == "lurking off":
                            tz = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.now(tz=tz)
                            day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                            hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                            bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                            hr = timeNow.strftime("%A")
                            bln = timeNow.strftime("%m")
                            for i in range(len(day)):
                                if hr == day[i]: hasil = hari[i]
                            for k in range(0, len(bulan)):
                                if bln == str(k): bln = bulan[k-1]
                            readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                            if to in read["readPoint"]:
                                try:
                                    del read["readPoint"][to]
                                    del read["readMember"][to]
                                    del read["readTime"][to]
                                    del read["ROM"][to]
                                except:
                                    pass
                                client.sendMessage(to, "Delete reading point:\n" + readTime)
                            else:
                                client.sendMessage(to, "Lurking belum diaktifkan ngapain di matikan?")
                        elif cmd == "lurking reset":
                            tz = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.now(tz=tz)
                            day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                            hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                            bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                            hr = timeNow.strftime("%A")
                            bln = timeNow.strftime("%m")
                            for i in range(len(day)):
                                if hr == day[i]: hasil = hari[i]
                            for k in range(0, len(bulan)):
                                if bln == str(k): bln = bulan[k-1]
                            readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                            if to in read["readPoint"]:
                                try:
                                    read["readPoint"][to] = True
                                    read["readMember"][to] = {}
                                    read["readTime"][to] = readTime
                                    read["ROM"][to] = {}
                                except:
                                    pass
                                client.sendMessage(to, "Reset reading point:\n" + readTime)
                            else:
                                client.sendMessage(to, "Lurking belum diaktifkan ngapain di reset?")
                        elif cmd == "lurking":
                            try:
                                if to not in read["readPoint"]:
                                    client.sendMessage(to, "Lurking has not been set.")
                                else:
                                    fm = "???[ Siders ]"
                                    reader = {}
                                    reader["name"] = ""
                                    if read["readMember"][to] == {}:
                                        reader["name"] += "\n? No readers"
                                    else:
                                        for a in read["readMember"][to]:
                                            reader["name"] += "\n? {}".format(str(read["readMember"][to][a]))
                                    time_ = read["readTime"][to]
                                    lm = "\n???[ Reader ]"
                                    lm += reader["name"]
                                    tota = len(read["readMember"][to]) - len(read["ROM"][to])
                                    totb = len(read["readMember"][to])
                                    lm += "\n???[ Total {} Siders From {} Viewers ]".format(str(tota), str(totb))
                                    lm += "\nPoint Set On : \n{}".format(str(time_))
                                    mentionSiders(to, fm, lm)
                            except Exception as error:
                                logError(error)
                        elif cmd.startswith("spamtag ") and sender == clientMID:
                            text_ = removeCmd("spamtag", text)
                            cond = text_.split(" ")
                            text = text_.replace(cond[0] + " ", "")
                            jml = int(cond[0])
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    text = text.replace("@{}".format(str(contact.displayName)),"")
                                if "|" in text:
                                    cond = text.split("|")
                                    fm = cond[0]
                                    lm = cond[1]
                                else:
                                    fm = ""
                                    lm = text
                                for ls in lists:
                                    for x in range(jml):
                                        sendMention(to, ls, str(fm), str(lm))
                                client.sendMessage(to, "Berhasil tag {} user dengan total {} tag".format(str(len(lists)), str(jml)))
                                return
                            else:
                                client.sendMessage(to, "Tidak ada user yang di tag")
                                return
                        elif cmd.startswith("spam ") and sender == clientMID:
                            text = removeCmd("spam", text)
                            cond = text.split(" ")
                            if len(cond) > 2:
                                total = int(cond[0])
                                status = cond[1]
                                word = cond[2].split(" ")
                                word_ = word
                                if status.lower() == "off":
                                    ret_ = "[ Spam ]"
                                    for wo in range(total):
                                        ret_ += "\n{}".format(str(random.choice(word_)))
                                    client.sendMessage(to, str(ret_))
                                elif status.lower() == "on":
                                    for wo in range(total):
                                        client.sendMessage(to, str(random.choice(word_)))
                                else:
                                    client.sendMessage(to, "Dibilangin jangan typo")
                            else:
                                client.sendMessage(to, "Dibilangin jangan typo")
                        elif cmd.startswith("addimage ") and sender == clientMID:
                            load()
                            name = removeCmd("addimage", text)
                            name = name.lower()
                            if name not in images:
                                settings["addImage"]["status"] = True
                                settings["addImage"]["name"] = str(name.lower())
                                images[str(name.lower())] = ""
                                f = codecs.open('image.json','w','utf-8')
                                json.dump(images, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Silahkan kirim gambar yang ingin anda tambahkan")
                            else:
                                client.sendMessage(to, "Gambar sudah ada dalam list")
                        elif cmd.startswith("delimage ") and sender == clientMID:
                            load()
                            name = removeCmd("delimage", text)
                            name = name.lower()
                            if name in images:
                                client.deleteFile(images[str(name.lower())])
                                del images[str(name.lower())]
                                f = codecs.open('image.json','w','utf-8')
                                json.dump(images, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Berhasil menghapus gambar {}".format(str(name.lower())))
                            else:
                                client.sendMessage(to, "Gambar tidak ada dalam list")
                        elif cmd.startswith("changeimage ") and sender == clientMID:
                            load()
                            name = removeCmd("changeimage", text)
                            name = name.lower()
                            if name in images:
                                settings["addImage"]["status"] = True
                                settings["addImage"]["name"] = str(name.lower())
                                images[str(name.lower())] = ""
                                f = codecs.open('image.json','w','utf-8')
                                json.dump(images, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Silahkan kirim gambar yang ingin anda ubah")
                            else:
                                client.sendMessage(to, "Gambar tidak ada dalam list")
                        elif cmd == "listimage":
                            load()
                            ret_ = "???[ List Images ]"
                            for image in images:
                                ret_ += "\n? " + image.title()
                            ret_ += "\n???[ Total {} Images ]".format(str(len(images)))
                            client.sendMessage(to, ret_)
                        elif cmd.startswith("sendimage ") and sender == clientMID:
                            load()
                            text = removeCmd("sendimage", text)
                            cond = text.split(" ")
                            jml = int(cond[0])
                            imagename = text.replace(cond[0] + " ","").lower()
                            if imagename in images:
                                imgURL = images[imagename]
                            else:
                                client.sendMessage(to, "Gambar tidak ditemukan")
                                return
                            for x in range(jml):
                                client.sendImage(to, imgURL)
                        elif cmd.startswith("addsticker ") and sender == clientMID:
                            load()
                            name = removeCmd("addsticker", text)
                            name = name.lower()
                            if name not in stickers:
                                settings["addSticker"]["status"] = True
                                settings["addSticker"]["name"] = str(name.lower())
                                stickers[str(name.lower())] = {}
                                f = codecs.open('sticker.json','w','utf-8')
                                json.dump(stickers, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Silahkan kirim stiker yang ingin anda tambahkan")
                            else:
                                client.sendMessage(to, "Nama stiker sudah ada dalam list")
                        elif cmd.startswith("delsticker ") and sender == clientMID:
                            load()
                            name = removeCmd("delsticker", text)
                            name = name.lower()
                            if name in stickers:
                                del stickers[str(name.lower())]
                                f = codecs.open('sticker.json','w','utf-8')
                                json.dump(stickers, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Berhasil menghapus stiker {}".format(str(name.lower())))
                            else:
                                client.sendMessage(to, "Stiker tidak ada dalam list")
                        elif cmd.startswith("changesticker ") and sender == clientMID:
                            load()
                            name = removeCmd("changesticker", text)
                            name = name.lower()
                            if name in stickers:
                                settings["addSticker"]["status"] = True
                                settings["addSticker"]["name"] = str(name.lower())
                                stickers[str(name.lower())] = ""
                                f = codecs.open('sticker.json','w','utf-8')
                                json.dump(stickers, f, sort_keys=True, indent=4, ensure_ascii=False)
                                client.sendMessage(to, "Silahkan kirim stiker yang ingin anda ubah")
                            else:
                                client.sendMessage(to, "Stiker tidak ada dalam list")
                        elif cmd == "liststicker":
                            load()
                            ret_ = "???[ List Sticker ]"
                            for sticker in stickers:
                                ret_ += "\n? " + sticker.title()
                            ret_ += "\n???[ Total {} Stickers ]".format(str(len(stickers)))
                            client.sendMessage(to, ret_)
                        elif cmd.startswith("sendsticker ") and sender == clientMID:
                            load()
                            text = removeCmd("sendsticker", text)
                            cond = text.split(" ")
                            jml = int(cond[0])
                            stickername = text.replace(cond[0] + " ","").lower()
                            if stickername in stickers:
                                sid = stickers[stickername]["STKID"]
                                spkg = stickers[stickername]["STKPKGID"]
                                sver = stickers[stickername]["STKVER"]
                            else:
                                return
                            for x in range(jml):
                                sendSticker(to, sver, spkg, sid)
                        elif cmd == "friendlist" and sender == clientMID:
                            contactlist = client.getAllContactIds()
                            kontak = client.getContacts(contactlist)
                            num=1
                            msgs="???[ List Friends ]"
                            for ids in kontak:
                                msgs+="\n? %i. %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\n???[ Total Friend : %i ]" % len(kontak)
                            client.sendMessage(to, msgs)
                        elif cmd.startswith("friendinfo "):
                            number = removeCmd("friendinfo", text)
                            contactlist = client.getAllContactIds()
                            try:
                                contact = contactlist[int(number)-1]
                                friend = client.getContact(contact)
                                cu = client.getProfileCoverURL(contact)
                                path = str(cu)
                                image = "http://dl.profile.line-cdn.net/" + friend.pictureStatus
                                try:
                                    client.sendMessage(to, "???[ Friends Info ]" + "? Nama : " + friend.displayName + "\n? Bio : " + friend.statusMessage + "\n? Mid : " + friend.mid)
                                    client.sendImageWithURL(to,image)
                                    client.sendImageWithURL(to,path)
                                except:
                                    pass
                            except:
                                pass
                        elif cmd == "blocklist" and sender == clientMID:
                            blockedlist = client.getBlockedContactIds()
                            kontak = client.getContacts(blockedlist)
                            num=1
                            msgs="???[ List Blocked ]"
                            for ids in kontak:
                                msgs+="\n? %i. %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\n???[ Total Blocked : %i ]" % len(kontak)
                            client.sendMessage(to, msgs)
                        elif cmd == "grouplist" and sender == clientMID:
                            groups = client.groups
                            ret_ = "???[ Group List ]"
                            no = 0 + 1
                            for gid in groups:
                                group = client.getGroup(gid)
                                ret_ += "\n? {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                no += 1
                            ret_ += "\n???[ Total {} Groups ]".format(str(len(groups)))
                            client.sendMessage(to, str(ret_))
                        elif cmd.startswith("memberlist "):
                            number = removeCmd("memberlist", text)
                            groups = client.getGroupIdsJoined()
                            ret_ = ""
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                no = 0
                                ret_ = "\n???[ Member List ]"
                                for mem in G.members:
                                    no += 1
                                    ret_ += "\n" "? "+ str(no) + ". " + mem.displayName
                                client.sendMessage(to,"???[ Group Name ]\n? "+ str(G.name) + ret_ + "\n???[ Total : %i Members ]" % len(G.members))
                            except:
                                pass
                        elif cmd == "listpending":
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                ret_ = "???[ Pending List ]"
                                no = 0 + 1
                                if group.invitee is None or group.invitee == []:
                                    client.sendMessage(to, "Tidak ada pendingan")
                                    return
                                else:
                                    for pen in group.invitee:
                                        ret_ += "\n? {}. {}".format(str(no), str(pen.displayName))
                                        no += 1
                                    ret_ += "\n???[ Total {} ]".format(str(len(group.invitee)))
                                    client.sendMessage(to, str(ret_))
                        elif cmd.startswith("pendinglist "):
                            if msg.toType == 2:
                                number = removeCmd("pendinglist", text)
                                groups = client.getGroupIdsJoined()
                                ret_ = "???[ Pending List ]"
                                no = 0 + 1
                                try:
                                    group = groups[int(number)-1]
                                    G = client.getGroup(group)
                                    if G.invitee is None or G.invitee == []:
                                        client.sendMessage(to, "Tidak ada pendingan")
                                        return
                                    else:
                                        for pen in G.invitee:
                                            ret_ += "\n? {}. {}".format(str(no), str(pen.displayName))
                                            no += 1
                                        ret_ += "\n???[ Total {} ]".format(str(len(G.invitee)))
                                        client.sendMessage(to, str(ret_))
                                except:
                                    pass
                        elif cmd == "rejectall" and sender == clientMID:
                            ginvited = client.getGroupIdsInvited()
                            if ginvited != [] and ginvited != None:
                                for gid in ginvited:
                                    client.rejectGroupInvitation(gid)
                                client.sendMessage(to, "Berhasil tolak sebanyak {} undangan".format(str(len(ginvited))))
                            else:
                                client.sendMessage(to, "Tidak ada undangan yang tertunda")
                        elif cmd == "cancelall" and sender == clientMID:
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                if group.invitee is None or group.invitee == []:
                                    client.sendMessage(to, "Tidak ada pendingan")
                                else:
                                    invitee = [contact.mid for contact in group.invitee]
                                    for inv in invitee:
                                        client.cancelGroupInvitation(to, [inv])
                                        time.sleep(1)
                                    client.sendMessage(to, "Berhasil membersihkan {} pendingan".format(str(len(invitee))))
                        elif cmd == "groupinfo":
                            if msg.toType != 2: return
                            group = client.getGroup(to)
                            try:
                                gCreator = group.creator.displayName
                            except:
                                gCreator = "Tidak ditemukan"
                            if group.invitee is None:
                                gPending = "0"
                            else:
                                gPending = str(len(group.invitee))
                            if group.preventedJoinByTicket == True:
                                gQr = "Tertutup"
                                gTicket = "Tidak ada"
                            else:
                                gQr = "Terbuka"
                                gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
                            timeCreated = time.strftime("%d-%m-%Y", time.localtime(int(group.createdTime) / 1000))
                            path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                            ret_ = "???[ Group Information ]"
                            ret_ += "\n? Name Group : {}".format(group.name)
                            ret_ += "\n? ID Group : {}".format(group.id)
                            ret_ += "\n? Creator Group : {}".format(gCreator)
                            ret_ += "\n? Group Created : {}".format(str(timeCreated))
                            ret_ += "\n? Jumlah Member : {}".format(str(len(group.members)))
                            ret_ += "\n? Jumlah Pending : {}".format(gPending)
                            ret_ += "\n? Group QR : {}".format(gQr)
                            ret_ += "\n? Group URL : {}".format(gTicket)
                            ret_ += "\n???[ Success ]"
                            client.sendImageWithURL(to, path)
                            client.sendMessage(to, str(ret_))
                        elif cmd.startswith("groupinfo "):
                            number = removeCmd("groupinfo", text)
                            groups = client.getGroupIdsJoined()
                            ret_ = ""
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    gCreator = G.creator.displayName
                                except:
                                    gCreator = "Tidak ditemukan"
                                if G.invitee is None:
                                    gPending = "0"
                                else:
                                    gPending = str(len(G.invitee))
                                if G.preventedJoinByTicket == True:
                                    gQr = "Tertutup"
                                    gTicket = "Tidak ada"
                                else:
                                    gQr = "Terbuka"
                                    gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(G.id)))
                                timeCreated = time.strftime("%d-%m-%Y", time.localtime(int(group.createdTime) / 1000))
                                ret_ += "???[ Group Information ]"
                                ret_ += "\n? Nama Group : {}".format(G.name)
                                ret_ += "\n? ID Group : {}".format(G.id)
                                ret_ += "\n? Pembuat : {}".format(gCreator)
                                ret_ += "\n? Waktu Dibuat : {}".format(str(timeCreated))
                                ret_ += "\n? Jumlah Member : {}".format(str(len(G.members)))
                                ret_ += "\n? Jumlah Pending : {}".format(gPending)
                                ret_ += "\n? Group Qr : {}".format(gQr)
                                ret_ += "\n? Group Ticket : {}".format(gTicket)
                                ret_ += "\n???[ Success ]"
                                client.sendMessage(to, str(ret_))
                            except:
                                pass
                        elif cmd == "listmember":
                            if msg.toType != 2: return
                            kontak = client.getGroup(to)
                            group = kontak.members
                            num=1
                            msgs="???[ List Member ]"
                            for ids in group:
                                msgs+="\n? %i. %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\n???[ Total Members : %i ]" % len(group)
                            client.sendMessage(to, msgs)
                        elif cmd == "grouppicture":
                            if msg.toType != 2: return
                            group = client.getGroup(to)
                            path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                            client.sendImageWithURL(to, path)
                        elif cmd == "groupname":
                            if msg.toType != 2: return
                            gid = client.getGroup(to)
                            client.sendMessage(to, "[Nama Group : ]\n" + gid.name)
                        elif cmd == "groupid":
                            if msg.toType != 2: return
                            gid = client.getGroup(to)
                            client.sendMessage(to, "[ ID Group ]\n" + gid.id)
                        elif cmd == "groupticket":
                            if msg.toType == 2:
                                g = client.getGroup(to)
                                if g.preventedJoinByTicket == True:
                                    g.preventedJoinByTicket = False
                                    client.updateGroup(g)
                                gurl = client.reissueGroupTicket(to)
                                client.sendMessage(msg.to,"line://ti/g/" + gurl)
                        elif cmd == "openqr":
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                group.preventedJoinByTicket = False
                                client.updateGroup(group)
                                gurl = client.reissueGroupTicket(to)
                                client.sendMessage(msg.to,"QR Group open\n\n" + "Link : line://ti/g/" + gurl)
                        elif cmd == "closeqr":
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                                client.sendMessage(msg.to,"QR Group close")
                        elif cmd == "groupcreator":
                            if msg.toType != 2: return
                            try:
                                group = client.getGroup(to)
                                GS = group.creator.mid
                                client.sendContact(to, GS)
                            except:
                                pass
                        elif cmd.startswith("changegroupname: "):
                            if msg.toType == 2:
                                X = client.getGroup(to)
                                X.name = removeCmd("changegroupname:", text)
                                client.updateGroup(X)
                        elif cmd.startswith("createannounce ") and sender == clientMID:
                            try:
                                txt = removeCmd("createannounce", text)
                                cond = txt.split("|")
                                if len(cond) == 1:
                                    link = "https://line.me/"
                                else:
                                    link = cond[1]
                                anu = ChatRoomAnnouncementContents()
                                anu.displayFields = 5
                                anu.text = cond[0]
                                anu.thumbnail = "http://brandmark.io/intro/info.png"
                                anu.link = link
                                client.createChatRoomAnnouncement(receiver, 0, anu)
                                client.sendMessage(to, "Success create announce")
                            except Exception as e:
                                client.sendMessage(to,str(e))
                        elif cmd.startswith("abroadcast ") and sender == clientMID:
                            try:
                                txt = removeCmd("abroadcast", text)
                                cond = txt.split("|")
                                if len(cond) == 1:
                                    link = "https://line.me/"
                                else:
                                    link = cond[1]
                                s = client.getGroupIdsJoined()
                                anu = ChatRoomAnnouncementContents()
                                anu.displayFields = 5
                                anu.text = cond[0]
                                anu.thumbnail = "http://brandmark.io/intro/info.png"
                                anu.link = link
                                for hmm in s:
                                    client.createChatRoomAnnouncement(hmm, 0, anu)
                                client.sendMessage(to, "Success Announce to All Group")
                            except Exception as e:
                                client.sendMessage(to,str(e))
                        elif cmd.startswith("gbroadcast ") and sender == clientMID:
                            txt = removeCmd("gbroadcast", text)
                            groups = client.getGroupIdsJoined()
                            for group in groups:
                                client.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
                                time.sleep(1)
                            client.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))
                        elif cmd.startswith("fbroadcast ") and sender == clientMID:
                            txt = removeCmd("fbroadcast", text)
                            friends = client.getAllContactIds()
                            for friend in friends:
                                client.sendMessage(friend, "[ Broadcast ]\n{}".format(str(txt)))
                                time.sleep(1)
                            client.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(friends))))
                        elif cmd.startswith("allbroadcast ") and sender == clientMID:
                            txt = removeCmd("allbroadcast", text)
                            friends = client.getAllContactIds()
                            groups = client.getGroupIdsJoined()
                            for group in groups:
                                client.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
                                time.sleep(1)
                            client.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))
                            for friend in friends:
                                client.sendMessage(friend, "[ Broadcast ]\n{}".format(str(txt)))
                                time.sleep(1)
                            client.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(friends))))
                        elif cmd.startswith("invitegroupcall ") and sender == clientMID:
                            if msg.toType == 2:
                                strnum = removeCmd("invitegroupcall", text)
                                num = int(strnum)
                                client.sendMessage(to, "Berhasil mengundang kedalam telponan group")
                                for var in range(0,num):
                                    group = client.getGroup(to)
                                    members = [mem.mid for mem in group.members]
                                    client.acquireGroupCallRoute(to)
                                    client.inviteIntoGroupCall(to, contactIds=members)
                        elif cmd.startswith("invitegroupvideocall ") and sender == clientMID:
                            if msg.toType == 2:
                                strnum = removeCmd("invitegroupvideocall", text)
                                num = int(strnum)
                                client.sendMessage(to, "Berhasil mengundang kedalam telponan group")
                                for var in range(0,num):
                                    group = client.getGroup(to)
                                    members = [mem.mid for mem in group.members]
                                    client.acquireGroupVideoCallRoute(to)
                                    client.inviteIntoGroupVideoCall(to, contactIds=members)
                        elif cmd == "getsquare"  and sender == clientMID:
                            try:
                                a = client.getJoinedSquares()
                                squares = a.squares
                                members = a.members
                                authorities = a.authorities
                                statuses = a.statuses
                                noteStatuses = a.noteStatuses
                                txt = str(squares)+'\n\n'+str(members)+'\n\n'+str(authorities)+'\n\n'+str(statuses)+'\n\n'+str(noteStatuses)+'\n\n'
                                txt2 = ''
                                for i in range(len(squares)):
                                    txt2 += str(i+1)+'. '+str(squares[i].invitationURL)+'\n'
                                client.sendMessage(to, txt2)
                            except Exception as e:
                            	client.sendMessage(to, str(e))
                        elif cmd == "getannounce":
                            gett = client.getChatRoomAnnouncements(receiver)
                            for a in gett:
                                aa = client.getContact(a.creatorMid).displayName
                                bb = a.contents
                                cc = bb.link
                                textt = bb.text
                                client.sendMessage(to, 'Link: ' + str(cc) + '\nText: ' + str(textt) + '\nMaker: ' + str(aa))
                        elif cmd == "about":
                            try:
                                arr = []
                                zero = "udd76b08e9178df926daf94371e9015f1"
                                creator2 = client.getContact(zero)
                                h = client.getContact(clientMID)
                                groups = client.getGroupIdsJoined()
                                contactlist = client.getAllContactIds()
                                kontak = client.getContacts(contactlist)
                                blockedlist = client.getBlockedContactIds()
                                kontak2 = client.getContacts(blockedlist)
                                ret_ = "???[ About Self ]"
                                ret_ += "\n? Client : {}".format(h.displayName)
                                ret_ += "\n? Group : {}".format(str(len(groups)))
                                ret_ += "\n? Friend : {}".format(str(len(kontak)))
                                ret_ += "\n? Blocked : {}".format(str(len(kontak2)))
                                ret_ += "\n???[ About Selfbot ]"
                                ret_ += "\n? Type : Selfbot by HelloWorld"
                                ret_ += "\n? Version : 3.0.8+ by linepy"
                                ret_ += "\n???[ Creator ]"
                                ret_ += "\n? - {}".format(creator2.displayName)
                                ret_ += "\n???[ Finish ]"
                                client.sendMessage(to, str(ret_))
                            except Exception as e:
                                client.sendMessage(msg.to, str(e))
                        elif cmd == "status":
                            try:
                                ret_ = "???[ Status ]"
                                groups = client.getGroupIdsJoined()
                                if settings["setKey"] == True: ret_ += "\n? Set Key : ON"
                                else: ret_ += "\n? Set Key : OFF"
                                if settings["autoAdd"] == True: ret_ += "\n? Auto Add : ONN"
                                else: ret_ += "\n? Auto Add : OFF"
                                if settings["autoJoin"] == True: ret_ += "\n? Auto Join : ON"
                                else: ret_ += "\n? Auto Join : OFF"
                                if settings["autoLeave"] == True: ret_ += "\n? Auto Leave Room : ON"
                                else: ret_ += "\n? Auto Leave Room : OFF"
                                if settings["autoJoinTicket"] == True: ret_ += "\n? Auto Join Ticket : ON"
                                else: ret_ += "\n? Auto Join Ticket : OFF"
                                if settings["autoRead"] == True: ret_ += "\n? Auto Read : ON"
                                else: ret_ += "\n? Auto Read : OFF"
                                if settings["autoReply"] == True: ret_ += "\n? Auto Reply : ON"
                                else: ret_ += "\n? Auto Reply : OFF"
                                if settings["autoRestart"] == True: ret_ += "\n? Auto Restart : ON"
                                else: ret_ += "\n? Auto Restart : OFF"
                                if settings["checkContact"] == True: ret_ += "\n? Check Contact : ON"
                                else: ret_ += "\n? Check Contact : OFF"
                                if settings["checkPost"] == True: ret_ += "\n? Check Post : ON"
                                else: ret_ += "\n? Check Post : OFF"
                                if settings["checkSticker"] == True: ret_ += "\n? Check Sticker : ON"
                                else: ret_ += "\n? Check Sticker : OFF"
                                if settings["detectMention"] == True: ret_ += "\n? Detect Mention : ON"
                                else: ret_ += "\n? Detect Mention : OFF"
                                if settings["responGc"] == True: ret_ += "\n? Respon Group Call : ON"
                                else: ret_ += "\n? Respon Group Call : OFF"
                                if settings["leaveMessage"] == True: ret_ += "\n? Leave Message : ON"
                                else: ret_ += "\n? Leave Message : OFF"
                                if settings["welcomeMessage"] == True: ret_ += "\n? Welcome Message : ON"
                                else: ret_ += "\n? Welcome Message : OFF"
                                if settings["protectGroupName"] == True: ret_ += "\n? Lock Group Name : ON"
                                else: ret_ += "\n? Lock Group Name : OFF"
                                if settings["protectGroupQr"] == True: ret_ += "\n? Lock Group Qr : ON"
                                else: ret_ += "\n? Lock Group Qr : OFF"
                                ret_ += "\n???[ Status ]"
                                client.sendMessage(to, str(ret_))
                            except Exception as e:
                                client.sendMessage(msg.to, str(e))
                        # Example remote command
                        elif cmd == "autoadd on" and sender == clientMID:
                            settings["autoAdd"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto add")
                        elif cmd == "autoadd off" and sender == clientMID:
                            settings["autoAdd"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto add")
                        elif cmd == "autojoin on" and sender == clientMID:
                            settings["autoJoin"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto join")
                        elif cmd == "autojoin off" and sender == clientMID:
                            settings["autoJoin"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto join")
                        elif cmd == "autoleave on" and sender == clientMID:
                            settings["autoLeave"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto leave")
                        elif cmd == "autoleave off" and sender == clientMID:
                            settings["autoLeave"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto leave")
                        elif cmd == "detectmention on" and sender == clientMID:
                            settings["detectMention"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto respon mention")
                        elif cmd == "detectmention off" and sender == clientMID:
                            settings["detectMention"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto respon mention")
                        elif cmd == "autojointicket on" and sender == clientMID:
                            settings["autoJoinTicket"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto join ticket")
                        elif cmd == "autojointicket off" and sender == clientMID:
                            settings["autoJoinTicket"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto join ticket")
                        elif cmd == "checkcontact on" and sender == clientMID:
                            settings["checkContact"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan cek detail kontak")
                        elif cmd == "checkcontact off" and sender == clientMID:
                            settings["checkContact"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan cek detail kontak")
                        elif cmd == "checkpost on" and sender == clientMID:
                            settings["checkPost"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan cek detail post")
                        elif cmd == "checkpost off" and sender == clientMID:
                            settings["checkPost"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan cek detail post")
                        elif cmd == "checksticker on" and sender == clientMID:
                            settings["checkSticker"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan cek sticker")
                        elif cmd == "checksticker off" and sender == clientMID:
                            settings["checkSticker"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan cek sticker")
                        elif cmd == "autoread on" and sender == clientMID:
                            settings["autoRead"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan auto read")
                        elif cmd == "autoread off" and sender == clientMID:
                            settings["autoRead"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan auto read")
                        elif cmd == "respongroupcall on" and sender == clientMID:
                            settings["responGc"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan Respon GroupCall")
                        elif cmd == "respongroupcall off" and sender == clientMID:
                            settings["responGc"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan Respon GroupCall")
                        elif cmd == "leavemessage on" and sender == clientMID:
                            settings["leaveMessage"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan Leave Message")
                        elif cmd == "leavemessage off" and sender == clientMID:
                            settings["leaveMessage"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan Leave Message")
                        elif cmd == "welcomemessage on" and sender == clientMID:
                            settings["welcomeMessage"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan Welcome Message")
                        elif cmd == "welcomemessage off" and sender == clientMID:
                            settings["welcomeMessage"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan Welcome Message")
                        elif cmd == "autoreply on" and sender == clientMID:
                            settings["autoReply"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan Auto Reply")
                        elif cmd == "autoreply off" and sender == clientMID:
                            settings["autoReply"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan Auto Reply")
                        elif cmd == "autorestart on" and sender == clientMID:
                            settings["autoRestart"] = True
                            client.sendMessage(to, "Berhasil mengaktifkan Auto Restart")
                        elif cmd == "autorestart off" and sender == clientMID:
                            settings["autoRestart"] = False
                            client.sendMessage(to, "Berhasil menonaktifkan Auto Restart")
                        elif cmd == "getreader on" and sender == clientMID:
                            settings["getReader"][receiver] = []
                            client.sendMessage(to, "Berhasil mengaktifkan Get Reader")
                        elif cmd == "getreader off" and sender == clientMID:
                            if receiver in settings["getReader"]:
                                del settings["getReader"][receiver]
                                client.sendMessage(to, "Berhasil menonaktifkan Get Reader")
                        elif cmd == "autoreply" and sender == clientMID:
                            if settings["replyPesan"] is not None:
                                client.sendMessage(to,"My Set AutoRespon : " + str(settings["replyPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["replySticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set AutoRespon : No messages are set")
                        elif cmd == "autoreplysticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "replySticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "delautoreplysticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["replySticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setautoreply: ") and sender == clientMID:
                            text_ = removeCmd("setautoreply:", text)
                            try:
                                settings["replyPesan"] = text_
                                client.sendMessage(to,"?AutoReply?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?AutoReply?\nFailed to replace message")
                        elif cmd == "detectmention" and sender == clientMID:
                            if settings["mentionPesan"] is not None:
                                client.sendMessage(to,"My Set DetectMention : " + str(settings["mentionPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["mentionSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set DetectMention : No messages are set")
                        elif cmd == "detectmentionsticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "mentionSticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "deldetectmentionsticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["mentionSticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setdetectmention: ") and sender == clientMID:
                            text_ = removeCmd("setdetectmention:", text)
                            try:
                                settings["mentionPesan"] = text_
                                client.sendMessage(to,"?DetectMention?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?DetectMention?\nFailed to replace message")
                        elif cmd == "leavemessage" and sender == clientMID:
                            if settings["leavePesan"] is not None:
                                client.sendMessage(to,"My Set LeaveMessage : " + str(settings["leavePesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set LeaveMessage : No messages are set")
                        elif cmd == "leavesticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "leaveSticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "delleavesticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["leaveSticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setleavemessage: ") and sender == clientMID:
                            text_ = removeCmd("setleavemessage:", text)
                            try:
                                settings["leavePesan"] = text_
                                client.sendMessage(to,"?LeaveMessage?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?LeaveMessage?\nFailed to replace message")
                        elif cmd == "welcomemessage" and sender == clientMID:
                            if settings["welcomePesan"] is not None:
                                client.sendMessage(to,"My Set WelcomeMessage : " + str(settings["welcomePesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["welcomeSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set WelcomeMessage : No messages are set")
                        elif cmd == "welcomesticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "welcomeSticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "delwelcomesticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["welcomeSticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setwelcomemessage: ") and sender == clientMID:
                            text_ = removeCmd("setwelcomemessage:", text)
                            try:
                                settings["welcomePesan"] = text_
                                client.sendMessage(to,"?WelcomeMessage?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?WelcomeMessage?\nFailed to replace message")
                        elif cmd == "autoadd" and sender == clientMID:
                            if settings["addPesan"] is not None:
                                client.sendMessage(to,"My Set AutoAdd : " + str(settings["addPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["addSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set AutoAdd : No messages are set")
                        elif cmd == "autoaddsticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "addSticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "delautoaddsticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["addSticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setautoadd: ") and sender == clientMID:
                            text_ = removeCmd("setautoadd:", text)
                            try:
                                settings["addPesan"] = text_
                                client.sendMessage(to,"?AutoAdd?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?AutoAdd?\nFailed to replace message")
                        elif cmd == "getreader" and sender == clientMID:
                            if settings["readerPesan"] is not None:
                                client.sendMessage(to,"My Set GetReader : " + str(settings["readerPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["readerSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set GetReader : No messages are set")
                        elif cmd == "getreadersticker" and sender == clientMID:
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "readerSticker"
                            client.sendMessage(to, "Silahkan kirim stiker yang ingin anda pakai")
                        elif cmd == "delgetreadersticker" and sender == clientMID:
                            settings["messageSticker"]["listSticker"]["readerSticker"] = None
                            client.sendMessage(to, "Berhasil mengahapus stiker")
                        elif cmd.startswith("setgetreader: ") and sender == clientMID:
                            text_ = removeCmd("setgetreader:", text)
                            try:
                                settings["readerPesan"] = text_
                                client.sendMessage(to,"?GetReader?Changed to : " + text_)
                            except:
                                client.sendMessage(to,"?GetReader?\nFailed to replace message")
                        elif cmd == "lockgroupname" and sender == clientMID:
                            if settings["protectGroupName"] == True:
                                client.sendMessage(to,"Kunci nama group telah di aktif")
                            else:
                                settings["protectGroupName"] = True
                                client.sendMessage(to,"Berhasil mengaktifkan kunci nama group")
                        elif cmd == "unlockgroupname" and sender == clientMID:
                            if settings["protectGroupName"] == False:
                                client.sendMessage(to,"Mengunci nama group telah di nonaktifkan")
                            else:
                                settings["protectGroupName"] = False
                                client.sendMessage(to,"Berhasil menonaktifkan kunci nama group")
                        elif cmd == "backupgroupname" and sender == clientMID:
                            G = client.getGroupIdsJoined()
                            for gid in G:
                                group = client.getGroup(gid)
                                groupName[gid] = group.name
                            client.sendMessage(to,"Berhasil backup semua nama group")
                        elif cmd == "lockgroupqr" and sender == clientMID:
                            if settings["protectGroupQr"] == True:
                                client.sendMessage(to,"Kunci qr group telah di aktifkan")
                            else:
                                settings["protectGroupQr"] = True
                                client.sendMessage(to,"Berhasil mengaktifkan kunci qr group")
                        elif cmd == "unlockgroupqr" and sender == clientMID:
                            if settings["protectGroupQr"] == False:
                                client.sendMessage(to,"kunci qr group telah di nonaktifkan")
                            else:
                                settings["protectGroupQr"] = False
                                client.sendMessage(to,"Berhasil menonaktifkan kunci qr group")
                        elif cmd == "mute":
                            if sender in clientMID or sender in settings["admin"]:
                                if to not in settings["botMute"]:
                                    settings["botMute"].append(to)
                                    client.sendMessage(to, "Berhasil menonaktifkan bot pada ruangan ini")
                            else:
                                if to not in settings["botOff"]:
                                    settings["botOff"].append(to)
                                    client.sendMessage(to, "Berhasil menonaktifkan bot pada ruangan ini")
                    if text.lower() == "mykey":
                        client.sendMessage(to,"My Set Keyword :?" + str(settings["keyCommand"]) + "?\nSetkey : " + str(settings['setKey']))
                    elif text.lower() == "setkey on" and sender == clientMID:
                        settings["setKey"] = True
                        client.sendMessage(to, "Berhasil mengaktifkan setkey")
                    elif text.lower() == "setkey off" and sender == clientMID:
                        settings["setKey"] = False
                        client.sendMessage(to, "Berhasil menonaktifkan setkey")
                    if cmd == "unmute":
                        if sender in clientMID or sender in settings["admin"]:
                            if to in settings["botMute"] or to in settings["botOff"]:
                                if to in settings["botMute"]:
                                    settings["botMute"].remove(to)
                                if to in settings["botOff"]:
                                    settings["botOff"].remove(to)
                                client.sendMessage(to, "Berhasil mengaktifkan bot pada ruangan ini")
                            else:
                                client.sendMessage(to, "Bot telah diaktifkan pada ruangan ini")
                        else:
                            if to in settings["botOff"] and to not in settings["botMute"]:
                                settings["botOff"].remove(to)
                                client.sendMessage(to, "Berhasil mengaktifkan bot pada ruangan ini")
                            else:
                                client.sendMessage(to, "Gagal mengaktifkan bot, hubungi admin untuk mengaktifkan")
                    if "/ti/g/" in text.lower():
                        if settings["autoJoinTicket"] == True:
                            link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                            links = link_re.findall(text)
                            n_links = []
                            for l in links:
                                if l not in n_links:
                                   n_links.append(l)
                            for ticket_id in n_links:
                                group = client.findGroupByTicket(ticket_id)
                                client.acceptGroupInvitationByTicket(group.id,ticket_id)
                                client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
                    for image in images:
                        if text.lower() == image:
                            client.sendImage(to, images[image])
                    for sticker in stickers:
                        if text.lower() == sticker:
                            sid = stickers[sticker]["STKID"]
                            spkg = stickers[sticker]["STKPKGID"]
                            sver = stickers[sticker]["STKVER"]
                            sendSticker(to, sver, spkg, sid)
                elif msg.contentType == 1:
                    if settings["changePicture"] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id, saveAs="tmp/pict.bin")
                        settings["changePicture"] = False
                        client.updateProfilePicture(path)
                        client.sendMessage(to, "Berhasil mengubah foto profile")
                    if settings["changeCover"] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id, saveAs="tmp/cover.bin")
                        settings['changeProfileCover'] = path
                        settings["changeCover"] = False
                        cover = str(settings["changeProfileCover"])
                        client.updateProfileCoverById(cover)
                        client.sendMessage(to, "Berhasil mengubah foto cover")
                    if settings['changeProfileVideo']['status'] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id, saveAs="tmp/pict.bin")
                        if settings['changeProfileVideo']['stage'] == 1:
                            settings['changeProfileVideo']['picture'] = path
                            client.sendMessage(to, "Silahkan kirimkan video yang ingin anda jadikan profile")
                            settings['changeProfileVideo']['stage'] = 2
                        elif settings['changeProfileVideo']['stage'] == 2:
                            settings['changeProfileVideo']['picture'] = path
                            changeProfileVideo(to)
                            client.sendMessage(to, "Berhasil mengubah video profile")
                    if settings["addImage"]["status"] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id)
                        images[settings["addImage"]["name"]] = str(path)
                        f = codecs.open("image.json","w","utf-8")
                        json.dump(images, f, sort_keys=True, indent=4, ensure_ascii=False)
                        client.sendMessage(to, "Berhasil menambahkan gambar {}".format(str(settings["addImage"]["name"])))
                        settings["addImage"]["status"] = False
                        settings["addImage"]["name"] = ""
                    if msg.toType == 2:
                        if to in settings["changeGroupPicture"]:
                            path = client.downloadObjectMsg(msg_id, saveAs="tmp/video.bin")
                            settings["changeGroupPicture"].remove(to)
                            client.updateGroupPicture(to, path)
                            client.sendMessage(to, "Berhasil mengubah foto group")
                elif msg.contentType == 2:
                    if settings['changeProfileVideo']['status'] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id)
                        if settings['changeProfileVideo']['stage'] == 1:
                            settings['changeProfileVideo']['video'] = path
                            client.sendMessage(to, "Silahkan kirimkan picture yang ingin anda jadikan profile")
                            settings['changeProfileVideo']['stage'] = 2
                        elif settings['changeProfileVideo']['stage'] == 2:
                            settings['changeProfileVideo']['video'] = path
                            changeProfileVideo(to)
                elif msg.contentType == 7:
                    if settings["messageSticker"]["addStatus"] == True and sender == clientMID:
                        name = settings["messageSticker"]["addName"]
                        if name != None and name in settings["messageSticker"]["listSticker"]:
                            settings["messageSticker"]["listSticker"][name] = {
                                "STKID": msg.contentMetadata["STKID"],
                                "STKVER": msg.contentMetadata["STKVER"],
                                "STKPKGID": msg.contentMetadata["STKPKGID"]
                            }
                            client.sendMessage(to, "Berhasil menambahkan " + name)
                        settings["messageSticker"]["addStatus"] = False
                        settings["messageSticker"]["addName"] = None
                    if settings["addSticker"]["status"] == True and sender == clientMID:
                        stickers[settings["addSticker"]["name"]]["STKVER"] = msg.contentMetadata["STKVER"]
                        stickers[settings["addSticker"]["name"]]["STKID"] = msg.contentMetadata["STKID"]
                        stickers[settings["addSticker"]["name"]]["STKPKGID"] = msg.contentMetadata["STKPKGID"]
                        f = codecs.open('sticker.json','w','utf-8')
                        json.dump(stickers, f, sort_keys=True, indent=4, ensure_ascii=False)
                        client.sendMessage(to, "Berhasil menambahkan stiker {}".format(str(settings["addSticker"]["name"])))
                        settings["addSticker"]["status"] = False
                        settings["addSticker"]["name"] = ""
                    if settings["checkSticker"] == True and sender == clientMID:
                        stk_id = msg.contentMetadata['STKID']
                        stk_ver = msg.contentMetadata['STKVER']
                        pkg_id = msg.contentMetadata['STKPKGID']
                        ret_ = "???[ Sticker Info ]"
                        ret_ += "\n? Sticker ID : {}".format(stk_id)
                        ret_ += "\n? Sticker Packages ID : {}".format(pkg_id)
                        ret_ += "\n? Sticker Version : {}".format(stk_ver)
                        ret_ += "\n???[ Link Sticker ]"
                        ret_ += "\n? line://shop/detail/{}".format(pkg_id)
                        ret_ += "\n???[ Finish ]"
                        client.sendMessage(to, str(ret_))
                elif msg.contentType == 13:
                    if settings["checkContact"] == True:
                        try:
                            contact = client.getContact(msg.contentMetadata["mid"])
                            if client != None:
                                cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
                            else:
                                cover = "Tidak dapat masuk di line channel"
                            path = "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
                            try:
                                client.sendImageWithURL(to, str(path))
                            except:
                                pass
                            ret_ = "???[ Details Contact ]"
                            ret_ += "\n? Nama : {}".format(str(contact.displayName))
                            ret_ += "\n? MID : {}".format(str(msg.contentMetadata["mid"]))
                            ret_ += "\n? Bio : {}".format(str(contact.statusMessage))
                            ret_ += "\n? Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
                            ret_ += "\n? Gambar Cover : {}".format(str(cover))
                            ret_ += "\n???[ Finish ]"
                            client.sendMessage(to, str(ret_))
                        except:
                            client.sendMessage(to, "Kontak tidak valid")
                elif msg.contentType == 16:
                    if settings["checkPost"] == True:
                        try:
                            ret_ = "???[ Details Post ]"
                            if msg.contentMetadata["serviceType"] == "GB":
                                contact = client.getContact(sender)
                                auth = "\n? Penulis : {}".format(str(contact.displayName))
                            else:
                                auth = "\n? Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
                            purl = "\n? URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                            ret_ += auth
                            ret_ += purl
                            if "mediaOid" in msg.contentMetadata:
                                object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                                if msg.contentMetadata["mediaType"] == "V":
                                    if msg.contentMetadata["serviceType"] == "GB":
                                        ourl = "\n? Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                        murl = "\n? Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                    else:
                                        ourl = "\n? Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                        murl = "\n? Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                    ret_ += murl
                                else:
                                    if msg.contentMetadata["serviceType"] == "GB":
                                        ourl = "\n? Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                    else:
                                        ourl = "\n? Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                ret_ += ourl
                            if "stickerId" in msg.contentMetadata:
                                stck = "\n? Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
                                ret_ += stck
                            if "text" in msg.contentMetadata:
                                text = "\n? Tulisan : {}".format(str(msg.contentMetadata["text"]))
                                ret_ += text
                            ret_ += "\n???[ Finish ]"
                            client.sendMessage(to, str(ret_))
                        except:
                            client.sendMessage(to, "Post tidak valid")

        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            if op.param1 in settings["getReader"] and op.param2 not in settings["getReader"][op.param1]:
                msgSticker = settings["messageSticker"]["listSticker"]["readerSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                if "@!" in settings["readerPesan"]:
                    msg = settings["readerPesan"].split("@!")
                    sendMention(op.param1, op.param2, msg[0], msg[1])
                else:
                    sendMention(op.param1, op.param2, "Halo", settings["readerPesan"])
                settings["getReader"][op.param1].append(op.param2)
            if op.param1 in read["readPoint"]:
                _name = client.getContact(op.param2).displayName
                tz = pytz.timezone("Asia/Jakarta")
                timeNow = datetime.now(tz=tz)
                timeHours = datetime.strftime(timeNow," (%H:%M)")
                read["readMember"][op.param1][op.param2] = str(_name) + str(timeHours)
        backupData()
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)

def run():
    while True:
        try:
            autoRestart()
            delExpire()
            ops = clientPoll.singleTrace(count=50)
            if ops != None:
                for op in ops:
                   loop.run_until_complete(clientBot(op))
                   #clientBot(op)
                   clientPoll.setRevision(op.revision)
        except Exception as e:
            logError(e)

if __name__ == "__main__":
    run()
