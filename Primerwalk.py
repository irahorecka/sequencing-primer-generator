#2019-07-22: script to generate primer walk for large DNA sequence - order form for IDT generated
#TO_DO: Add both plate and tube IDT order generator. 
#Communicates with frontend file for GUI interface (Primerwalk_GUI.py)
#Update: Now reads .csv file 'sequence_file.csv' for input - bulk primer synthesis capacity in place with new directory generated per day.
#   name of vector to be synthesized
#   full vector sequence string and segment of interest (NT) whether uppercase or lowercase, does not matter
#   bp break you would like per primer generation (common is 300 bp)
#   nM concentration of primer to be ordered on IDT

#   Primer selction criteria available on: https://dnacore.mgh.harvard.edu/new-cgi-bin/site/pages/sequencing_pages/primer_design.jsp;jsessionid=633F7917850FBFDF707F67F872267D71 
#   IDT website for oligo synthesis: https://www.idtdna.com/site/order/oligoentry

import csv 
import datetime
import pandas as pd
import os.path
import shutil
import Primerwalk_GUI

global order_type

seq_table = {
    'A':'T',
    'G':'C',
    'C':'G',
    'T':'A'
}

well_list = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 
'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 
'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 
'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 
'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 
'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 
'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 
'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 
'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 
'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 
'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 
'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12']


# == FUNCTION ==

#complement function for sequence
def complement(seq):
    comp = ''
    for i in seq:
        comp += seq_table.get(i.upper(), '0')
    return comp
#reverse complement function for sequence
def r_complement(seq):
    comp = ''
    for i in seq:
        comp += seq_table.get(i.upper(), '0')
    return comp[::-1]

#checks for secondary primer binding sites
def nonspecific_looker(fprimer, rprimer, full_seq):
    full_seq = full_seq.upper()
    reverse_full = r_complement(full_seq)
    for i in fprimer:
        if full_seq.count(i) > 1 or reverse_full.count(i) > 1:
            return 'FAIL'
        else:
            pass
    for i in rprimer:
        if full_seq.count(i) > 1 or reverse_full.count(i) > 1:
            return 'FAIL'
        else:
            pass
    return 'PASS'


# == CLASS  ==
    
#write fprimer and rprimer sequences to .csv file compatable with IDT oligoDNA bulk input
class IDT_CSV:
    def __init__(self, fprimer_l, rprimer_l, filename):
        self.fprimer_l = fprimer_l
        self.rprimer_l = rprimer_l
        self.filename = filename
        self.csv_tube_name = f'IDT_Tube_{filename}'
        self.csv_plate_name = f'IDT_Plate_{filename}'
        self.primer_conc = primer_conc
        self.title = f"{str(self.filename)}.csv"
        self.idt_tube_list = ['Name,Sequence,Scale,Purification']
        self.idt_plate_list = ['Well Position,Name,Sequence']

    def write_tube_order(self, primer_conc):
        for i in self.fprimer_l:
            self.idt_tube_list.append(f"{f'{self.filename}_{self.fprimer_l.index(i)+1}_f'},{i},{self.primer_conc}nm,STD \n")
        for i in self.rprimer_l:
            self.idt_tube_list.append(f"{f'{self.filename}_{self.rprimer_l.index(i)+1}_r'},{i},{self.primer_conc}nm,STD \n")
        with open(self.title,'w',newline = '') as csv_tube_file:
            writer = csv.writer(csv_tube_file, delimiter = ',')
            writer.writerows([i.split(',') for i in self.idt_tube_list])
        csv_tube_file.close()

    def write_plate_order(self):
        count = -1
        for i in self.fprimer_l:
            count += 1
            self.idt_plate_list.append(f"{well_list[count]},{f'{self.filename}_{self.fprimer_l.index(i)+1}_f'},{i} \n")
        for i in self.rprimer_l:
            count += 1
            self.idt_plate_list.append(f"{well_list[count]},{f'{self.filename}_{self.rprimer_l.index(i)+1}_r'},{i} \n")
        with open(self.title,'w',newline = '') as csv_plate_file:
            writer = csv.writer(csv_plate_file, delimiter = ',')
            writer.writerows([i.split(',') for i in self.idt_plate_list])
        csv_plate_file.close()

    def csv_to_excel(self, order_type):
        path = f'{os.getcwd()}/{self.title}'
        if order_type == 'tube':
            pd.read_csv(path).to_excel(f'{str(self.csv_tube_name)}.xlsx', index = False)
        elif order_type == 'plate':
            pd.read_csv(path).to_excel(f'{str(self.csv_plate_name)}.xlsx', index = False)
        os.remove(path)

    #write .csv file for Tm - could be interesting but not in production
    def write_Tm(self):
        pass


