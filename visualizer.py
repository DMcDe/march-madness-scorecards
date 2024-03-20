# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:26:52 2024

@author: djmcd
"""

import formatter as fm
import matplotlib as mpl
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class logoManager():
    def __init__(self, file: str):
        """Creates pandas dataframe with team name and logo IDs."""
        self.df = pd.read_csv(file).set_index("team")
        self.df.index = self.df.index.str.lower()

    def getLogo(self, team: str, zm = 1):
        """Gets the logo for a team. Returns it as an offsetimage for a mpl plot."""
        team_id = self.getLogoID(team)        
        return OffsetImage(plt.imread(f'./logos/{team_id}.png'), zoom = zm)
        
    def getLogoID(self, team: str):
        """Queries df to turn a team name into the id in the folder. Returns the id."""
        try:
            team_id = str(self.df.at[team, 'team.id'])
        except:
            print(f"{team} logo not found. Inserting generic.\n")
            team_id = "Basketball Filler"
            
        return team_id

def makeKenPomTable(data: dict, fig = None, ax = None):
    """Generates the table given a dict of kenpom data. Returns the mpl ax w the table."""
    if (ax is None or fig is None):
        #Declare figure
        fig, ax = plt.subplots(figsize = (5, 5))
    
    #Set layout size and configurations
    rows = 16
    cols = 16
    
    x_left = 0
    x_right = cols
    x_quart = x_right / 4
    
    y_lower = 0
    y_upper = rows
    y_quart = y_upper / 4
    
    ax.set_xlim(x_left, x_right)
    ax.set_ylim(y_lower, y_upper)
    
    #Trace layout lines
    ax.plot([x_left, 3 * x_quart], [y_quart, y_quart], ls = ":", c = "k", lw = 0.75)
    ax.plot([3 * x_quart, 3 * x_quart], [y_quart, y_upper], ls = ":", c = "k", lw = 0.75)
    
    ax.plot([1 * x_quart, 1 * x_quart], [y_lower, y_quart], ls = ":", c = "k", lw = 0.75)
    ax.plot([2 * x_quart, 2 * x_quart], [y_lower, y_quart], ls = ":", c = "k", lw = 0.75)
    ax.plot([3 * x_quart, 3 * x_quart], [y_lower, y_quart], ls = ":", c = "k", lw = 0.75)
    
    ax.plot([3 * x_quart, x_right], [3 * y_quart, 3 * y_quart], ls = ":", c = "k", lw = 0.75)
    ax.plot([3 * x_quart, x_right], [2 * y_quart, 2 * y_quart], ls = ":", c = "k", lw = 0.75)
    ax.plot([3 * x_quart, x_right], [1 * y_quart, 1 * y_quart], ls = ":", c = "k", lw = 0.75)
    
    #Outline plot
    ax.plot([x_left, x_left], [y_lower, y_upper], lw = 1.5, c = "k")
    ax.plot([x_right, x_right], [y_lower, y_upper], lw = 1.5, c = "k")
    ax.plot([x_left, x_right], [y_lower, y_lower], lw = 1.5, c = "k")
    ax.plot([x_left, x_right], [y_upper, y_upper], lw = 1.5, c = "k")
    
    #Define colormap
    norm = mpl.colors.Normalize(1, 351)
    cmap = mpl.colors.LinearSegmentedColormap.from_list("gr", ["g", "w", "r"], N = 351)
    
    #Featured text
    ax.text(x = 1.5 * x_quart, y = 2.5 * y_quart, s = data["EM"], va = "center", ha = "center", fontsize = 30)
    ax.text(x = 1.5 * x_quart, y = 2.5 * y_quart + 1.25, s = "AdjEM", va = "center", ha = "center", weight = "bold", fontsize = 25)
    ax.text(x = 1.5 * x_quart, y = 2.5 * y_quart - 1.25, s = "({rk})".format(rk = data["Rk"]), va = "center", ha = "center", fontsize = 20)
    rect_em = patches.Rectangle((0, y_quart), width = 3 * x_quart, height = 3 * y_quart, ec = "none", fc = cmap(norm(int(data["Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_em)
    
    #Offense
    ax.text(x = 3.5 * x_quart, y = 3.5 * y_quart, s = data["Off"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 3.5 * x_quart, y = 3.5 * y_quart + 1, s = "AdjO", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 3.5 * x_quart, y = 3.5 * y_quart - 1, s = "({rk})".format(rk = data["Off Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_off = patches.Rectangle((3 * x_quart, 3 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Off Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_off)
    
    #Defense
    ax.text(x = 3.5 * x_quart, y = 2.5 * y_quart, s = data["Def"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 3.5 * x_quart, y = 2.5 * y_quart + 1, s = "AdjD", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 3.5 * x_quart, y = 2.5 * y_quart - 1, s = "({rk})".format(rk = data["Def Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_def = patches.Rectangle((3 * x_quart, 2 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Def Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_def)
    
    #Tempo
    ax.text(x = 3.5 * x_quart, y = 1.5 * y_quart, s = data["Temp"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 3.5 * x_quart, y = 1.5 * y_quart + 1, s = "AdjT", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 3.5 * x_quart, y = 1.5 * y_quart - 1, s = "({rk})".format(rk = data["Temp Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_t = patches.Rectangle((3 * x_quart, 1 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Temp Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_t)
    
    #Luck
    ax.text(x = 3.5 * x_quart, y = 0.5 * y_quart, s = data["Luck"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 3.5 * x_quart, y = 0.5 * y_quart + 1, s = "Luck", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 3.5 * x_quart, y = 0.5 * y_quart - 1, s = "({rk})".format(rk = data["Luck Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_l = patches.Rectangle((3 * x_quart, 0 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Luck Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_l)
    
    #SOS EM
    ax.text(x = 0.5 * x_quart, y = 0.5 * y_quart, s = data["Opp EM"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 0.5 * x_quart, y = 0.5 * y_quart + 1, s = "SOS", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 0.5 * x_quart, y = 0.5 * y_quart - 1, s = "({rk})".format(rk = data["Opp EM Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_sos = patches.Rectangle((0 * x_quart, 0 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Opp EM Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_sos)
    
    #SOS offense
    ax.text(x = 1.5 * x_quart, y = 0.5 * y_quart, s = data["Opp Off"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 1.5 * x_quart, y = 0.5 * y_quart + 1, s = "SOS (O)", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 1.5 * x_quart, y = 0.5 * y_quart - 1, s = "({rk})".format(rk = data["Opp Off Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_osos = patches.Rectangle((1 * x_quart, 0 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Opp Off Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_osos)
    
    #SOS defense
    ax.text(x = 2.5 * x_quart, y = 0.5 * y_quart, s = data["Opp Def"], va = "center", ha = "center", fontsize = "xx-large")
    ax.text(x = 2.5 * x_quart, y = 0.5 * y_quart + 1, s = "SOS (D)", va = "center", ha = "center", weight = "bold", fontsize = "x-large")
    ax.text(x = 2.5 * x_quart, y = 0.5 * y_quart - 1, s = "({rk})".format(rk = data["Opp Def Rk"]), va = "center", ha = "center", fontsize = "large")
    rect_dsos = patches.Rectangle((2 * x_quart, 0 * y_quart), width = x_quart, height = y_quart, ec = "none", fc = cmap(norm(int(data["Opp Def Rk"]))), alpha = .6, zorder = -1)
    ax.add_patch(rect_dsos)
    
    #Turn off grid and axes
    ax.axis("off")
    
    #Title
    ax.text(x = x_left + .5, y = y_upper - 1, s = "KenPom Metrics", va = "center", ha = "left", fontsize = 25, weight = "bold")
    return ax
    
def makeStatsTable(stats: dict, fig = None, ax = None):
    """Generates the statistics table given a dict of correctly formatted stats. Returns the mpl ax w the table."""
    if (ax is None or fig is None):
        #Declare figure
        fig, ax = plt.subplots(figsize = (5, 7.5))
    
    #Set table size
    rows = 9
    cols = 5
    
    #Set borders
    x_left = -.1
    x_right = cols - 1.5
    
    y_lower = -.5
    y_upper = rows
    
    #Add padding
    ax.set_xlim(x_left, x_right)
    ax.set_ylim(y_lower , y_upper)
    
    #Fill in table
    for r in range(rows):
        data = stats[r]
        
        #Stat name
        ax.text(x = 0, y = r, s = data["Stat"], va = "center", ha = "left", weight = "bold", fontsize = "xx-large")
        
        #Stat
        ax.text(x = .75, y = r, s = data["Num"], va = "center", ha = "left", fontsize = "xx-large")
        
        #Rk
        ax.text(x = 1.2, y = r, s = "({rk})".format(rk = data["Rk"]), va = "center", ha = "left", fontsize = "x-large")
        
        #Opp Stat
        ax.text(x = 2.25, y = r, s = data["Opp"], va = "center", ha = "left", fontsize = "xx-large")
        
        #Opp Rk
        ax.text(x = 2.65, y = r, s = "({rk})".format(rk = data["Opp Rk"]), va = "center", ha = "left", fontsize = "x-large")
    
    #Add category titles
    ax.text(x = 1.25, y = rows - .25, s = "Own Per Game (Rk)", va = "center", ha = "center", weight = "bold", fontsize = "xx-large")
    ax.text(x = 2.75, y = rows - .25, s = "Opp Per Game (Rk)", va = "center", ha = "center", weight = "bold", fontsize = "xx-large")
    
    #Add table lines
    for r in range(1, rows):
        ax.plot([x_left, x_right], [r - .5, r - .5], ls = ":", lw = ".5", c = "k")
        
    ax.plot([x_left, x_right], [rows - .5, rows - .5], lw = ".5", c = "k")
    
    #Own/Opp separator
    ax.plot([cols / 2 - .5, cols / 2 - .5], [y_lower, y_upper], lw = ".5", c = "k")
    
    #Label separator
    ax.plot([.5, .5], [y_lower, y_upper], ls = ":", lw = ".5", c = "k")
    
    #Outline
    ax.plot([x_left, x_left], [y_lower, y_upper], lw = 1.5, c = "k")
    ax.plot([x_right, x_right], [y_lower, y_upper], lw = 1.5, c = "k")
    ax.plot([x_left, x_right], [y_lower, y_lower], lw = 1.5, c = "k")
    ax.plot([x_left, x_right], [y_upper, y_upper], lw = 1.5, c = "k")
    
    #Color based on rank
    norm = mpl.colors.Normalize(1, 351)
    cmap = mpl.colors.LinearSegmentedColormap.from_list("gr", ["g", "w", "r"], N = 351)
    for r in range(rows):
        data = stats[r]
        
        rect = patches.Rectangle((.5, r - .5), width = 1.5, height = 1, ec = "none", fc = cmap(norm(int(data["Rk"][:-2]))), alpha = .6, zorder = -1)
        ax.add_patch(rect)
        
        opp_rect = patches.Rectangle((2, r - .5), width = 1.5, height = 1, ec = "none", fc = cmap(norm(int(data["Opp Rk"][:-2]))), alpha = .6, zorder = -1)
        ax.add_patch(opp_rect)
        
    #Turn off grid and axes
    ax.axis("off")

    return ax
    
def makeGameLog(games: dict, fig = None, ax = None):
    """Generates the game log visual given a dict of game info. Returns the mpl ax w the table."""
    if (ax is None or fig is None):
        #Declare figure
        fig, ax = plt.subplots(figsize = (20/3, 15 + 20/3))
    
    #Convert net pts into a list
    data = [gm["Net Pts"] for gm in games]
    data.reverse()
    ypos = np.arange(len(data))
    
    #List of colors based on if win or loss
    colors = ["g" if gm["Net Pts"] > 0 else "r" for gm in games]
    colors.reverse()
    
    #Make bar chart
    ax.barh(ypos, width = data, height = 0.6, ec = "k", color = colors)
    
    #Set axes
    max_net = max(abs(min(data)), max(data))
    ax.set_xlim(-max_net * 1.3, max_net * 1.3)
    ax.set_ylim(-1, len(data))
    
    #Turn off y axis
    plt.yticks([])
    
    #Add opponent logo, score for each game
    strings = []
    for gm in games:
        win = int(gm["Pts"]) > int(gm["Opp Pts"])
        score = "{own} - {opp} [{loc}]".format(own = gm["Pts"], opp = gm["Opp Pts"], loc = gm["Loc"])
        net = gm["Net Pts"]
        fg = "FG%: {own}-{opp}".format(own = gm["FG%"], opp = gm["Opp FG%"])
        to = "TO: {own}-{opp}".format(own = gm["TO"], opp = gm["Opp TO"])
        opponent = gm["Opp"]
        game_data = {"WN": win,
                     "SC": score,
                     "NT": net,
                     "FG%": fg,
                     "TO": to,
                     "OP": opponent}
        
        strings.append(game_data)
    
    strings.reverse()
    
    y_pos = 0
    for gm in strings:
        #Set position and alignment
        x_pos = -max_net/30 if gm["WN"] else max_net/30
        align = "right" if gm["WN"] else "left"
        logo_offset = max_net / 8 if gm["WN"] else - max_net / 6
        
        #Add text for stats
        ax.text(x = x_pos, y = y_pos + .15, s = gm["SC"], va = "center", ha = align, weight = "bold", fontsize = "x-large")
        ax.text(x = x_pos, y = y_pos - .15, s = "{fg}, {to}".format(fg = gm["FG%"], to = gm["TO"]), va = "center", ha = align, fontsize = "medium")
        
        #Add logos
        mgr = logoManager("./logos/team_ids.csv")
        ab = AnnotationBbox(mgr.getLogo(gm["OP"].lower(), zm = .064), (gm["NT"] + logo_offset, y_pos), frameon = False)
        ax.add_artist(ab)
        
        #Increment y position for next game
        y_pos += 1
    
    ax.set_title("Game Log", loc = "center", fontsize = 15, weight = "bold")
    return ax

def makeScorecard(tm_1: str, tm_2: str, cbbr_1: dict, cbbr_2: dict, kp_1: dict, kp_2: dict, log_1: dict, log_2: dict):
    """Creates the entire scorecard for a matchup given team names and stat dictionaries. Returns and saves a figure of the scorecard."""
    #Initialize logo manager
    mgr = logoManager("./logos/team_ids.csv")    
    
    #Get record data from game log
    recs_1 = fm.getRecords(log_1)
    recs_2 = fm.getRecords(log_2)
    
    #Define a figure and gridspec
    fig = plt.figure(figsize = (28, 21.67))
    gs = mpl.gridspec.GridSpec(4, 4, wspace = .08, left = .05, right = .95)
    
    ## --- Leftmost Column (Team 1 Stats) --- ##
    
    #Make subgrid
    gs_ll = mpl.gridspec.GridSpecFromSubplotSpec(4, 1, gs[:, 0], height_ratios = [1, 1, 3, 7/3], hspace = .1)
    
    #Define axes
    logo_1_ax = fig.add_subplot(gs_ll[0])
    text_1_ax = fig.add_subplot(gs_ll[1])
    cbbr_1_ax = fig.add_subplot(gs_ll[2])
    kp_1_ax = fig.add_subplot(gs_ll[3])
    
    #Add logo to axis
    ab_1 = AnnotationBbox(mgr.getLogo(tm_1, zm = .35), (.5, .5), frameon = False)
    logo_1_ax.add_artist(ab_1)
    logo_1_ax.set_axis_off()
    
    #Format strings
    nm_1 = tm_1.upper()
    rec_1 = "{w} - {l} ({p})".format(w = recs_1["W"], l = recs_1["L"], p = round(recs_1["%"], 3))
    hrec_1 = "{w}-{l} ({p})".format(w = recs_1["Hm W"], l = recs_1["Hm L"], p = round(recs_1["Hm %"], 3))
    rrec_1 = "{w}-{l} ({p})".format(w = recs_1["Rd W"], l = recs_1["Rd L"], p = round(recs_1["Rd %"], 3))
    nrec_1 = "{w}-{l} ({p})".format(w = recs_1["Nt W"], l = recs_1["Nt L"], p = round(recs_1["Nt %"], 3))
    
    #Add text to axes
    text_1_ax.text(x = .5, y = 1.0, s = nm_1, fontsize = 35, weight = "bold", va = "center", ha = "center")
    text_1_ax.text(x = .5, y = .75, s = rec_1, fontsize = 35, va = "center", ha = "center")    
    text_1_ax.text(x = .0, y = .50, s = "Home: ", fontsize = 30, va = "center", ha = "left")
    text_1_ax.text(x = 1, y = .50, s = hrec_1, fontsize = 30, va = "center", ha = "right")
    text_1_ax.text(x = .0, y = .25, s = "Road: ", fontsize = 30, va = "center", ha = "left")
    text_1_ax.text(x = 1, y = .25, s = rrec_1, fontsize = 30, va = "center", ha = "right")
    text_1_ax.text(x = .0, y = 0.0, s = "Neutral: ", fontsize = 30, va = "center", ha = "left")
    text_1_ax.text(x = 1, y = 0.0, s = nrec_1, fontsize = 30, va = "center", ha = "right")
    text_1_ax.set_axis_off()
    
    #Add graphs to axes
    makeStatsTable(cbbr_1, fig, cbbr_1_ax)
    makeKenPomTable(kp_1, fig, kp_1_ax)
    
    ## --- Leftmidd Column (Team 1 Games) --- ##
    gs_l = mpl.gridspec.GridSpecFromSubplotSpec(1, 1, gs[:, 1])
    log_1_ax = fig.add_subplot(gs_l[0])
    makeGameLog(log_1, fig, log_1_ax)
    
    
    ## --- Rghtmidd Column (Team 2 Games) --- ##
    gs_r = mpl.gridspec.GridSpecFromSubplotSpec(1, 1, gs[:, 2])
    log_2_ax = fig.add_subplot(gs_r[0])
    makeGameLog(log_2, fig, log_2_ax)
    
    ## --- Rghtmost Column (Team 2 Stats) --- ##
    
    #Make subgrid
    gs_rr = mpl.gridspec.GridSpecFromSubplotSpec(4, 1, gs[:, 3], height_ratios = [1, 1, 3, 7/3], hspace = .1)
    
    #Define axes
    logo_2_ax = fig.add_subplot(gs_rr[0])
    text_2_ax = fig.add_subplot(gs_rr[1])
    cbbr_2_ax = fig.add_subplot(gs_rr[2])
    kp_2_ax = fig.add_subplot(gs_rr[3])
    
    #Add logo to axis
    ab_2 = AnnotationBbox(mgr.getLogo(tm_2, zm = .35), (.5, .5), frameon = False)
    logo_2_ax.add_artist(ab_2)
    logo_2_ax.set_axis_off()
    
    #Format strings
    nm_2 = tm_2.upper()
    rec_2 = "{w} - {l} ({p})".format(w = recs_2["W"], l = recs_2["L"], p = round(recs_2["%"], 3))
    hrec_2 = "{w}-{l} ({p})".format(w = recs_2["Hm W"], l = recs_2["Hm L"], p = round(recs_2["Hm %"], 3))
    rrec_2 = "{w}-{l} ({p})".format(w = recs_2["Rd W"], l = recs_2["Rd L"], p = round(recs_2["Rd %"], 3))
    nrec_2 = "{w}-{l} ({p})".format(w = recs_2["Nt W"], l = recs_2["Nt L"], p = round(recs_2["Nt %"], 3))
    
    #Add text to axes
    text_2_ax.text(x = .5, y = 1.0, s = nm_2, fontsize = 35, weight = "bold", va = "center", ha = "center")
    text_2_ax.text(x = .5, y = .75, s = rec_2, fontsize = 35, va = "center", ha = "center")    
    text_2_ax.text(x = .0, y = .50, s = "Home: ", fontsize = 30, va = "center", ha = "left")
    text_2_ax.text(x = 1, y = .50, s = hrec_2, fontsize = 30, va = "center", ha = "right")
    text_2_ax.text(x = .0, y = .25, s = "Road: ", fontsize = 30, va = "center", ha = "left")
    text_2_ax.text(x = 1, y = .25, s = rrec_2, fontsize = 30, va = "center", ha = "right")
    text_2_ax.text(x = .0, y = 0.0, s = "Neutral: ", fontsize = 30, va = "center", ha = "left")
    text_2_ax.text(x = 1, y = 0.0, s = nrec_2, fontsize = 30, va = "center", ha = "right")
    text_2_ax.set_axis_off()
    
    #Add graphs to axes
    makeStatsTable(cbbr_2, fig, cbbr_2_ax)
    makeKenPomTable(kp_2, fig, kp_2_ax)
    
    #Add vertical line between the two
    line = plt.Line2D((.4995, .4995), (.01, .99), color = "k", lw = 3, ls = ":")
    fig.add_artist(line)
    
    gs.tight_layout(fig)
    
    plt.savefig(f"{tm_1} vs {tm_2}.png")
    
    return fig
  