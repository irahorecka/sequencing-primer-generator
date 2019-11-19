"""
Backend .py file for Primerwalk_GUI.py
This script generates appropriate forward and reverse
primers for sequences included in the imported .csv
file (sequence_file.csv) and determines tube or 96-plate
layout for ordering on IDT.
"""
import csv
import datetime
import os.path
import shutil
import pandas as pd
import Primerwalk_GUI

global order_type

SEQ_TABLE = {
    'A': 'T',
    'G': 'C',
    'C': 'G',
    'T': 'A'
}

WELL_LIST = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
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


def complement(seq):
    """ Complement function for sequence """
    comp = ''.join([SEQ_TABLE.get(i.upper(), '0') for i in seq])
    return comp


def r_complement(seq):
    """ Reverse complement function for sequence """
    comp = ''.join([SEQ_TABLE.get(i.upper(), '0') for i in seq])
    return comp[::-1]


def nonspecific_looker(fprimer, rprimer, full_seq):
    """ Checks for secondary primer binding sites """
    full_seq = full_seq.upper()
    reverse_full = r_complement(full_seq)
    for i in fprimer:
        if full_seq.count(i) > 1 or reverse_full.count(i) > 1:
            return 'FAIL'
    for i in rprimer:
        if full_seq.count(i) > 1 or reverse_full.count(i) > 1:
            return 'FAIL'
    return 'PASS'


class IDTCSV:
    """
    A class to write fprimer and rprimer sequences to .xlsx file
    compatable with IDT oligoDNA bulk input - either in single tube
    format or 96-well plate format
    """
    def __init__(self, fprimer_l, rprimer_l, filename):
        self.fprimer_l = fprimer_l
        self.rprimer_l = rprimer_l
        self.filename = filename
        self.csv_tube_name = f'IDT_Tube_{filename}'
        self.csv_plate_name = f'IDT_Plate_{filename}'
        self.title = f"{str(self.filename)}.csv"
        self.idt_tube_list = ['Name,Sequence,Scale,Purification']
        self.idt_plate_list = ['Well Position,Name,Sequence']

    def write_tube_order(self, primer_conc):
        """
        A method to write .csv files in single tube format
        """
        for i in self.fprimer_l:
            self.idt_tube_list.append(f"{f'{self.filename}_{self.fprimer_l.index(i)+1}_f'},{i},{primer_conc}nm,STD \n")
        for i in self.rprimer_l:
            self.idt_tube_list.append(f"{f'{self.filename}_{self.rprimer_l.index(i)+1}_r'},{i},{primer_conc}nm,STD \n")
        with open(self.title, 'w', newline='') as csv_tube_file:
            writer = csv.writer(csv_tube_file, delimiter=',')
            writer.writerows([i.split(',') for i in self.idt_tube_list])
        csv_tube_file.close()

    def write_plate_order(self):
        """
        A method to write .csv files in 96-well plate format
        """
        count = -1
        for i in self.fprimer_l:
            count += 1
            self.idt_plate_list.append(f"{WELL_LIST[count]},{f'{self.filename}_{self.fprimer_l.index(i)+1}_f'},{i} \n")
        for i in self.rprimer_l:
            count += 1
            self.idt_plate_list.append(f"{WELL_LIST[count]},{f'{self.filename}_{self.rprimer_l.index(i)+1}_r'},{i} \n")
        with open(self.title, 'w', newline='') as csv_plate_file:
            writer = csv.writer(csv_plate_file, delimiter=',')
            writer.writerows([i.split(',') for i in self.idt_plate_list])
        csv_plate_file.close()

    def csv_to_excel(self, order_type):
        """
        Convert written .csv files, whether in single tube
        format or 96-well plate format, to a .xlsx format
        compatible with IDT upload.
        """
        path = f'{os.getcwd()}/{self.title}'
        if order_type == 'tube':
            pd.read_csv(path).to_excel(f'{str(self.csv_tube_name)}.xlsx', index=False)
        elif order_type == 'plate':
            pd.read_csv(path).to_excel(f'{str(self.csv_plate_name)}.xlsx', index=False)
        os.remove(path)


