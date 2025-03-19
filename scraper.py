# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:34:41 2024

@author: djmcd
"""

import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from seleniumbase import Driver

def readCBBR(team: str, year: str):
    """Scrapes the basketball reference page for a given team and year. Returns dict of stats."""
    link = f'https://www.sports-reference.com/cbb/schools/{team}/men/{year}.html'
    url = requests.get(link)
    soup = BeautifulSoup(url.text, "html.parser")
    
    try:
        data = soup.find("div", attrs={"id": "switcher_per_game_team"}).find("table").find("tbody").find_all("tr")
        stats = data[0].find_all("td")
        ranks = data[1].find_all("td")
        opp_stats = data[2].find_all("td")
        opp_ranks = data[3].find_all("td")
    except:
        return 1
    
    #Field Goals
    fg = stats[2].text
    fgr = ranks[2].text
    ofg = opp_stats[2].text
    ofgr = opp_ranks[2].text
    
    #Field Goal Pct
    fgp = stats[4].text
    fgpr = ranks[4].text
    ofgp = opp_stats[4].text
    ofgpr = opp_ranks[4].text
    
    #Three Point Field Goals
    tp = stats[8].text
    tpr = ranks[8].text
    otp = opp_stats[8].text
    otpr = opp_ranks[8].text
    
    #Three Point Pct
    tpp = stats[10].text
    tppr = ranks[10].text
    otpp = opp_stats[10].text
    otppr = opp_ranks[10].text
    
    #Free Throws
    ft = stats[11].text
    ftr = ranks[11].text
    oft = opp_stats[11].text
    oftr = opp_ranks[11].text
    
    #Free Throw Pct
    ftp = stats[13].text
    ftpr = ranks[13].text
    oftp = opp_stats[13].text
    oftpr = opp_ranks[13].text
    
    #Total Rebounds
    tr = stats[16].text
    trr = ranks[16].text
    otr = opp_stats[16].text
    otrr = opp_ranks[16].text
    
    #Turnovers
    to = stats[20].text
    tor = ranks[20].text
    oto = opp_stats[20].text
    otor = opp_ranks[20].text
    
    #Points
    pt = stats[22].text
    ptr = ranks[22].text
    opt = opp_stats[22].text
    optr = opp_ranks[22].text
    
    res = {"FG": fg,
            "FG Rk": fgr,
            "Opp FG": ofg,
            "Opp FG Rk": ofgr,
            "FG%": fgp,
            "FG% Rk": fgpr,
            "Opp FG%": ofgp,
            "Opp FG% Rk": ofgpr,
            "3P": tp,
            "3P Rk": tpr,
            "Opp 3P": otp,
            "Opp 3P Rk": otpr,
            "3P%": tpp,
            "3P% Rk": tppr,
            "Opp 3P%": otpp,
            "Opp 3P% Rk": otppr,
            "FT": ft,
            "FT Rk": ftr,
            "Opp FT": oft,
            "Opp FT Rk": oftr,
            "FT%": ftp,
            "FT% Rk": ftpr,
            "Opp FT%": oftp,
            "Opp FT% Rk": oftpr,
            "TR": tr,
            "TR Rk": trr,
            "Opp TR": otr,
            "Opp TR Rk": otrr,
            "TO": to,
            "TO Rk": tor,
            "Opp TO": oto,
            "Opp TO Rk": otor,
            "Pts": pt,
            "Pts Rk": ptr,
            "Opp Pts": opt,
            "Opp Pts Rk": optr}
    
    return res
    
def readGameLog(team: str, year: str):
    """Scrapes the basketball reference game log for a given team and year. Returns list of game dicts."""
    link = f'https://www.sports-reference.com/cbb/schools/{team}/men/{year}-gamelogs.html'
    url = requests.get(link)
    soup = BeautifulSoup(url.text, "html.parser")
    
    try:
        gamelog = soup.find("div", attrs={"id": "div_team_game_log"}).find("table").find("tbody").find_all("tr")
    except:
        print("Error fetching games")
        return 1
    
    games = []
    for gm in gamelog:
        #Continue over empty rows
        if (gm.attrs=={"class": ["over_header", "thead"]} or gm.attrs=={"class": ["thead"]}):
            continue
        
        cols = gm.find_all("td")
        loc = cols[2].text
        opp = cols[3].text
        pt = cols[6].text
        opt = cols[7].text
        fgp = cols[10].text
        ofgp = cols[27].text
        tpp = cols[13].text
        otpp = cols[30].text
        tr = cols[18].text
        otr = cols[35].text
        to = cols[22].text
        oto = cols[39].text
                
        if (pt == ""):
            continue
        
        if (loc == ""):
            loc = "H"
        
        game = {"Opp": opp,
                "Loc": loc,
                "Pts": pt,
                "Opp Pts": opt,
                "Net Pts": int(pt) - int(opt),
                "FG%": fgp,
                "Opp FG%": ofgp,
                "3P%": tpp,
                "Opp 3P%": otpp,
                "TR": tr,
                "Opp TR": otr,
                "TO": to,
                "Opp TO": oto}
        
        games.append(game)
        
    return games
    
def readKenPom(team: str, year: str):
    """Scrapes kenpom rankings for a given team and year. Returns dict of metrics."""
    # Set up selenium
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    
    driver = Driver(uc=True, headless=False)
    
    link = f'https://kenpom.com/index.php?y={year}'
    driver.uc_open_with_reconnect(link, reconnect_time=6)
    driver.uc_gui_click_captcha()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be(link))
    time.sleep(1)
    if driver.current_url == link:
        table = driver.page_source
    
    soup = BeautifulSoup(table, "html.parser")
    
    driver.quit()
    
    #Have to double loop here because every 40 teams is a new tbody
    tables = soup.find("div", attrs={"id": "table-wrapper"}).find("table").find_all("tbody")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            try:
                cols[1]
            except:
                continue
            
            #Since this is for tournament teams, have to get rid of their ranking, hence [:-2]
            if (cols[1].text.lower()[:-2] == team.lower() or cols[1].text.lower()[:-3] == team.lower()):
                rk = cols[0].text
                em = cols[4].text
                o = cols[5].text
                ork = cols[6].text
                d = cols[7].text
                drk = cols[8].text
                t = cols[9].text
                trk = cols[10].text
                l = cols[11].text
                lrk = cols[12].text
                sos = cols[13].text
                sosrk = cols[14].text
                oppo = cols[15].text
                oppork = cols[16].text
                oppd = cols[17].text
                oppdrk = cols[18].text
                
                data = {"EM": em,
                        "Rk": rk,
                        "Off": o,
                        "Off Rk": ork,
                        "Def": d,
                        "Def Rk": drk,
                        "Temp": t,
                        "Temp Rk": trk,
                        "Luck": l,
                        "Luck Rk": lrk,
                        "Opp EM": sos,
                        "Opp EM Rk": sosrk,
                        "Opp Off": oppo,
                        "Opp Off Rk": oppork,
                        "Opp Def": oppd,
                        "Opp Def Rk": oppdrk}
                
                return data


    return 1