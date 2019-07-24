# Sequencing-Primer-Generator
A python tool that will batch generate optimal DNA primers for Sanger sequencing. The output .xlsx file is directly compatible for bulk input into IDT Oligo Entry.

## Introduction
In this repository, there are two files: Primerwalk_GUI.py and Primerwalk.py. Primerwalk_GUI.py is a front end desktop application that communicates with the backend Primerwalk.py python file. This repository would be most helpful for molecular biologist who frequently conduct full plasmid sequencing. <br>
<br>
*Primerwalk_GUI.py*<br>
<img src="https://i.imgur.com/nKVMKuh.png" alt="alt text" width="500" height="400"> <br><br>

There are licensed softwares that provide primer synthesis capabilities, but none that can synthesize appropriate forward and reverse primers in batch. The exported files of Primerwalk.py is compatible for single tube ordering and 96-well plate ordering from IDT (idtdna.com).<br>

Single tube ordering form: https://www.idtdna.com/site/order/oligoentry <br>
96-well plate ordering form: https://www.idtdna.com/site/order/plate/index/pico/5647
<br>

## How to use

### Python packages to install
- pandas
- kivy
- csv
- shutil

### Input file formatting

The only changes one must make when using this code is modifying the directory in Primerwalk_GUI.py (var 'main_dir'). Please ensure that both Primerwalk_GUI.py and Primerwalk.py are located in the same directory. 

Please make a .csv file named 'sequence_file.csv'. Store this file in the same directory as Primerwalk_GUI.py and Primerwalk.py. Note: the naming of this file is *critical* for Primerwalk.py to parse.<br>
Please adhere precisely to the format outlined below (note: the headers are case sensitive - please adhere as exactly as listed): <br>
<br>
*sequence_file.csv*<br>
<img src="https://i.imgur.com/jCFubfz.png" alt="alt text"> <br><br>

**Name**: Name of plasmid / DNA sample<br>
**Full Sequence**: Full sample DNA sequence<br>
**Primer Walk**: Sequence of DNA to be sequenced (this could equate to Full Sequence, if desired)<br>
**BP Gap**: Base pair gap between primers (usually, max is 500 bp before sequence resolution is compromised)<br>
**Primer conc. (nM)**: Primer concentration to order (usually 25nM or 100nM) - to be used for single tube ordering<br>
<br>

### Running Primerwalk_GUI.py on terminal

Navigate through your terminal to the directory in which Primerwalk_GUI.py is installed.<br>
Type: *python Primerwalk_GUI.py*<br>
The following desktop application should appear:<br>
<br>
<img src="https://i.imgur.com/nKVMKuh.png" alt="alt text" width="500" height="400"> <br><br>
#### Choosing Single Tubes:

If you would like to order single tubes of primers from IDT, click the 'SINGLE TUBES' button on the desktop application. If executed correctly, the desktop application would look like this: <br><br>

<img src="https://i.imgur.com/hZEgnl0.png" alt="alt text" width="500" height="400"> <br><br>
A new directory with the name of today's date will be created in your main directory (i.e. the directory with your Primerwalk_GUI.py, Primerwalk.py, and sequence_file.csv files). Inside the directory, you will find unique .xlsx files for every plasmid you inputted in the 'sequence_file.csv' file. <br>
Each file will have the following naming format: *IDT_Tube_(plasmid name).xlsx*<br><br>

<img src="https://i.imgur.com/jCFubfz.png" alt="alt text"> <br><br>

Please upload this file directly to this website (https://www.idtdna.com/site/order/oligoentry) and perform the following tasks: <br><br>
*Click on button 'Bulk Input' in center of webpage (blue button)*<br>
<img src="https://i.imgur.com/ReISAAS.png" alt="alt text"> <br><br>
*Click on button 'Choose File' to upload your .xlsx ordering forms*<br>
<img src="https://i.imgur.com/m9CKjG8.png" alt="alt text"> <br><br>
All required fields in the ordering form should automatically fill. Proceed to checkout if satisfied with input.<br><br>

#### Choosing 96-Well Plate:
