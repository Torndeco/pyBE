pyBE
====

Python Battleye Log + Rcon Tools


A small group of simple python scripts to help with arma3.

pyBE_chatbot.py:
  * Simple rcon bot code unfinished, framework is in place.
    Does nothing atm...
    
pyBE_raw.py
  * Simple python script to send server an rcon command.
      i.e python pyBE_raw.py "say -1 Server Restart 10mins"
      
pyBE_rawFile.py
  * Similar to pyBE_raw.py, but parsers a text file to send server multiple rcon commands.
      i.e python pyBE_rawFile.py "examples/rawFile.example"

Todo:
Upload newer simple pyBEscanner here + close old repo
      

Requirements
	Python 2.7


Thanks for 
  *People mentioned for help/work on pyBEscanner
  *Nanomo for creating the c# app for kicking players
  *k4n30 for updating the rules & finding my mistakes
  *ziellos2k for creating the BattleNET C# library


Major thanks for 

  http://www.bigbrotherbot.net/
  Using there gplv2 python rcon code for arma
  There bot is alot more advanced for a chatbot + has various plugins.
  Also supports multiple games, u should check it out


