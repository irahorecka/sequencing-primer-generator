# Sequencing-Primer-Generator
A python tool that will batch generate optimal DNA primers for Sanger sequencing. The output .xlsx file is directly compatible for bulk input into IDT Oligo Entry.

## Introduction
In this repository, there are two files: Primerwalk_GUI.py and Primerwalk.py. Primerwalk_GUI.py is a front end desktop application that communicates with the backend Primerwalk.py python file. This repository would be most helpful for molecular biologist who frequently conduct full plasmid sequencing. 

There are licensed softwares that provide primer synthesis capabilities, but none that can synthesize appropriate forward and reverse primers in batch. The exported files of Primerwalk.py is compatible for single tube ordering and 96-well plate ordering from IDT (idtdna.com).

Single tube ordering form: https://www.idtdna.com/site/order/oligoentry
96-well plate ordering form: https://www.idtdna.com/site/order/plate/index/pico/5647

The only changes one must make when using this code is modifying the directory in Primerwalk_GUI.py (var 'main_dir'). Please ensure that both Primerwalk_GUI.py and Primerwalk.py are located in the same directory. 


<img src="https://i.imgur.com/nKVMKuh.png" alt="alt text" width="500" height="400">
