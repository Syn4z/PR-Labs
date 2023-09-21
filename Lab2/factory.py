from player import Player
import xml.etree.ElementTree as xmlTree
import player_pb2
from datetime import datetime


class PlayerFactory:
    def to_json(self, players):
        # This function should transform a list of Player objects into a list with dictionaries.
        dictList = []
        for player in players:
            playerDict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": str(player.date_of_birth).split()[0],
                "xp": player.xp,
                "class": player.cls
            }
            dictList.append(playerDict)
        return dictList

    def from_json(self, list_of_dict):
        # This function should transform a list of dictionaries into a list with Player objects.
        playerList = []
        for dictionary in list_of_dict:
            player = Player(dictionary["nickname"], dictionary["email"], dictionary["date_of_birth"], dictionary["xp"],
                            dictionary["class"])
            playerList.append(player)
        return playerList

    def from_xml(self, xml_string):
        # This function should transform a XML string into a list with Player objects.
        playerList = []
        xmlObject = xmlTree.fromstring(xml_string)
        for block in xmlObject.findall("player"):
            player = Player(block.find("nickname").text, block.find("email").text, block.find("date_of_birth").text,
                            int(block.find("xp").text), block.find("class").text)
            playerList.append(player)
        return playerList

    def to_xml(self, list_of_players):
        # This function should transform a list with Player objects into a XML string.
        xmlString = ""
        xmlString += "<?xml version=\"1.0\"?>\n"
        xmlString += "<data>\n"
        for player in list_of_players:
            dateOfBirth = player.date_of_birth.strftime("%Y-%m-%d")
            xmlString += "<player>\n"
            xmlString += "<nickname>" + player.nickname + "</nickname>\n"
            xmlString += "<email>" + player.email + "</email>\n"
            xmlString += "<date_of_birth>" + dateOfBirth + "</date_of_birth>\n"
            xmlString += "<xp>" + str(player.xp) + "</xp>\n"
            xmlString += "<class>" + player.cls + "</class>\n"
            xmlString += "</player>\n"
        xmlString += "</data>\n"
        return xmlString

    def from_protobuf(self, binary):
        playersList = player_pb2.PlayersList()
        playersList.ParseFromString(binary)
        playersObjects = []
        for player_message in playersList.player:
            player = Player(
                nickname=player_message.nickname,
                email=player_message.email,
                date_of_birth=player_message.date_of_birth,
                xp=player_message.xp,
                cls=player_pb2.Class.Name(player_message.cls)
            )
            playersObjects.append(player)
        return playersObjects

    def to_protobuf(self, list_of_players):
        playersMessages = []
        for player in list_of_players:
            player_message = player_pb2.PlayersList.Player()
            player_message.nickname = player.nickname
            player_message.email = player.email
            player_message.date_of_birth = datetime.strftime(player.date_of_birth, "%Y-%m-%d")
            player_message.xp = player.xp
            player_message.cls = player_pb2.Class.Value(player.cls)
            playersMessages.append(player_message)
        playersMessagesList = player_pb2.PlayersList(player=playersMessages)
        binaryData = playersMessagesList.SerializeToString()
        return binaryData
