# mpl_voting_power

### Project for the 2019 ETH Lecture "Math in Politics and Law"

This repository contains the voting data and the source code to the report.

### Sources
> voting data:
> https://www.parlament.ch/de/ratsbetrieb/abstimmungen/abstimmung-nr-xls

> faction data:
> https://www.parlament.ch/de/organe/fraktionen

> faction color:
> https://medium.com/srf-schweizer-radio-und-fernsehen/wie-wir-bei-srf-parteien-einf%C3%A4rben-9f010f80cf62

Steps:
* converting the xls files into csv files using exel
* conveting the csv files to a UTF-8 endcoding
* writing the factions.csv file form fraction data
* parsing the csv files and read the data in memory
* analyse and compute the data
* visualise the results


### Files
* classes.py holds all the class definitions for the project
* PBI.py holds the function to calculate the Banzhaf Voting Power Index
* parser.py holds function to parse data and load it into memory
* plot.py holds some helper function to faster print plots und the party colors
* mathHelper holds mathmatical helper functions
* voting_power.ipynb jupyter notebook with the main programm
