# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:49:07 2024

@author: djmcd
"""

import formatter as fm
import scraper as sc
import visualizer as vs
    
if __name__ == "__main__":
    print("This program generates a matchup card for March Madness games.\n")
    
    #Get the year
    year = input("Enter the tournament year (YYYY): ")
    
    #Get first team's CBBR
    tm1_cbb = input("Enter the first team's name as it appears on sports reference. This is usually just the school name: ")
    cbb_data_1 = sc.readCBBR(tm1_cbb, year)
    
    while (cbb_data_1 == 1):
        print("Hm, that didn't work, try again. If \"state\" is in the team name, it should be written out.\n")
        print("Replace any space with a dash (-).\n")
        tm1_cbb = input("Reenter the first team's name: ")
        cbb_data_1 = sc.readCBBR(tm1_cbb, year)
        
    log_1 = sc.readGameLog(tm1_cbb, year)
   
    #Get first team's kenpom
    tm1_kp = input("Enter the first team's name as it appears on kenpom. This is usually just the school name: ")
    kp_1 = sc.readKenPom(tm1_kp, year)
   
    while (kp_1 == 1):
        print("Hm, that didn't work, try again. If \"state\" is in the team name, it should be \"St.\"\n")
        tm1_kp = input("Reenter the first team's name: ")
        kp_1 = sc.readKenPom(tm1_kp, year)
    
    #Get second team's CBBR
    tm2_cbb = input("Enter the second team's name as it appears on sports reference: ")
    cbb_data_2 = sc.readCBBR(tm2_cbb, year)
    
    while (cbb_data_2 == 1):
        print("Hm, that didn't work, try again. If \"state\" is in the team name, it should be written out.\n")
        print("Replace any space with a dash (-).\n")
        tm2_cbb = input("Reenter the second team's name: ")
        cbb_data_2 = sc.readCBBR(tm2_cbb, year)
   
    log_2 = sc.readGameLog(tm2_cbb, year)
    
    #Get second team's kenpom
    tm2_kp = input("Enter the second team's name as it appears on kenpom: ")
    kp_2 = sc.readKenPom(tm2_kp, year)
    
    while (kp_2 == 1):
        print("Hm, that didn't work, try again. If \"state\" is in the team name, it should be \"St.\"\n")
        tm2_kp = input("Reenter the second team's name: ")
        kp_2 = sc.readKenPom(tm2_kp, year)
        
    #Format CBBR data
    cd1_formatted = fm.formatCBBR(cbb_data_1)
    cd2_formatted = fm.formatCBBR(cbb_data_2)
    
    scorecard = vs.makeScorecard(tm1_kp, tm2_kp, cd1_formatted, cd2_formatted, kp_1, kp_2, log_1, log_2)