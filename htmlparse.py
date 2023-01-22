from urllib.request import urlopen

def openURL(battlenetID):
    userinfo = battlenetID
    url = f'https://overwatch.blizzard.com/en-us/career/{userinfo}/'
    try:
        page = urlopen(url)
    except: 
        return False

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def averageHealing(battlenetID):
    html = openURL(battlenetID)
    if html == False:
        return "Incorrect Profile!"

    htmlID = "<p class=\"name\">Healing Done - Avg per 10 Min</p><p class=\"value\">"
    modifier = len(htmlID)

    start = html.find(htmlID) + modifier
    if start != modifier - 1:
        output = html[start:html.find("</p>", start)]
    else:
        return "Profile is Private!"
    
    if "." in output:
        output = float(output)
    else:
        output = int(output)
    return output

def averageFinalBlows(battlenetID):
    html = openURL(battlenetID)
    if html == False:
        return "Incorrect Profile!"
        

    htmlID = "<p class=\"name\">Final Blows - Avg per 10 Min</p><p class=\"value\">"
    modifier = len(htmlID)

    start = html.find(htmlID) + modifier
    if start != modifier - 1:
        output = html[start:html.find("</p>", start)]
    else:
        return "Profile is Private!"
    if "." in output:
        output = float(output)
    else:
        output = int(output)
    return output

def averageDamage(battlenetID):
    html = openURL(battlenetID)
    if html == False:
        return "Incorrect Profile!"
        

    htmlID = "<p class=\"name\">Hero Damage Done - Avg per 10 Min</p><p class=\"value\">"
    modifier = len(htmlID)

    start = html.find(htmlID) + modifier
    if start != modifier - 1:
        output = html[start:html.find("</p>", start)]
    else:
        return "Profile is Private!"

    if "." in output:
        output = float(output)
    else:
        output = int(output)
    return output

def gamesPlayed(battlenetID):
    html = openURL(battlenetID)
    if html == False:
        return "Incorrect Profile!"
        

    htmlID = "<p class=\"name\">Games Played</p><p class=\"value\">"
    modifier = len(htmlID)

    start = html.find(htmlID) + modifier
    if start != modifier - 1:
        totalGames = html[start:html.find("</p>", start)]
    else:
        return "Profile is Private!"
    
    htmlID = "<p class=\"name\">Games Lost</p><p class=\"value\">"
    modifier = len(htmlID)
    start = html.find(htmlID) + modifier
    lostGames = html[start:html.find("</p>", start)]

    output = round((float(int(totalGames)-int(lostGames))/float(totalGames)) * 100, 2)
    return output