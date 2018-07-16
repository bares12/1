# -*- coding: utf-8 -*-

from LineAPI import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator

# Silahkan Edit Sesukamu
# Asalkan Rapih Dan Respon
# jika ingin login Via qr Ganti Saja
# Atau Login Via Email
# Jangan Lupa Add Creator 
# id Line ( unk87 )
#==============================================================================#
botStart = time.time()

unk = LINE()
#unk = LINE("token kamu")
#unk = LINE("Email","Password")
unk.log("Auth Token : " + str(unk.authToken))
channelToken = unk.getChannelResult()
unk.log("Channel Token : " + str(channelToken))

ais = LINE()
#ais = LINE("TOKEN KAMU")
#ais = LINE("Email","Password")
ais.log("Auth Token : " + str(ais.authToken))
channelToken = ais.getChannelResult()
ais.log("Channel Token : " + str(channelToken))

ki2 = LINE()
#ki2 = LINE("TOKEN KAMU")
#ki2 = LINE("Email","Password")
ki2.log("Auth Token : " + str(ki2.authToken))
channelToken = ki2.getChannelResult()
ki2.log("Channel Token : " + str(channelToken))

ki3 = LINE()
#ki3 = LINE("TOKEN KAMU")
#ki3 = LINE("Email","Password")
ki3.log("Auth Token : " + str(ki3.authToken))
channelToken = ki3.getChannelResult()
ki3.log("Channel Token : " + str(channelToken))

ki4 = LINE()
#ki4 = LINE("TOKEN KAMU")
#ki4 = LINE("Email","Password")
ki4.log("Auth Token : " + str(ki4.authToken))
channelToken = ki4.getChannelResult()
ki4.log("Channel Token : " + str(channelToken))

KAC = [unk,ais,ki2,ki3,ki4]
UNK = [ais,ki2,ki3,ki4] # ini jangan luh hapus peak.
#maksudnya agar bot sb/induk gak ikutan nge kick.
unkMID = unk.profile.mid
aisMID = ais.profile.mid
ki2MID = ki2.profile.mid
ki3MID = ki3.profile.mid
ki4MID = ki4.profile.mid
Bots = [unkMID,aisMID,ki2MID,ki3MID,ki4MID]
creator = ["ube187443474747c3ec352e7efeb48c1b"]
Owner = ["ube187443474747c3ec352e7efeb48c1b"]
admin = ["ube187443474747c3ec352e7efeb48c1b"]

unkProfile = unk.getProfile()
aisProfile = ais.getProfile()
ki2Profile = ki2.getProfile()
ki2Profile = ki3.getProfile()
ki2Profile = ki4.getProfile()

lineSettings = unk.getSettings()
aisSettings = ais.getSettings()
ki2Settings = ki2.getSettings()
ki2Settings = ki3.getSettings()
ki2Settings = ki4.getSettings()

oepoll = OEPoll(unk)
oepoll1 = OEPoll(ais)
oepoll2 = OEPoll(ki2)
oepoll3 = OEPoll(ki3)
oepoll4 = OEPoll(ki4)

responsename = unk.getProfile().displayName
responsename2 = ais.getProfile().displayName
responsename3 = ki2.getProfile().displayName
responsename2 = ki3.getProfile().displayName
responsename3 = ki4.getProfile().displayName
#==============================================================================#




with open('Owner.json', 'r') as fp:
    Owner = json.load(fp)
    
with open('admin.json', 'r') as fp:
    admin = json.load(fp)
    
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

myProfile["displayName"] = unkProfile.displayName
myProfile["statusMessage"] = unkProfile.statusMessage
myProfile["pictureStatus"] = unkProfile.pictureStatus

readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

#==============================================================================#

read = json.load(readOpen)
settings = json.load(settingsOpen)

def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def logError(text):
    unk.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        unk.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        
def helpmessage():
    helpMessage = " [ Help Message ]" + "\n" + \
                  "  " + "\n" + \
                  " Help1" + "\n" + \
                  " Help2" + "\n" + \
                  " Help3" + "\n" + \
                  " Help4" + "\n" + \
                  " Help Self" + "\n" + \
                  " Status" + "\n" + \
                  " Runtime" + "\n" + \
                  " About" + "\n" + \
                  "   "
    return helpMessage        
        
def helpmedia():
    helpMedia =   " [ Menu MyBot ]" + "\n" + \
                  "  " + "\n" + \
                  " Restart" + "\n" + \
                  " Join ( panggil bot ) " + "\n" + \
                  " Absen" + "\n" + \
                  " Kabur ( usir bot ) " + "\n" + \
                  " Kabur all ( kluar semua ) " + "\n" + \
                  " Respon ( cek semua bot )" + "\n" + \
                  " Sp" + "\n" + \
                  " Kick @" + "\n" + \
                  " Kickallmember" + "\n" + \
                  "   "
    return helpMedia

def helpmedia1():
    helpMedia1 =   " [ Owner's ]" + "\n" + \
                  "  " + "\n" + \
                  " OwnerList" + "\n" + \
                  " AdminList" + "\n" + \
                  " BanContact" + "\n" + \
                  " UnbanContact" + "\n" + \
                  " BanList" + "\n" + \
                  " Clearban" + "\n" + \
                  " Adminadd @" + "\n" + \
                  " Owneradd @" + "\n" + \
                  "  b"
    return helpMedia1

