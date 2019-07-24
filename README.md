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

The only changes one must make when using this code is modifying the directory in Primerwalk_GUI.py (var 'main_dir'). Please ensure that both Primerwalk_GUI.py and Primerwalk.py are located in the same directory. 

Please make a .csv file named 'sequence_file.csv'. Note: the naming of this file is critical for Primerwalk.py to parse.<br>
Please adhere precisely to the format outlined below (note: the headers are case sensitive - please adhere as exactly as listed): <br>

<img src="https://i.imgur.com/jCFubfz.png" alt="alt text"> <br><br>

**Name**: Name of plasmid / DNA sample<br>
**Full Sequence**: Full sample DNA sequence<br>
**Primer Walk**: Sequence of DNA to be sequenced (this could equate to Full Sequence, if desired)<br>
**BP Gap**: Base pair gap between primers (usually, max is 500 bp before sequence resolution is compromised)<br>
**Primer conc. (nM)**: Primer concentration to order (usually 25nM or 100nM) - to be used for single tube ordering<br>
