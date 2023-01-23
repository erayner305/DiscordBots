from urllib.request import urlopen

class player:
    def openURL(self, battleID):
        userinfo = battleID
        url = f'https://overwatch.blizzard.com/en-us/career/{userinfo}/'
        page = urlopen(url)
        html = page.read().decode("utf-8")
        return html

    def winRate(self, html):
        htmlID = "<p class=\"name\">Games Played</p><p class=\"value\">"
        modifier = len(htmlID)

        start = html.find(htmlID) + modifier
        if start != modifier - 1:
            totalGames = html[start:html.find("</p>", start)]
        else:
            self.private = True
            return "Profile is Private!"
        
        htmlID = "<p class=\"name\">Games Lost</p><p class=\"value\">"
        modifier = len(htmlID)

        start = html.find(htmlID) + modifier
        wonGames = int(totalGames) - int(html[start:html.find("</p>", start)])

        output = round((float(wonGames)/float(totalGames)) * 100, 2)
        return output
    
    def averages(self, type, html):
        if type == "healing":
            htmlID = "<p class=\"name\">Healing Done - Avg per 10 Min</p><p class=\"value\">"
        elif type == "damage":
            htmlID = "<p class=\"name\">Hero Damage Done - Avg per 10 Min</p><p class=\"value\">"
        else:
            return "Invalid Parameter"
        modifier = len(htmlID)

        start = html.find(htmlID) + modifier
        if start != modifier - 1:
            output = html[start:html.find("</p>", start)]
        else:
            self.private = True
            return "Profile is Private!"

        return int(output)
        

    def __init__(player, battleID):
        player.exists = True
        player.private = False
        try: profile = player.openURL(battleID) 
        except: player.exists = False

        if player.exists:
            player.healing = player.averages("healing", profile)
            player.damage = player.averages("damage", profile)
            player.wins = player.winRate(profile)

eric = player("Breach-11489")
print(eric.damage)
print(eric.healing)
print(eric.wins)