# march-madness-scorecards
A python that generates a statistics scorecard for march madness matchups. Scorecards contain easy to read data to help you cut through the noise and make your best bracket.

Running main will prompt you to enter a year and two team names. It will then use data from college basketball reference and kenpom to create a visual scorecard with information on relevant statistics, home and away record, and individual game results.

Known issues and future improvements:
1) Not all teams have logos in the provided logo folder, and some teams have logos but under different names (ex: mississippi state vs mississippi st.)
2) Because of the way it reads kenpom, it only works for teams still in the tournament. Teams not in the tournament won't be recognized when you enter their name.
3) Inputting names is somewhat cumbersome. This will be improved in future iterations.
4) Women's version is in the works.
5) More comprehensive statistics may be included in future versions.