def helpmedia2():
    helpMedia2 =   "  [ Groups ]" + "\n" + \
                  " GroupCreator" + "\n" + \
                  " GroupId" + "\n" + \
                  " GroupName" + "\n" + \
                  " GroupPicture" + "\n" + \
                  " GroupList" + "\n" + \
                  " GroupMemberList" + "\n" + \
                  " GroupInfo" + "\n" + \
                  " Gticket" + "\n" + \
                  " Gticket on/off" + "\n" + \
                  " Mimic on" + "\n" + \
                  " Mimic off" + "\n" + \
                  " MimicAdd" + "\n" + \
                  " MimicDel" + "\n" + \
                  " Lurking on/off" + "\n" + \
                  " Lurking" + "\n" + \
                  " Tag" + "\n" + \
                  "   "
    return helpMedia2
    
def helptexttospeech():
    helpTextToSpeech =   "[ Menu Set ]" + "\n" + \
                  " Protect on/off" + "\n" + \
                  " QrProtect on/off" + "\n" + \
                  " InviteProtect on/off" + "\n" + \
                  " CancelProtect on/off" + "\n" + \
                  " AutoAdd on/off" + "\n" + \
                  " AutoJoin on/off" + "\n" + \
                  " AutoLeave on/off" + "\n" + \
                  " CheckSticker on/off" + "\n" + \
                  " AutoRead on/off" + "\n" + \
                  " DetectMention on/off" + "\n" + \
                  " Join link on/off" + "\n" + \
                  " Pro on/off" + "\n" + \
                  "  "
    return helpTextToSpeech
    
def helptranslate():
    helpTranslate =    " [ Help Self ]" + "\n" + \
                  "  " + "\n" + \
                  " Me" + "\n" + \
                  " MyMid" + "\n" + \
                  " Midnya @" + "\n" + \
                  " MyName" + "\n" + \
                  " MyBio" + "\n" + \
                  " MyPicture" + "\n" + \
                  " MyVideoProfile" + "\n" + \
                  " MyCover" + "\n" + \
                  " StealContact @" + "\n" + \
                  " StealMid @" + "\n" + \
                  " StealName「Mention」" + "\n" + \
                  " StealBio @" + "\n" + \
                  " StealPicture @" + "\n" + \
                  " StealVideoProfile @" + "\n" + \
                  " StealCover @" + "\n" + \
                  " CloneProfile @" + "\n" + \
                  " RestoreProfile" + "\n" + \
                  "   "
    return helpTranslate
#==============================================================================#
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
        
def command(text):
    pesan = text.lower()
    if pesan.startswith(settings["keyCommand"]):
        cmd = pesan.replace(settings["keyCommand"],"")
    else:
        cmd = "Undefined command"
    return cmd        


def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] UNK87 BOT SATU")
            return
#-------------------------------------------------------------------------------
        if op.type == 25:
            msg = op.message
            if msg.contentType == 13:
                if settings["wblack"] == True:
                    if msg.contentMetadata["mid"] in settings["commentBlack"]:
                        unk.sendMessage(msg.to,"sudah masuk daftar hitam")
                        settings["wblack"] = False
                    else:
                        settings["commentBlack"][msg.contentMetadata["mid"]] = True
                        settings["wblack"] = False
                        unk.sendMessage(msg.to,"Itu tidak berkomentar")
                elif settings["dblack"] == True:
                    if msg.contentMetadata["mid"] in settings["commentBlack"]:
                        del settings["commentBlack"][msg.contentMetadata["mid"]]
                        unk.sendMessage(msg.to,"Done")
                        settings["dblack"] = False
                    else:
                        settings["dblack"] = False
                        unk.sendMessage(msg.to,"Tidak ada dalam daftar hitam")
