import discord
import random
import json
import os


class Dice():

    @staticmethod
    def Shake(num=1,surface=100,drift=0,listing=False):
        if listing:
            dst = []
            for i in range(abs(num)):
                dst.append(random.randrange(1,surface+1))
            dst.append(sum(dst)+drift)
            return dst
        else:
            dst = drift
            for i in range(abs(num)):
                dst += (random.randrange(1,surface+1))

            if num <0 :dst = -dst
            return dst

    @staticmethod
    def ToStr(num=1,surface=100,drift=0):#exanple "-1D4+3"
        if num == 0: return str(drift)#Diceがない場合補整値をそのまま出力
        elif num == 1:num = ""
        elif num == -1: num = "-"
        else: pass

        if drift == 0:
            return"{}D{}".format(num, surface)
        else:
            return "{}D{}{:+}".format(num, surface, drift)

    @staticmethod
    def ToDict(strring):
        tmp = strring

        [num ,tmp] = tmp.split("D")

        if not num:
            num = 1
        elif num == "-":
            num = -1
        else:
            num = int(num)

        if "+" in tmp:
            [surface,drift] = tmp.split("+")
            surface = int(surface)
            drift = int(drift)
        elif "-" in tmp:
            [surface,drift] = tmp.split("-")
            surface = int(surface)
            drift = - int(drift)
        else:
            surface = int(tmp)
            drift = 0

        return {"num":num, "surface":surface, "drift":drift}


class TRPG_Seat():
    STATUS_DICE_DICT = {
        "STR":{ "num":3, "surface":6 },
        "CON":{ "num":3, "surface":6 },
        "POW":{ "num":3, "surface":6 },
        "DEX":{ "num":3, "surface":6 },
        "APP":{ "num":3, "surface":6 },
        "SIZ":{ "num":2, "surface":6, "drift":6 },
        "INT":{ "num":2, "surface":6, "drift":6 },
        "EDU":{ "num":3, "surface":6, "drift":3 },
        "財産":{ "num":3, "surface":6 },
    }
    SKILL_DICT = {
        "回避":0,
        "キック":25,
        "組み付き":25,
        "こぶし":50,
        "頭突き":10,
        "投擲":25,
        "マーシャルアーツ":1,
        "拳銃":20,
        "サブマシンガン":15,
        "ショットガン":30,
        "マシンガン":15,
        "ライフル":25,
    
        "応急手当":30,
        "鍵開け":1,
        "隠す":15,
        "隠れる":10,
        "聞き耳":25,
        "忍び歩き":10,
        "写真術":10,
        "精神分析":1,
        "追跡":10,
        "登攀":40,
        "図書館":25,
        "目星":25,
    
        "運転":20,
        "機械修理":20,
        "重機械操作":1,
        "乗馬":5,
        "水泳":25,
        "製作":5,
        "操縦":1,
        "跳躍":25,
        "電気修理":10,
        "ナビゲート":10,
        "変装":1,
    
        "言いくるめ":5,
        "信用":15,
        "説得":15,
        "値切り":5,
        "母国語":50,
    
        "医学":5,
        "オカルト":5,
        "化学":1,
        "クトゥルフ神話":0,
        "芸術":5,
        "経理":10,
        "考古学":1,
        "コンピューター":1,
        "心理学":5,
        "人類学":1,
        "生物学":1,
        "地質学":1,
        "電子工学":1,
        "天文学":1,
        "博物学":10,
        "物理学":1,
        "法律":5,
        "薬学":1,
        "歴史":20,
    }

    def __init__(self):
        self.StatusDict ={
            "パーソナルデータ":{
                "名前":"名無し",
                "職業":"放浪者",
                "年齢":"25",
                "性別":"男",
                "髪の色":"黒",
                "瞳の色":"黒",
                "肌の色":"肌色",
                "身長":"175",
                "体重":"65",
            },
            "能力値":{
                "STR":0,
                "CON":0,
                "POW":0,
                "DEX":0,
                "APP":0,
                "SIZ":0,
                "INT":0,
                "EDU":0,
                "財産":0,
                "SAN":0,
                "幸運":0,
                "アイデア":0,
                "知識":0,
                "HP":0,
                "MP":0,
                "職業機能ポイント":0,
                "趣味技能ポイント":0,
                "ダメージボーナス":"0",
            },
            "SAN不定領域":0,
            "技能値":self.SKILL_DICT.copy(),
            "武器・防具":{},
            "所持品・所持金":{},
            "メモ":{},
        }
        self.StatusDice()
        return

    @staticmethod
    def CalcBounus_Num(BNS_sum):#Diceの数
        if BNS_sum <= 16:
            return -1
        else:
            return (BNS_sum -9)//16

    @staticmethod
    def CalcBounus_Surface(BNS_sum):#Diceの面の数
        return 4 if(13 <= BNS_sum <= 32) else 6  #ダメージボーナス https://hajimeteno-trpg.com/wp/entry/2018/10/18/214451


    def DecideName(self, who):#TODO Dict
        self.name = who
        return

    def StatusDice(self,print=True):
        for key,item in self.STATUS_DICE_DICT.items():
            self.StatusDict["能力値"][key] = Dice.Shake(**item)
        self.StatusCalc()
        return

    def SANCalc(self):
        self.StatusDict["SAN不定領域"] = self.StatusDict["能力値"]["SAN"] *4 //5
        return


    def StatusCalc(self):
        self.StatusDict["能力値"]["SAN"] = self.StatusDict["能力値"]["POW"] *5
        self.StatusDict["能力値"]["幸運"] = self.StatusDict["能力値"]["POW"] *5
        self.StatusDict["能力値"]["アイデア"] = self.StatusDict["能力値"]["INT"] *5
        self.StatusDict["能力値"]["知識"] = self.StatusDict["能力値"]["EDU"] *5
        self.StatusDict["能力値"]["HP"] = round((self.StatusDict["能力値"]["CON"] + self.StatusDict["能力値"]["SIZ"]) /2)
        self.StatusDict["能力値"]["MP"] = self.StatusDict["能力値"]["POW"]
        self.StatusDict["能力値"]["職業機能ポイント"] = self.StatusDict["能力値"]["EDU"] *20
        self.StatusDict["能力値"]["趣味技能ポイント"] = self.StatusDict["能力値"]["INT"] *10
        BNS_sum = self.StatusDict["能力値"]["STR"] + self.StatusDict["能力値"]["SIZ"]
        self.StatusDict["能力値"]["ダメージボーナス"] = Dice.ToStr(
            num=self.CalcBounus_Num(BNS_sum),
            surface=self.CalcBounus_Surface(BNS_sum)
        )
        self.StatusDict["技能値"]["回避"] = self.StatusDict["能力値"]["DEX"] *2
        self.StatusDict["技能値"]["母国語"] = self.StatusDict["能力値"]["EDU"] *5
        self.SANCalc()
        return
     

    def PrintStatus(self,key=""):
        if key:
            return self.StatusDict["能力値"][key]
        else:
            return self.StatusDict["能力値"]

    def OverrideStatus(self,key1,key2,value):
        self.StatusDict[key1][key2] = value
        return


