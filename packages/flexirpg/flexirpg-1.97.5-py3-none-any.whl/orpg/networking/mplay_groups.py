from orpg.mapper.map_msg import *

class game_group:
    def __init__( self, id, name, pwd, desc="", boot_pwd="", minVersion="", mapFile=None, messageFile=None, persist =0 ):
        self.id = id
        self.name = name
        self.desc = desc
        self.minVersion = minVersion
        self.messageFile = messageFile
        self.players = []
        self.pwd = pwd
        self.boot_pwd = boot_pwd
        self.game_map = map_msg()
        self.persistant = persist

        if mapFile != None:
            f = open( mapFile )
            tree = f.read()
            f.close()

        else:
            f = open(orpg.dirpath.dir_struct["template"] + "default_map.xml")
            tree = f.read()
            f.close()

        self.game_map.init_from_xml(tree)


    def add_player(self,id):
        self.players.append(id)

    def remove_player(self,id):
        self.players.remove(id)

    def get_num_players(self):
        num =  len(self.players)
        return num

    def get_player_ids(self):
        tmp = self.players
        return tmp


    def check_pwd(self,pwd):
        return (pwd==self.pwd)

    def check_boot_pwd(self,pwd):
        return (pwd==self.boot_pwd)

    def check_version(self,ver):
        if (self.minVersion == ""):
            return 1
        minVersion=self.minVersion.split('.')
        version=ver.split('.')
        for i in range(min(len(minVersion),len(version))):
            w=max(len(minVersion[i]),len(version[i]))
            v1=minVersion[i].rjust(w);
            v2=version[i].rjust(w);
            if v1<v2:
                return 1
            if v1>v2:
                return 0

        if len(minVersion)>len(version):
            return 0
        return 1

    #depreciated - see send_group_list()
    def toxml(self,act="new"):
        #  Please don't add the boot_pwd to the xml, as this will give it away to players watching their console
        xml_data = "<group id=\"" + self.id
        xml_data += "\" name=\"" + self.name
        xml_data += "\" pwd=\"" + str(self.pwd!="")
        xml_data += "\" players=\"" + str(self.get_num_players())
        xml_data += "\" action=\"" + act + "\" />"
        return xml_data