#-------------------------------------------------------------------------------
                elif settings["wblacklist"] == True:
                    if msg.contentMetadata["mid"] in settings["blacklist"]:
                        unk.sendMessage(msg.to,"sudah masuk daftar hitam")
                        settings["wblacklist"] = False
                    else:
                        settings["blacklist"][msg.contentMetadata["mid"]] = True
                        settings["wblacklist"] = False
                        unk.sendMessage(msg.to,"Done")
                        
                elif settings["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in settings["blacklist"]:
                        del settings["blacklist"][msg.contentMetadata["mid"]]
                        unk.sendMessage(msg.to,"Done")
                        settings["dblacklist"] = False
                    else:
                        settings["dblacklist"] = False
                        unk.sendMessage(msg.to,"Done")
                        
                       
#-------------------------------------------------------------------------------
        if op.type == 25:
            print ("[ 25 ] UNK87 BOT TIGA")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != unk.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    unk.sendMessage(to, str(helpMessage), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
                  #  unk.sendContact(to, "ud827b95f8468c46e30cf9bf5dd35e8e7")
             #   if text.lower() == 'token list':
            #        helpAdmin = helpadmin()
            #        unk.sendMessage(to, str(helpAdmin))    
                if text.lower() == 'help1':
                    helpMedia = helpmedia()
                    unk.sendMessage(to, str(helpMedia), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
  #                  unk.sendContact(to, "ud827b95f8468c46e30cf9bf5dd35e8e7")
 #                   unk.sendMessage(to,"isi pesanmu")
                if text.lower() == 'help3':
                    helpMedia1 = helpmedia1()
                    unk.sendMessage(to, str(helpMedia1), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
  #                  unk.sendContact(to, "ud827b95f8468c46e30cf9bf5dd35e8e7")
 #                   unk.sendMessage(to,"isi pesanmu")
                if text.lower() == 'help4':
                    helpMedia2 = helpmedia2()
                    unk.sendMessage(to, str(helpMedia2), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
  #                  unk.sendContact(to, "ud827b95f8468c46e30cf9bf5dd35e8e7")
 #                   unk.sendMessage(to,"isi pesanmu")
                elif text.lower() == 'help2':
                    helpTextToSpeech = helptexttospeech()
                    unk.sendMessage(to, str(helpTextToSpeech), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
  #                  unk.sendMessage(to, "isi pesanmu")
                elif text.lower() == 'help self':
                    helpTranslate = helptranslate()
                    unk.sendMessage(to, str(helpTranslate), contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+unk.getContact(unkMID).pictureStatus, 'AGENT_NAME': 'Creator', 'AGENT_LINK': 'https://bit.ly/2J3ywc3'})
    #                unk.sendMessage(to, "isi pesanmu")
#==============================================================================#
                elif text.lower() == 'sp':
                    start = time.time()
                    unk.sendMessage(to, "Cek Speed...")
                    elapsed_time = time.time() - start
                    unk.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':    
                    unk.sendMessage(to, "Please Wait...")
                    time.sleep(5)
                    unk.sendMessage(to, "Restart Sukses")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    unk.sendMessage(to, "Bot Aktif {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "ube187443474747c3ec352e7efeb48c1b"
                        creator = unk.getContact(owner)
                        contact = unk.getContact(unkMID)
                        grouplist = unk.getGroupIdsJoined()
                        contactlist = unk.getAllContactIds()
                        blockedlist = unk.getBlockedContactIds()
                        ret_ = "╔══[ About Bot ]"
                        ret_ += "\n╠ akun : {}".format(contact.displayName)
                        ret_ += "\n╠ group : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ teman : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ Blokir : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ About Selfbot ]"
                        ret_ += "\n╠ Version : Premium"
                        ret_ += "\n╠ Creator : {}".format(creator.displayName)
                        ret_ += "\n╚══[ About Bot ]"
                        unk.sendMessage(to, str(ret_))
                    except Exception as e:
                        unk.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'status':
                    try:
                        ret_ = "╔══[ Status ]"
                        if settings["protect"] == True: ret_ += "║ Protect ✅"
                        else: ret_ += "║  Protect ❌"
                        if settings["qrprotect"] == True: ret_ += "\n║ Qr Protect ✅"
                        else: ret_ += "\n║ Qr Protect ❌"
                        if settings["inviteprotect"] == True: ret_ += "\n║ Invite Protect ✅"
                        else: ret_ += "\n║ Invite Protect ❌"
                        if settings["cancelprotect"] == True: ret_ += "\n║ Cancel Protect ✅"
                        else: ret_ += "\n║ Cancel Protect ❌"
                        if settings["autoAdd"] == True: ret_ += "\n║ Auto Add ✅"
                        else: ret_ += "\n║ Auto Add ❌"
                        if settings["autoJoin"] == True: ret_ += "\n║ Auto Join ✅"
                        else: ret_ += "\n║ Auto Join ❌"
                        if settings["autoLeave"] == True: ret_ += "\n║ Auto Leave ✅"
                        else: ret_ += "\n║ Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n║ Auto Read ✅"
                        else: ret_ += "\n║ Auto Read ❌"
                        if settings["checkSticker"] == True: ret_ += "\n║ Check Sticker ✅"
                        else: ret_ += "\n║ Check Sticker ❌"
                        if settings["detectMention"] == True: ret_ += "\n║ Detect Mention ✅"
                        else: ret_ += "\n║ Detect Mention ❌"
                        ret_ += "\n╚══[ Status ]"
                        unk.sendMessage(to, str(ret_))
                    except Exception as e:
                        unk.sendMessage(msg.to, str(e))
                        
                elif msg.text.lower().startswith("spaminvite "):
                   #if msg._from in admin:
                    dan = text.split("|")
                    userid = dan[0]
                    namagrup = dan[0]
                    jumlah = int(dan[0])
                    grups = unk.groups
                    tgb = unk.findContactsByUserid(userid)
                    if jumlah <= 10000000:
                        for var in range(0,jumlah):
                            try:
                                unk.createGroup(str(namagrup), [tgb.mid])
                                for i in grups:
                                    grup = unk.getGroup(i)
                                    if grup.name == namagrup:
                                        unk.inviteIntoGroup(grup.id, [tgb.mid])
                                        unk.sendMessage(to, "@! sukses spam grup!\n\nkorban: @!\njumlah: {}\nnama grup: {}".format(jumlah, str(namagrup)), [sender, tgb.mid])
                            except Exception as Nigga:
                                unk.sendMessage(to, str(Nigga))
                            #else:
                                unk.sendMessage(to, "@! kebanyakan njer!!", [sender])
#-------------------------------------------------------------------------------
                elif msg.text.lower().startswith("owneradd "):
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                Owner[target] = True
                                f=codecs.open('Owner.json','w','utf-8')
                                json.dump(Owner, f, sort_keys=True, indent=4,ensure_ascii=False)
                                unk.sendMessage(msg.to,"Owner Di Tambahkan")
                            except:
                                pass
                    
                elif msg.text.lower().startswith("ownerdel "):
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                del Owner[target]
                                f=codecs.open('Owner.json','w','utf-8')
                                json.dump(Owner, f, sort_keys=True, indent=4,ensure_ascii=False)
                                unk.sendMessage(msg.to,"Owner Di Hapuskan")
                            except:
                                pass
#-------------------------------------------------------------------------------
                elif text.lower() == 'ownerlist':
                        if Owner == []:
                            unk.sendMessage(msg.to,"The Ownerlist is empty")
                        else:
                            unk.sendMessage(msg.to,"Tunggu...")
                            mc = "╔═══════════════"
                            for mi_d in admin:
                                mc += "╠ " +unk.getContact(mi_d).displayName + "\n"
                            unk.sendMessage(msg.to,mc + "╠═══════════════\n╠〘 line.me/ti/p/~situ.sehat 〙\n╚═══════════════")
#-------------------------------------------------------------------------------
                elif msg.text.lower().startswith("adminadd "):
                        targets = []
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                admin[target] = True
                                f=codecs.open('admin.json','w','utf-8')
                                json.dump(admin, f, sort_keys=True, indent=4,ensure_ascii=False)
                                unk.sendMessage(msg.to,"Admin Di Tambahkan")
                                break
                            except:
                                unk.sendMessage(msg.to,"Added Target Fail !")
                                break
                    
                elif msg.text.lower().startswith("admindel "):
                        targets = []
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            try:
                                del admin[target]
                                f=codecs.open('admin.json','w','utf-8')
                                json.dump(admin, f, sort_keys=True, indent=4,ensure_ascii=False)
                                unk.sendMessage(msg.to,"Admin Telah Di Hapus")
                                break
                            except:
                                unk.sendMessage(msg.to,"Deleted Target Fail !")
                            break
              #      else:
               #         unk.sendMessage(msg.to,"Owner Permission Required")
#-------------------------------------------------------------------------------
                elif text.lower() == 'adminlist':
                #    if msg._from in Owner:
                        if admin == []:
                            unk.sendMessage(msg.to,"The Adminlist is empty")
                        else:
                            unk.sendMessage(msg.to,"Tunggu...")
                            mc = "╔═══════════════"
                            for mi_d in admin:
                                mc += "╠ " +unk.getContact(mi_d).displayName + "\n"
                            unk.sendMessage(msg.to,mc + "╠═══════════════\n╠〘 line.me/ti/p/~situ.sehat〙\n╚═══════════════")
#-------------------------------------------------------------------------------
                elif text.lower() == 'protect on':
                        if settings["protect"] == True:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Already On")
                        else:
                            settings["protect"] = True
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Set To On")
                                
                elif text.lower() == 'protect off':
                        if settings["protect"] == False:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Already Off")
                        else:
                            settings["protect"] = False
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Set To Off")
#----------------------------------------------------------------------------------------                        
                elif text.lower() == 'qrprotect on':
                        if settings["qrprotect"] == True:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Qr On")
                            else:
                                unk.sendMessage(msg.to," Protection Qr Set To On")
                        else:
                            settings["qrprotect"] = True
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Qr Set To On")
                            else:
                                unk.sendMessage(msg.to," Protection Qr Already On")
                                
                elif text.lower() == 'qrprotect off':
                        if settings["qrprotect"] == False:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Qr Already Off")
                            else:
                                unk.sendMessage(msg.to," Protection Qr Set To Off")
                        else:
                            settings["qrprotect"] = False
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Qr Set To Off")
                            else:
                                unk.sendMessage(msg.to," Protection Qr Already Off")
#-------------------------------------------------------------------------------
                elif text.lower() == 'inviteprotect on':
                        if settings["inviteprotect"] == True:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Invite Already On")
                            else:
                                unk.sendMessage(msg.to," Protection Invite Set To On")
                        else:
                            settings["inviteprotect"] = True
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Invite Set To On")
                            else:
                                unk.sendMessage(msg.to," Protection Invite Already On")
                                
                elif text.lower() == 'inviteprotect off':
                        if settings["inviteprotect"] == False:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Invite Already Off")
                            else:
                                unk.sendMessage(msg.to," Protection Invite Set To Off")
                        else:
                            settings["inviteprotect"] = False
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Invite Set To Off")
                            else:
                                unk.sendMessage(msg.to," Protection Invite Already Off")
#-------------------------------------------------------------------------------
                elif text.lower() == 'cancelprotect on':
                        if settings["cancelprotect"] == True:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Cancel Invite Already On")
                            else:
                                unk.sendMessage(msg.to," Protection Cancel Invite Set To On")
                        else:
                            settings["cancelprotect"] = True
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Cancel Invite Set To On")
                            else:
                                unk.sendMessage(msg.to," Protection Cancel Invite Already On")
                                
                elif text.lower() == 'cancelprotect off':
                        if settings["cancelprotect"] == False:
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Cancel Invite Already Off")
                            else:
                                unk.sendMessage(msg.to," Protection Cancel Invite Set To Off")
                        else:
                            settings["cancelprotect"] = False
                            if settings["lang"] == "JP":
                                unk.sendMessage(msg.to," Protection Cancel Invite Set To Off")
                            else:
                                unk.sendMessage(msg.to," Protection Cancel Invite Already Off")
#-------------------------------------------------------------------------------
                elif text.lower() == 'pro on':
                        settings["protect"] = True
                        settings["qrprotect"] = True
                        settings["inviteprotect"] = True
                        settings["cancelprotect"] = True
                        settings["join link"] = True
                        unk.sendMessage(msg.to," All Protect Set To On")
                        		            
                elif text.lower() == 'pro off':
             #       if msg._from in Owner:
                        settings["protect"] = False
                        settings["qrprotect"] = False
                        settings["inviteprotect"] = False
                        settings["cancelprotect"] = False
                        unk.sendMessage(msg.to," All Protect Set To Modar")
            #        else:
             #           unk.sendMessage(msg.to,"Just for Owner")
#-------------------------------------------------------------------------------
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Auto Add")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Auto Add")
                elif text.lower() == 'autojoin on':
             #     if msg._from in Owner:    
                    settings["autoJoin"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Auto Join")
                elif text.lower() == 'autojoin off':
                #  if msg._from in Owner:    
                    settings["autoJoin"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Auto Join")
                elif text.lower() == 'autoleave on':
               #   if msg._from in Owner:
                    settings["autoLeave"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Auto Leave")
                elif text.lower() == 'autoleave off':
             #     if msg._from in Owner:
                    settings["autoLeave"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Auto Leave")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Auto Read")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Auto Read")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Check Details Sticker")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Check Details Sticker")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Detect Mention")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Detect Mention")
                elif text.lower() == 'join link on':
                    settings["autoJoinTicket"] = True
                    unk.sendMessage(to, "Berhasil mengaktifkan Auto Join Link")
                elif text.lower() == 'join link off':
                    settings["autoJoinTicket"] = False
                    unk.sendMessage(to, "Berhasil menonaktifkan Auto Join Link")                    
#==============================================================================#
                elif msg.text.lower() == 'respon':
                        ais.sendContact(to, aisMID)
                        ki2.sendContact(to, ki2MID)
                        ki3.sendContact(to, ki3MID)
                        ki4.sendContact(to, ki4MID)
                elif text.lower() in ["kabur"]:    
                    #unk.leaveGroup(msg.to)
                    ais.leaveGroup(msg.to)
                    ki2.leaveGroup(msg.to)
                    ki3.leaveGroup(msg.to)
                    ki4.leaveGroup(msg.to)
                elif text.lower() in ["kabur all"]:    
                    unk.leaveGroup(msg.to)
                    ais.leaveGroup(msg.to)
                    ki2.leaveGroup(msg.to)
                    ki3.leaveGroup(msg.to)
                    ki4.leaveGroup(msg.to)      
                elif text.lower() in ["join"]:    
                    G = unk.getGroup(msg.to)
                    ginfo = unk.getGroup(msg.to)
                    G.preventedJoinByTicket = False
                    unk.updateGroup(G)
                    invsend = 0
                    Ticket = unk.reissueGroupTicket(msg.to)
                    ais.acceptGroupInvitationByTicket(msg.to,Ticket)
                    ki2.acceptGroupInvitationByTicket(msg.to,Ticket)
                    ki3.acceptGroupInvitationByTicket(msg.to,Ticket)
                    ki4.acceptGroupInvitationByTicket(msg.to,Ticket)
                    G = unk.getGroup(msg.to)
                    G.preventedJoinByTicket = True
                    unk.updateGroup(G)
                    G.preventedJoinByTicket(G)
                    unk.updateGroup(G)
                
                elif text.lower() == 'me':
                    sendMessageWithMention(to, unkMID)
                    unk.sendContact(to, unkMID)
    #                unk.sendMessage(msg.to," Jangan Songong Pake Sc Orang")
                elif text.lower() == 'mymid':
                    unk.sendMessage(msg.to,"[MID]\n" +  unkMID)
                elif text.lower() == 'myname':
                    me = unk.getContact(unkMID)
                    unk.sendMessage(msg.to,"[DisplayName]\n" + me.displayName)
                elif text.lower() == 'mybio':
                    me = unk.getContact(unkMID)
                    unk.sendMessage(msg.to,"[StatusMessage]\n" + me.statusMessage)
                elif text.lower() == 'mypicture':
                    me = gie.getContact(unkMID)
                    unk.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideoprofile':
                    me = unk.getContact(unkMID)
                    unk.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = unk.getContact(unkMID)
                    cover = unk.getProfileCoverURL(unkMID)    
                    unk.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("stealcontact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = unk.getContact(ls)
                            mi_d = contact.mid
                            unk.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("midnya "):
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
                            ret_ += "\n{}" + ls
                        unk.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("stealname "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = unk.getContact(ls)
                            unk.sendMessage(msg.to, "[ Display Name ]\n" + contact.displayName)
                elif msg.text.lower().startswith("stealbio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = unk.getContact(ls)
                            unk.sendMessage(msg.to, "[ Status Message ]\n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("stealpicture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.unk.naver.jp/" + unk.getContact(ls).pictureStatus
                            unk.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealvideoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.unk.naver.jp/" + unk.getContact(ls).pictureStatus + "/vp"
                            unk.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealcover "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = unk.getProfileCoverURL(ls)
                                unk.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):    
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            unk.cloneContactProfile(contact)
                            unk.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                        except:
                            unk.sendMessage(msg.to, "Gagal clone member")
                elif text.lower() == 'restoreprofile':    
                    try:
                        unkProfile.displayName = str(myProfile["displayName"])
                        unkProfile.statusMessage = str(myProfile["statusMessage"])
                        unkProfile.pictureStatus = str(myProfile["pictureStatus"])
                        unk.updateProfileAttribute(8, unkProfile.pictureStatus)
                        unk.updateProfile(unkProfile)
                        unk.sendMessage(msg.to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                    except:
                        unk.sendMessage(msg.to, "Gagal restore profile")
#==============================================================================#
                elif msg.text.lower().startswith("mimicadd "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            unk.sendMessage(msg.to,"Target ditambahkan!")
                            break
                        except:
                            unk.sendMessage(msg.to,"Added Target Fail !")
                            break
                elif msg.text.lower().startswith("mimicdel "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            unk.sendMessage(msg.to,"Target dihapuskan!")
                            break
                        except:
                            unk.sendMessage(msg.to,"Deleted Target Fail !")
                            break
                elif text.lower() == 'mimiclist':
                    if settings["mimic"]["target"] == {}:
                        unk.sendMessage(msg.to,"Tidak Ada Target")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+unk.getContact(mi_d).displayName
                        unk.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                    
                elif "mimic" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            unk.sendMessage(msg.to,"Reply Message on")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            unk.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
                elif text.lower() == 'groupcreator':
                    group = unk.getGroup(to)
                    GS = group.creator.mid
                    unk.sendContact(to, GS)
                elif text.lower() == 'groupid':
                    gid = unk.getGroup(to)
                    unk.sendMessage(to, "[ID Group : ]\n" + gid.id)
                elif text.lower() == 'grouppicture':
                    group = unk.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    unk.sendImageWithURL(to, path)
                elif text.lower() == 'groupname':
                    gid = unk.getGroup(to)
                    unk.sendMessage(to, "[Nama Group : ]\n" + gid.name)
                elif text.lower() == 'gticket':
                    if msg.toType == 2:
                        group = unk.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = unk.reissueGroupTicket(to)
                            unk.sendMessage(to, "[ Group Ticket ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            unk.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu".format(str(settings["keyCommand"])))
                elif text.lower() == 'gticket on':
                    if msg.toType == 2:
                        group = unk.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            unk.sendMessage(to, "Grup qr sudah terbuka")
                        else:
                            group.preventedJoinByTicket = False
                            unk.updateGroup(group)
                            unk.sendMessage(to, "Berhasil membuka grup qr")
                elif text.lower() == 'gticket off':
                    if msg.toType == 2:
                        group = unk.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            unk.sendMessage(to, "Grup qr sudah tertutup")
                        else:
                            group.preventedJoinByTicket = True
                            unk.updateGroup(group)
                            unk.sendMessage(to, "Berhasil menutup grup qr")
                elif text.lower() == 'groupinfo':
                    group = unk.getGroup(to)
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
                        gTicket = "https://line.me/R/ti/g/{}".format(str(unk.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ Group Info ]"
                    ret_ += "\n╠ Nama Group : {}".format(str(group.name))
                    ret_ += "\n╠ ID Group : {}".format(group.id)
                    ret_ += "\n╠ Pembuat : {}".format(str(gCreator))
                    ret_ += "\n╠ Jumlah Member : {}".format(str(len(group.members)))
                    ret_ += "\n╠ Jumlah Pending : {}".format(gPending)
                    ret_ += "\n╠ Group Qr : {}".format(gQr)
                    ret_ += "\n╠ Group Ticket : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    unk.sendMessage(to, str(ret_))
                    unk.sendImageWithURL(to, path)
                elif text.lower() == 'groupmemberlist':
                    if msg.toType == 2:
                        group = unk.getGroup(to)
                        ret_ = "╔══[ Member List ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ Total {} ]".format(str(len(group.members)))
                        unk.sendMessage(to, str(ret_))
                elif text.lower() == 'grouplist':
                        groups = unk.groups
                        ret_ = "╔══[ Group List ]"
                        no = 0 + 1
                        for gid in groups:
                            group = unk.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
                        unk.sendMessage(to, str(ret_))
#-------------------------------------------------------------------------------
                elif text.lower() == 'clearban':
                        settings["blacklist"] = {}
                        ais.sendMessage(msg.to," Done")
                        
                elif text.lower() == 'absen':
                        ais.sendMessage(msg.to," Bot2 On")
                        ki2.sendMessage(msg.to," Bot3 On")
                        ki3.sendMessage(msg.to," Bot4 On")
                        ki4.sendMessage(msg.to," Bot5 On")
                        ki4.sendMessage(msg.to," Semua Sudah Hadir Bos Siap Beroparesi")
                        
                elif text.lower() == 'bancontact':
                        settings["wblacklist"] = True
                        unk.sendMessage(msg.to,"Send Contact")
                        
                elif msg.text in ["unbancontact"]:
                        settings["dblacklist"] = True
                        unk.sendMessage(msg.to,"Send Contact")
#-------------------------------------------------------------------------------
                elif text.lower() == 'banlist':
                        if settings["blacklist"] == {}:
                            unk.sendMessage(msg.to,"Tidak Ada Banlist")
                        else:
                            unk.sendMessage(msg.to,"Daftar Banlist")
                            num=1
                            msgs="═══T E R S A N G K A═══"
                            for mi_d in settings["blacklist"]:
                                msgs+="\n[%i] %s" % (num, unk.getContact(mi_d).displayName)
                                num=(num+1)
                            msgs+="\n═══T E R S A N G K A═══\n\nTotal Tersangka :  %i" % len(settings["blacklist"])
                            unk.sendMessage(msg.to, msgs)
#=======================================================================================
                elif msg.text.lower().startswith("kick "):
                       targets = []
                       key = eval(msg.contentMetadata["MENTION"])
                       key["MENTIONEES"][0]["M"]
                       for x in key["MENTIONEES"]:
                           targets.append(x["M"])
                       for target in targets:
                           try:
                               random.choice(UNK).kickoutFromGroup(msg.to,[target])
                           except:
                               random.choice(UNK).sendText(msg.to,"Error")
#-------------------------------------------------------------------------------
                elif text.lower() == 'kick all member':
                 #   if msg._from in Owner:
                        if msg.toType == 2:
                            print ("[ 19 ] KICK ALL MEMBER")
                            _name = msg.text.replace("kickallmember","")
                            #gs = unk.getGroup(msg.to)
                            gs = ais.getGroup(msg.to)
                            gs = ki2.getGroup(msg.to)
                            gs = ki3.getGroup(msg.to)
                            gs = ki4.getGroup(msg.to)
                           #unk.sendMessage(msg.to,"「 Bye All 」")
                           #unk.sendMessage(msg.to,"「 Sory guys 」")
                            targets = []
                            for g in gs.members:
                                if _name in g.displayName:
                                    targets.append(g.mid)
                            if targets == []:
                                unk.sendMessage(msg.to,"Not Found")
                            else:
                                for target in targets:
                                    if not target in Bots:
                                        if not target in Owner:
                                            if not target in admin:
                                                try:
                                                    klist=[line,ais,ki2,ki3,ki4]
                                                    kicker=random.choice(klist)
                                                    kicker.kickoutFromGroup(msg.to,[target])
                                                    print (msg.to,[g.mid])
                                                except:
                                                    unk.sendMessage(msg.to,"") 
#==============================================================================#          
                elif text.lower() == 'tag':
                    group = unk.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        unk.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        unk.sendMessage(to, "Total {} Mention".format(str(len(nama))))          
                elif text.lower() == 'lurking on':
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
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                unk.sendMessage(msg.to,"Lurking already on")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            unk.sendMessage(msg.to, "Set reading point:\n" + readTime)
                            unk.sendMessage(msg.to,"➲ Jangan Songong Pake Sc Orang")
                            
                elif text.lower() == 'lurking off':
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
                    if msg.to not in read['readPoint']:
                        unk.sendMessage(msg.to,"Lurking already off")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        unk.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == 'lurking reset':
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
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        unk.sendMessage(msg.to, "Reset reading point:\n" + readTime)
                    else:
                        unk.sendMessage(msg.to, "Lurking belum diaktifkan ngapain di reset?")
                        
                elif text.lower() == 'lurking':
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
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            unk.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = unk.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
                        try:
                            unk.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        unk.sendMessage(receiver,"Lurking has not been set.")
                        
#===============================================================================[unkMID - kiMID]
        if op.type == 19:
            print ("[ 19 ] UNK87 BOT KICK")
            try:
                if op.param3 in unkMID:
                    if op.param2 in aisMID:
                        G = ais.getGroup(op.param1)
#                        ginfo = ki.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ais.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                    else:
                        G = ais.getGroup(op.param1)
#                        ginfo = ais.getGroup(op.param1)
                        ais.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ais.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[unkMID - ki2MID]
                elif op.param3 in unkMID:
                    if op.param2 in ki2MID:
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                    else:
                        G = ki2.getGroup(op.param1)
                        ki2.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[unkMID - ki3MID]
                elif op.param3 in unkMID:
                    if op.param2 in ki3MID:
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                    else:
                        G = ki3.getGroup(op.param1)
                        ki3.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[unkMID - ki4MID]
                elif op.param3 in unkMID:
                    if op.param2 in ki4MID:
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                    else:
                        G = ki4.getGroup(op.param1)
                        ki4.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#===============================================================================[kiMID unkMID]
                if op.param3 in aisMID:
                    if op.param2 in unkMID:
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                    else:
                        G = unk.getGroup(op.param1)
                        unk.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[kiMID ki2MID]
                elif op.param3 in aisMID:
                    if op.param2 in ki2MID:
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                    else:
                        G = ki2.getGroup(op.param1)
#                        ginfo = ki2.getGroup(op.param1)
                        ki2.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[kiMID ki3MID]
                elif op.param3 in aisMID:
                    if op.param2 in ki3MID:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                    else:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        ki3.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[kiMID ki4MID]
                elif op.param3 in aisMID:
                    if op.param2 in ki4MID:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                    else:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        ki4.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#===============================================================================[ki2MID unkMID]
                if op.param3 in ki2MID:
                    if op.param2 in unkMID:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                    else:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        unk.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki2MID kiMID]
                elif op.param3 in ki2MID:
                    if op.param2 in aisMID:
                        G = ais.getGroup(op.param1)
#                        ginfo = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ais.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki.updateGroup(G)
                    else:
                        G = ais.getGroup(op.param1)
#                        ginfo = ki.getGroup(op.param1)
                        ais.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ki.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ais.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki2MID ki3MID]
                elif op.param3 in ki2MID:
                    if op.param2 in ki3MID:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                    else:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        ki3.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki2MID ki4MID]
                elif op.param3 in ki2MID:
                    if op.param2 in ki4MID:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                    else:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        ki4.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#===============================================================================[ki3MID unkMID]
                if op.param3 in ki3MID:
                    if op.param2 in unkMID:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                    else:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        unk.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki3MID kiMID]
                elif op.param3 in ki3MID:
                    if op.param2 in aisMID:
                        G = ais.getGroup(op.param1)
#                        ginfo = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                    else:
                        G = ais.getGroup(op.param1)
#                        ginfo = ais.getGroup(op.param1)
                        ais.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki3MID ki2MID]
                elif op.param3 in ki3MID:
                    if op.param2 in ki2MID:
                        G = ki2.getGroup(op.param1)
#                        ginfo = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                    else:
                        G = ki2.getGroup(op.param1)
#                        ginfo = ki2.getGroup(op.param1)
                        ki2.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki3MID ki4MID]
                elif op.param3 in ki3MID:
                    if op.param2 in ki4MID:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                    else:
                        G = ki4.getGroup(op.param1)
#                        ginfo = ki4.getGroup(op.param1)
                        ki4.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki4.updateGroup(G)
                        invsend = 0
                        Ticket = ki4.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki4.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki4.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki4.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#===============================================================================[ki4MID unkMID]
                if op.param3 in ki4MID:
                    if op.param2 in unkMID:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                    else:
                        G = unk.getGroup(op.param1)
#                        ginfo = unk.getGroup(op.param1)
                        unk.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        unk.updateGroup(G)
                        invsend = 0
                        Ticket = unk.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = unk.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        unk.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        unk.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki4MID kiMID]
                elif op.param3 in ki4MID:
                    if op.param2 in aisMID:
                        G = ais.getGroup(op.param1)
#                        ginfo = ki.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                    else:
                        G = ais.getGroup(op.param1)
#                        ginfo = ais.getGroup(op.param1)
                        ais.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ais.updateGroup(G)
                        invsend = 0
                        Ticket = ais.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ais.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ais.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ais.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki4MID ki2MID]
                elif op.param3 in ki4MID:
                    if op.param2 in ki2MID:
                        G = ki2.getGroup(op.param1)
#                        ginfo = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                    else:
                        G = ki2.getGroup(op.param1)
#                        ginfo = ki2.getGroup(op.param1)
                        ki2.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki2.updateGroup(G)
                        invsend = 0
                        Ticket = ki2.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki2.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki2.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki2.updateGroup(G)
                        settings["blacklist"][op.param2] = True
#-------------------------------------------------------------------------------[ki4MID ki3MID]
                elif op.param3 in ki4MID:
                    if op.param2 in ki3MID:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                    else:
                        G = ki3.getGroup(op.param1)
#                        ginfo = ki3.getGroup(op.param1)
                        ki3.kickoutFromGroup(op.param1,[op.param2])
                        G.preventedJoinByTicket = False
                        ki3.updateGroup(G)
                        invsend = 0
                        Ticket = ki3.reissueGroupTicket(op.param1)
                        unk.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ais.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki2.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki3.acceptGroupInvitationByTicket(op.param1,Ticket)
                        ki4.acceptGroupInvitationByTicket(op.param1,Ticket)
                        G = ki3.getGroup(op.param1)
                        G.preventedJoinByTicket = True
                        ki3.updateGroup(G)
                        G.preventedJoinByTicket(G)
                        ki3.updateGroup(G)
                        settings["blacklist"][op.param2] = True
                        
                elif op.param2 not in Bots:
                    if op.param2 in admin:
                        pass
                    elif settings["protect"] == True:
                        settings["blacklist"][op.param2] = True
                        random.choice(KAC).kickoutFromGroup(op.param1,[op.param2])
                        random.choice(KAC).inviteIntoGroup(op.param1,[op.param3])
                        random.choice(KAC).sendText(op.param1,"Don't Play bro...!")
                        
                else:
                    pass
            except:
                pass
#==============================================================================#
        if op.type == 13:
            if op.param2 not in Bots:
                if op.param2 in admin:
                    pass
                elif settings["inviteprotect"] == True:
                    settings["blacklist"][op.param2] = True
                    random.choice(KAC).cancelGroupInvitation(op.param1,[op.param3])
                    random.choice(KAC).kickoutFromGroup(op.param1,[op.param2])
                    if op.param2 not in Bots:
                        if op.param2 in admin:
                            pass
                        elif settings["cancelprotect"] == True:
                            settings["blacklist"][op.param2] = True
                            random.choice(KAC).cancelGroupInvitation(op.param1,[op.param3])	
#-------------------------------------------------------------------------------
        if op.type == 11:
            if op.param2 not in Bots:
                if op.param2 in admin and Bots and Owner:
                    pass
                elif settings["qrprotect"] == True:
                    settings["blacklist"][op.param2] = True
                    G = ais.getGroup(op.param1)
                    G.preventedJoinByTicket = True
                    ais.updateGroup(G)
                    random.choice(KAC).kickoutFromGroup(op.param1,[op.param2])
                else:
                    unk.sendMessage(op.param1,"Jangan Buka Qr")
            else:
                unk.sendMessage(op.param1,"")
#==============================================================================#
       # if op.type == 55:
        #    print ("[ 55 ] UNK87 BOTS EMPAT")
         #   if op.param1 in read["readPoint"]:
          #      _name = unk.getContact(op.param2).displayName
           #     tz = pytz.timezone("Asia/Jakarta")
           #     timeNow = datetime.now(tz=tz)
            #    timeHours = datetime.strftime(timeNow," (%H:%M)")
             #   read["readMember"][op.param1][op.param2] = str(_name) + str(timeHours)
     #   backupData()
    #except Exception as error:
     #   logError(error)
#==============================================================================#
        if op.type == 25:
            msg = op.message
            if text.lower() == '/ti/g/':    
                if settings["join ticket"] == True:
                    link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = link_re.findall(text)
                    n_links = []
                    for l in links:
                        if l not in n_links:
                            n_links.append(l)
                    for ticket_id in n_links:
                        group = unk.findGroupByTicket(ticket_id)
                        unk.acceptGroupInvitationByTicket(group.id,ticket_id)
                        unk.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
                        
    except Exception as error:
        logError(error)
#==============================================================================#
# Auto join if BOT invited to group
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        unk.acceptGroupInvitation(op.param1)
        ais.acceptGroupInvitation(op.param1)
        ki2.acceptGroupInvitation(op.param1)
        ki3.acceptGroupInvitation(op.param1)
        ki4.acceptGroupInvitation(op.param1)
    except Exception as e:
        unk.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))
# Auto kick if BOT out to group
def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param2 not in Bots:
            random.choice(KAC).kickoutFromGroup(op.param1,op.param2)
        else:
            pass
    except Exception as e:
        unk.log("[NOTIFIED_KICKOUT_FROM_GROUP] ERROR : " + str(e))

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)       