#checking appropriate primer selection rules:
#1: GC percentage should be no less than 45% and no greater than 55%
#2: Melt temp of primer should be greater than 50C and less than 65C
#3: There should be no more than 4 homopolymer sequences in the primer
#4: The 3' end of every primer should be a 'G' or 'C'
class Rule:
    def __init__(self, prim_sequence):
        self.p_seq = prim_sequence
    
    def GC_perc(self):
        GC = self.p_seq.count('G') + self.p_seq.count('C')
        len_seq = len(self.p_seq)
        if GC > 0.45*(len_seq) and GC < 0.55*(len_seq):
            return True
        else:
            return False

    def homo_polymer(self):
        if 'CCCC' in self.p_seq:
            return False
        elif 'AAAA' in self.p_seq:
            return False
        elif 'GGGG' in self.p_seq:
            return False
        elif 'TTTT' in self.p_seq:
            return False
        else:
            return True

    def last_gc(self):
        if (self.p_seq[-1] == 'G' or self.p_seq[-1] == 'C') and (self.p_seq[-2] == 'G' or self.p_seq[-2] == 'C'):
            return True
        else:
            return False

    def TM(self):
        GC = self.p_seq.count('G') + self.p_seq.count('C')
        TA = self.p_seq.count('T') + self.p_seq.count('A')
        Tm = 64.9 + 41*((GC - 16.4)/(GC + TA))
        if Tm > 50 and Tm < 65:
            return True 
        else:
            return False


class Primer_Check:
    def __init__(self, seq, count):
        self.seq = seq
        self.count = count

    #generates appropriate 22bp forward primer with test cases in Rule class for each instance of potential forward primer
    def f_check(self, fprimer_l):
        fprimer = self.seq[self.count-50:self.count-28].upper()
        fp_test = Rule(fprimer)
        try:
            if fp_test.GC_perc() and fp_test.TM() and fp_test.homo_polymer() and fp_test.last_gc() == True:
                fprimer_l.append(fprimer)
                return fprimer_l
            else:
                self.count -= 1
                self.f_check(fprimer_l)
        except RecursionError:
            fprimer_l.append('FAIL')
            return fprimer_l

    #generates appropriate 22bp reverse primer with test cases in Rule class for each instance of potential reverse primer
    def r_check(self, rprimer_l):
        rprimer = r_complement(seq[self.count+28:self.count+50]).upper()
        rp_test = Rule(rprimer)
        try:
            if rp_test.GC_perc() and rp_test.TM() and rp_test.homo_polymer() and rp_test.last_gc() == True:
                rprimer_l.append(rprimer)
                return rprimer_l
            else:
                self.count -= 1
                self.r_check(rprimer_l)
        except RecursionError:
            rprimer_l.append('FAIL')
            return rprimer_l


class Primer_Seek:
    def __init__(self, seq, bp):
        self.seq = seq
        self.bp = bp

    #appends appropriate primers (both forward and reverse) to specified list
    def primer_find(self):
        count = 0
        fprimer_l = []
        rprimer_l = []
        for i in self.seq:
            count += 1
            if count % self.bp == 0:
                Primer = Primer_Check(seq, count)
                fprimer_l.append(Primer.f_check(fprimer_l))
                rprimer_l.append(Primer.r_check(rprimer_l))
        fprimer_l = [i for i in fprimer_l if type(i) != list and i != None]
        rprimer_l = [i for i in rprimer_l if type(i) != list and i != None]
        return fprimer_l, rprimer_l

    #if there is an unsuccessful attempt to make a primer, the search bp value is incremented by 10
    def primer_synthesis(self):
        fprimer, rprimer = self.primer_find()
        while 'FAIL' in fprimer or 'FAIL' in rprimer:
            self.bp = self.bp + 10
            fprimer, rprimer = self.primer_find()
        return fprimer, rprimer


#read input file 'sequence_file.csv' for batch primer sequence generation
seq_file = pd.read_csv('sequence_file.csv')
new_direct = f'{os.getcwd()}/{datetime.date.today()}'
#if the directory path you want to make is not there, make it - override if current directory there.
if os.path.exists(new_direct):
    shutil.rmtree(new_direct)
os.makedirs(new_direct)
os.chdir(new_direct)

for index, row in seq_file.iterrows():
    filename = row['Name']
    full_seq = row['Full Sequence']
    seq = row['Primer Walk']
    bp = row['BP Gap']
    primer_conc = row['Primer conc. (nM)']

    #checks for sequences for every row in 'sequence_file.csv'
    Seek = Primer_Seek(seq, bp)
    fprimer, rprimer = Seek.primer_synthesis()
    status = nonspecific_looker(fprimer, rprimer, full_seq)
    while status == 'FAIL':
        bp += 10
        Seek = Primer_Seek(seq, bp)
        fprimer, rprimer = Seek.primer_synthesis()
        status = nonspecific_looker(fprimer, rprimer, full_seq)
    fprimer = list(set(fprimer))
    rprimer = list(set(rprimer))

    write_to_file = IDT_CSV(fprimer, rprimer, filename)
    if order_type.lower() == 'tube':
        write_to_file.write_tube_order(primer_conc)
    elif order_type.lower() == 'plate':
        write_to_file.write_plate_order()
    write_to_file.csv_to_excel(order_type)

#print to terminal if script executes successfully
print(f'\n-- COMPLETE --\nPlease check folder: {datetime.date.today()}\n')
