# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: YOUR NAME HERE
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from random import *
from load import load_seq

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    
    result = ""
    
    """Converts DNA into amino acids"""
    for i in range(len(dna) / 3):        #separates dna into groups of 3
        current_codon = dna[i*3:i*3+3]
        for j in range(len(codons)):            #looks through list of codons
            for k in range(len(codons[j])):
                if codons[j][k] == current_codon: 
                    result += aa[j]
                    break #this ends the iteration if the codon was identified
                            
    return result

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    
    dna1 = 'TATTACTAATAGTGACATCACCAACAGAATAACAAAAA'
    dna2 = 'CTAGCCGAGCTAGAGTCA'
    
    print "input: " + dna1 + ", expected output: YY|||HHQQNNK, actual output: " + coding_strand_to_AA(dna1)
    print "input: " + dna2 + ", expected output: LAELES, actual output: " + coding_strand_to_AA(dna2)        

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """

    reverse_dna = ""
    
    """Computes the complementary DNA sequence"""
    for i in dna:
        if i == 'A':
            reverse_dna = 'T' + reverse_dna
        elif i == 'T':
            reverse_dna = 'A' + reverse_dna
        elif i == 'C':
            reverse_dna = 'G' + reverse_dna
        else: #assuming that the input will always be a valid DNA sequence
            reverse_dna = 'C' + reverse_dna
            
    return reverse_dna
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    dna1 = "ATCGGACTA"
    dna2 = "CTGATCGATCGCTAC"
    
    print "input: " + dna1 + ", expected output: TAGTCCGAT, actual output: " + get_reverse_complement(dna1)
    print "input: " + dna2 + ", expected output: GTAGCGATCGATCAG, actual output: " + get_reverse_complement(dna2)        

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    
    start_ORF = 0
    
    """Finds the start codon"""
    for i in range(len(dna) - 3):
        current_codon = dna[i:i+3]
        if current_codon == 'ATG':
            start_ORF = i
            break
    
    """Finds the end codon (if one exists)"""
    search_range = (len(dna) - start_ORF)/3
    for j in range(search_range): #Divides the ORF into sets of 3
        current_codon = dna[start_ORF + j*3 : start_ORF + j*3 + 3]
        if current_codon == 'TAG' or current_codon == 'TAA' or current_codon == 'TGA':
            end_ORF = start_ORF + j*3
            dna = dna[start_ORF:end_ORF]
            break
        
    return dna

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    
    dna1 = "ACTATGACGGCTTGA"
    dna2 = "CGTAGTATGAC"
        
    print "input: " + dna1 + ", expected output: ATGACGGCT, actual output: " + rest_of_ORF(dna1)
    print "input: " + dna2 + ", expected output: CGTAGTATGAC, actual output: " + rest_of_ORF(dna2)        
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    all_ORFs = []
    dna_temp = dna
    frame_temp = ""
    frame_index = 0
    
    """Finds all of the ORFs in the strand"""
    while not dna_temp == "":
        frame_temp = rest_of_ORF(dna_temp)
        all_ORFs.append(frame_temp) #Adds the strand to the list
        frame_index = dna_temp.index(frame_temp) #Finds the index of the frame in the dna strand
        dna_temp = dna_temp[frame_index + len(frame_temp) + 3 : len(dna_temp)]

    return all_ORFs 
    
def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
    
    dna1 = 'AAAAAAATGCGAGATTAG'
    dna2 = 'ATGAGATAGATGGCATAG'
     
    print "input: " + dna1 + ", expected output: ['ATGCGAGAT'], actual output: "
    print find_all_ORFs_oneframe(dna1)
    
    print "input: " + dna2 + ", expected output: ['ATGAGA', 'ATGGCA'], actual output: "
    print find_all_ORFs_oneframe(dna2)
        
        
def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    
    indices_of_ATG = [] #Stores where ATG codons are located
    all_ORFs = []
    ORF = ""
    
    """Finds where all the start codons are located"""
    for i in range(len(dna)-2):
        if dna[i:i+3] == 'ATG':
            indices_of_ATG.append(i)
                        
    """Finds all ORFs starting at each start codon"""
    for j in range(len(indices_of_ATG)):
        start_index = indices_of_ATG[j]
        end_index = len(dna) #If there are incomplete codons (1 or 2 aa's) they are cut off
        
        ORF = find_all_ORFs_oneframe(dna[start_index:end_index])
        all_ORFs.append(ORF[0])
        
    return all_ORFs
        
    
def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    dna1 = "ATGAATGAATG"
    dna2 = "ATATGCGATG"
    
    print "input: " + dna1 + ", expected output: ['ATGAATGAATG', 'ATGAATG', 'ATG'], actual output: "
    print find_all_ORFs(dna1)
    
    print "input: " + dna2 + ", expected output: ['ATGCGATG', 'ATG'], actual output: "
    print find_all_ORFs(dna2)
        
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
     
    dna_complement = get_reverse_complement(dna)
    
    list1 = find_all_ORFs(dna)
    list2 = find_all_ORFs(dna_complement)
    
    list1.extend(list2)
    
    return list1

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    dna1 = "ATGAATACATG"
    dna2 = "ATATGCGCAT"
    
    print "input: " + dna1 + ", expected output: ['ATGAATACATG', 'ATG', 'ATGTATTCAT'], actual output: "
    print find_all_ORFs_both_strands(dna1)
    
    print "input: " + dna2 + ", expected output: ['ATGCGCAT', 'ATGCGCATAT'], actual output: "
    print find_all_ORFs_both_strands(dna2)

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""

    all_ORFs = find_all_ORFs_both_strands(dna)
    longest_strand = ""
    
    for i in all_ORFs:
        if len(i) > len(longest_strand):
            longest_strand = i
            
    return longest_strand
    
def longest_ORF_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """

    dna1 = "ATCGATCGCACGATCGCATCGCATTCGATCGCGATCGCATCG"
    dna2 = "ATCCAGCGACTCGCGAGCATACGCATACGATCGACTCGA"
    
    print "input: " + dna1 + ", expected output: ATGCGATCGCGATCGAATGCGATGCGATCGTGCGATCGAT, actual output: "
    print longest_ORF(dna1)
    
    print "input: " + dna2 + ", expected output: ATGCGTATGCTCGCGAGTCGCTGGAT, actual output: "
    print longest_ORF(dna2)

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
        
    longest_strand = 0        

    for i in range(num_trials):
        rand_dna = list(dna) #Converts dna string into a list
        shuffle(rand_dna) #Shuffles the dna list
        rand_dna = collapse(rand_dna) #Converts the dna back into a string

        rand_longest_ORF = longest_ORF(rand_dna)
                
        if len(rand_longest_ORF) > longest_strand:
            longest_strand = len(rand_longest_ORF)
            
    return longest_strand

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    all_ORFs = find_all_ORFs_both_strands(dna)
    thresh_ORFs = []
    
    for i in all_ORFs:
        if len(i) > threshold:
            amino_i = coding_strand_to_AA(i)
            thresh_ORFs.append(amino_i)
            
    return thresh_ORFs
   
def main():   
    dna = load_seq("./data/X73525.fa")
    threshold = longest_ORF_noncoding(dna, 1500)
    candidate_genes = gene_finder(dna, threshold)
    
main()