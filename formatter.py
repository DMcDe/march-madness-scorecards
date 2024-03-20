# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 13:40:08 2024

@author: djmcd
"""

def formatCBBR(stats: dict):
    """Reformats a dictionary of basketball reference stats to make it easier to iterate through for visuals. Returns formatted list."""
    fg = {"Stat": "FG", "Num": stats["FG"], "Rk": stats["FG Rk"], "Opp": stats["Opp FG"], "Opp Rk": stats["Opp FG Rk"]}
    fgp = {"Stat": "FG%", "Num": stats["FG%"], "Rk": stats["FG% Rk"], "Opp": stats["Opp FG%"], "Opp Rk": stats["Opp FG% Rk"]}
    tp = {"Stat": "3P", "Num": stats["3P"], "Rk": stats["3P Rk"], "Opp": stats["Opp 3P"], "Opp Rk": stats["Opp 3P Rk"]}
    tpp = {"Stat": "3P%", "Num": stats["3P%"], "Rk": stats["3P% Rk"], "Opp": stats["Opp 3P%"], "Opp Rk": stats["Opp 3P% Rk"]}
    ft = {"Stat": "FT", "Num": stats["FT"], "Rk": stats["FT Rk"], "Opp": stats["Opp FT"], "Opp Rk": stats["Opp FT Rk"]}
    ftp = {"Stat": "FT%", "Num": stats["FT%"], "Rk": stats["FT% Rk"], "Opp": stats["Opp FT%"], "Opp Rk": stats["Opp FT% Rk"]}
    tr = {"Stat": "TR", "Num": stats["TR"], "Rk": stats["TR Rk"], "Opp": stats["Opp TR"], "Opp Rk": stats["Opp TR Rk"]}
    to = {"Stat": "TO", "Num": stats["TO"], "Rk": stats["TO Rk"], "Opp": stats["Opp TO"], "Opp Rk": stats["Opp TO Rk"]}
    pts = {"Stat": "Pts", "Num": stats["Pts"], "Rk": stats["Pts Rk"], "Opp": stats["Opp Pts"], "Opp Rk": stats["Opp Pts Rk"]}
    
    return [tr, to, ftp, ft, tpp, tp, fgp, fg, pts]

def getRecords(games: dict):
    """Generates overall, home, neutral, and road records given a game log. Returns a dict with wins, losses, and win pct."""
    #Declare variables for home/road/neutral wins/losses
    h_w = h_l = r_w = r_l = n_w = n_l = 0
    
    #Add each game to respective category
    for gm in games:
        if (gm["Loc"] == "H"):
            if (gm["Net Pts"] > 0):
                h_w += 1
            else:
              h_l +=1
        elif (gm["Loc"] == "@"):
            if (gm["Net Pts"] > 0):
                r_w += 1
            else:
                r_l += 1
        elif (gm["Loc"] == "N"):
            if (gm["Net Pts"] > 0):
                n_w += 1
            else:
                n_l += 1
        else:
            print("Unexpected game location. Game is excluded from records.\n")
        
    #Get overall record
    w = h_w + r_w + n_w
    l = h_l + r_l + n_l
    
    #Calculate winning percentages
    wp = w / (w + l)
    hwp = h_w / (h_w + h_l)
    rwp = r_w / (r_w + r_l)
    nwp = n_w / (n_w + n_l)
    
    #Return data
    rec = {"W": w,
           "L": l,
           "%": wp,
           "Hm W": h_w,
           "Hm L": h_l,
           "Hm %": hwp,
           "Rd W": r_w,
           "Rd L": r_l,
           "Rd %": rwp,
           "Nt W": n_w,
           "Nt L": n_l,
           "Nt %": nwp
           }
    
    return rec