class Rule:
    """
    A class to validate primers for submission pass four criteria:
    1: GC percentage should be no less than 45% and no greater than 55%
    2: Melt temp of primer should be greater than 50C and less than 65C
    3: There should be no more than 4 homopolymer sequences in the primer
    4: The 3' end of every primer should be a 'G' or 'C'
    """
    def __init__(self, prim_sequence):
        self.p_seq = prim_sequence

    def gc_perc(self):
        """ Check GC percentage in primer """
        _gc = self.p_seq.count('G') + self.p_seq.count('C')
        len_seq = len(self.p_seq)
        return bool(_gc > 0.45*(len_seq) and _gc < 0.55*(len_seq))

    def homo_polymer(self):
        """ Checks for homopolymers (i.e. any consecutive nucleotide
        sequences longer than four nucleotides in length) """
        codon = lambda nt: nt.upper()*4
        for i in 'agct':
            if codon(i) in self.p_seq:
                return False
        return True

    def last_gc(self):
        """ Checks two leading and terminal sequences are either G or C """
        return bool(self.p_seq[-1] == 'G' or self.p_seq[-1] == 'C') and (self.p_seq[-2] == 'G' or self.p_seq[-2] == 'C')

    def temp_melt(self):
        """ Checks melting temperature of primer """
        gc = self.p_seq.count('G') + self.p_seq.count('C')
        ta = self.p_seq.count('T') + self.p_seq.count('A')
        temp_melt = 64.9 + 41*((gc - 16.4)/(gc + ta))
        return bool(temp_melt > 50 and temp_melt < 65)


class PrimerCheck:
    """
    A high level QC class to proccess lower level QC -
    send to file writer if all conditions are
    satisfied for generated primer(s).
    """
    def __init__(self, seq, count):
        self.seq = seq
        self.count = count

    def f_check(self, fprimer_l):
        """
        Generates appropriate 22bp forward primer, passes for QC
        in Rule class.
        """
        fprimer = self.seq[self.count-50:self.count-28].upper()
        fp_test = Rule(fprimer)
        try:
            if fp_test.gc_perc() and fp_test.temp_melt() and fp_test.homo_polymer() and fp_test.last_gc():
                fprimer_l.append(fprimer)
                return fprimer_l
            self.count -= 1
            self.f_check(fprimer_l)
        except RecursionError:
            fprimer_l.append('FAIL')
            return fprimer_l

    def r_check(self, rprimer_l):
        """
        Generates appropriate 22bp reverse primer, passes for QC
        in Rule class.
        """
        rprimer = r_complement(self.seq[self.count+28:self.count+50]).upper()
        rp_test = Rule(rprimer)
        try:
            if rp_test.gc_perc() and rp_test.temp_melt() and rp_test.homo_polymer() and rp_test.last_gc():
                rprimer_l.append(rprimer)
                return rprimer_l
            self.count -= 1
            self.r_check(rprimer_l)
        except RecursionError:
            rprimer_l.append('FAIL')
            return rprimer_l


class PrimerSeek:
    """
    A class to look at the full sequence and generate appropriate
    primers to ship to QC and eventually write to .csv --> .xlsx
    file.
    """
    def __init__(self, seq, bp):
        self.seq = seq
        self.bp = bp

    def primer_find(self):
        """
        Appends appropriate primers (both forward and reverse)
        to specified list
        """
        count = 0
        fprimer_l = []
        rprimer_l = []
        for count in range(len(self.seq)):
            if count % self.bp == 0:
                Primer = PrimerCheck(self.seq, count)
                fprimer_l.append(Primer.f_check(fprimer_l))
                rprimer_l.append(Primer.r_check(rprimer_l))
        primer_l = lambda _direction: [i for i in _direction if not isinstance(i, list) and i is not None]
        fprimer_l = primer_l(fprimer_l)
        rprimer_l = primer_l(rprimer_l)
        return fprimer_l, rprimer_l

    def primer_synthesis(self):
        """
        If there is an unsuccessful attempt to make a primer,
        the search bp value is incremented by 10
        """
        fprimer, rprimer = self.primer_find()
        while 'FAIL' in fprimer or 'FAIL' in rprimer:
            self.bp = self.bp + 10
            fprimer, rprimer = self.primer_find()
        return fprimer, rprimer


def process_csv(order_type):
    """
    Read input file 'sequence_file.csv' for batch primer
    sequence generation - if the directory path you want
    to make is not there, make it - override if directory
    is present.
    """
    seq_file = pd.read_csv('sequence_file.csv')
    new_direct = f'{os.getcwd()}/{datetime.date.today()}'
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

        Seek = PrimerSeek(seq, bp)
        fprimer, rprimer = Seek.primer_synthesis()
        status = nonspecific_looker(fprimer, rprimer, full_seq)
        while status == 'FAIL':
            bp += 10
            Seek = PrimerSeek(seq, bp)
            fprimer, rprimer = Seek.primer_synthesis()
            status = nonspecific_looker(fprimer, rprimer, full_seq)
        fprimer = list(set(fprimer))
        rprimer = list(set(rprimer))

        write_to_file = IDTCSV(fprimer, rprimer, filename)
        if order_type.lower() == 'tube':
            write_to_file.write_tube_order(primer_conc)
        elif order_type.lower() == 'plate':
            write_to_file.write_plate_order()

        write_to_file.csv_to_excel(order_type)


try:
    process_csv(order_type)
    print(f'\n-- COMPLETE --\nPlease check folder: {datetime.date.today()}\n')
except Exception as error:
    print(f'An exception occurred: {error}')
