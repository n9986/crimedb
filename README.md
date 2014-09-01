crimedb
=======

## Introduction

This is a CLI application which helps manage mafia.


To run:

	pip install -r requirements.txt
	python fbi.py

After running, you will be dropped into a shell-like environment where commands can be issued to manipulate the database.

---

## Commands



---

## Sample


Consider the following decommissioning and recommissioning cycle:

	$FBI> tree -i 1
	Danilo Mazzanti [1]
	  +--Simone Endrizzi [3]
	  |  +--Nunzio Marchesi [9]
	  |  |  +--Viviano Pisano [12]
	  |  +--Giacobbe Milanesi [10]
	  |     +--Gherardo Fiorentini [13]
	  |     +--Giacinto Genovesi [14]
	  +--Alfonsino Lucchese [6]
	  +--Bonifacio Arcuri [8]
	
	$FBI> decommission -i 10 -s jailed
	Done deactivating Giacobbe Milanesi [10]
	$FBI> tree -i 1
	Danilo Mazzanti [1]
	  +--Simone Endrizzi [3]
	  |  +--Nunzio Marchesi [9]
	  |     +--Viviano Pisano [12]
	  |     +--Gherardo Fiorentini [13]
	  |     +--Giacinto Genovesi [14]
	  +--Alfonsino Lucchese [6]
	  +--Bonifacio Arcuri [8]
	
	$FBI> recommission -i 10 -s active
	Done reactivating Giacobbe Milanesi [10]
	$FBI> tree -i 1
	Danilo Mazzanti [1]
	  +--Simone Endrizzi [3]
	  |  +--Nunzio Marchesi [9]
	  |  |  +--Viviano Pisano [12]
	  |  +--Giacobbe Milanesi [10]
	  |     +--Gherardo Fiorentini [13]
	  |     +--Giacinto Genovesi [14]
	  +--Alfonsino Lucchese [6]
	  +--Bonifacio Arcuri [8]
	
	$FBI> 
	
	
	
----

### Design Approach

Consider the following sample mafia data:

![Mafia Organization Chart](static/img/chart.png)