class TRPG_Seat_bot(discord.Client):

    Character_Dictionary ={}

    def print_Status(self,user):
            status =  self.Character_Dictionary[user].PrintStatus()
            dst = []
            for key, item in status.items():
                dst.append("{} : {},　".format(key,item))
                if key == "EDU" or key == "MP":
                    dst.append("\n")

            dst.append(dst.pop().replace(", ", ""))
            return("".join(dst).replace(",\n", "\n"))
    
    def Save_File(self,user,filename="tmp"):
        try:
            os.mkdir("./{}/".format(user))
        except FileExistsError:
            pass

        with open("./{}/{}.json".format(user,filename),mode="w") as f:
            json.dump(self.Character_Dictionary[user].StatusDict,f,indent=4,ensure_ascii=False)
        return



    async def on_ready(self):
        print("ログインしました")
        return

    async def on_message(self,message):
        if message.author.bot : return  #botは無視

        strring = message.content
        sendM = message.channel.send
        user = message.author.name

        if strring == "!make":
            self.Character_Dictionary[user] = TRPG_Seat()
            await sendM(self.print_Status(user))
            return

        if strring =="!clear":
            await sendM("{}のキャラクターは消滅した".format(user) if self.Character_Dictionary.pop(user,None) else "{}には消すキャラクターがいない".format(user))
            return
        
        """
        if strring =="!save":
            self.Save_File(user=user)
        """

        if strring == "!show":
            if user in self.Character_Dictionary:
                await sendM(self.print_Status(user))
            else:
                self.Character_Dictionary[user] = TRPG_Seat()
                await sendM(self.print_Status(user))
            return

        
        if strring.startswith("!override."):
            strring = strring.split(".")
            if len(strring) != 4:
                await sendM("sample\n`!override.能力値.SAN.10`\n`!override.技能値.目星.99`")
            else:
                self.Character_Dictionary[user].OverrideStatus(*strring[1:])
            return

        if strring.startswith("!change."):
            strring = strring.split(".")
            if len(strring) != 4:
                await sendM("sample\n`!change.能力値.SAN.10`\n`!change.技能値.目星.99`")
            else:
                self.Character_Dictionary[user].OverrideStatus(*strring[1:])
                self.Character_Dictionary[user].StatusCalc()
            return

        if strring.startswith(("#","＃")) and "D" in strring:#ロール処理
            strring = strring.replace("＃","#").replace("#","").replace("＋","+")
            try:
                tmp = Dice.ToDict(strring)
            except ValueError:
                await sendM(file=discord.File("NotInt.png"))
                return
            dst = []
            if tmp["surface"] <= 3 or tmp["num"] == 0:
                dst.append("コロコロ...(?!)\n")
            else:
                dst.append("コロコロ...\n")
            dst.append("{}さん".format(user))
            if tmp["num"] <= 1:
                dst.append("，{}です".format(Dice.Shake(**tmp)))
                await sendM("".join(dst))
                return
            elif tmp["num"] > 50:
                await sendM(file=discord.File("ToManyNum.png"))
            else:
                result = Dice.Shake(**tmp,listing=True)
                for i in range(tmp["num"]):
                    result[i] = "{}個目 : {}\n".format(i+1,result[i])

                result[tmp["num"]] = "{}さんの合計 : {}".format(user,result[tmp["num"]])
                dst.append("\n")
                dst = dst + result
                await sendM("".join(dst))
            return

        if strring =="!halt.seat":
            await sendM("ログアウトします")
            for key in self.Character_Dictionary:
                self.Save_File(user=key)
            await self.close()

def main():
    TOKEN = "yore token"
    client = TRPG_Seat_bot()
    client.run(TOKEN)

def test():
    print("")

if __name__ == "__main__":
    main()
    #test()
