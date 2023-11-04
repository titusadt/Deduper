#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program for removing PCR duplicates")
    parser.add_argument("-f", "--sam_file", help="to specify the input sam_file")#, required=True)
    parser.add_argument("-u", "--umi_file", help="to specify the input umi file")#, required=True)
    parser.add_argument("-o", "--sam_out", help="to specify the output sam file")#, required=True)
    #parser.add_argument("-d", "--dup_file", help="file to wrint unknown umis")#, required=True)
    return parser.parse_args()

args=get_args() 
sam_file:str =args.sam_file
umi_file:str =args.umi_file
sam_output:str = args.sam_out
#dup_file:str = args.dup_file

def store_umi(umi_file):
    '''this function takes in the known umi file and stores it into a set'''
    umi_set= set()
    with open(umi_file, 'r') as umi:
        for line in umi:
            umi_set.add(line.strip())
    return umi_set

#we dont care about reveerse complemented umis
# def check_umi(umi_set, qname):
#     '''This function checks if umi in qname is in umi_set, write unknowns into file and returns the known Umi'''
#     #get umi 
#     umi_line = re.findall("[ACTGNU]{0,8}",qname)
#     umi = umi_line[len(umi_line)-2]
#     #check if umi not in set and write to unknown file
#     with open(unkown_umi, 'w') as umi_output: 
#         if umi not in umi_set:
#             print(umi)
#             umi_output.write(f'{umi}\n')
#         else:
#             return umi

    #return umi

def check_strandedness(flag):
    '''this function returns a bool based on if the sequence is reversed or not'''
    flag:int =0
    if((flag & 16) == 16):
        #yes reverse complemented on the '-'strand
        return True
    else:
        # + PLUS strand
        return False
    
def adjust_position(position, cigar, strand):
    '''this function uses the cigar string to adjust the position based on strandedness'''
    #new_position =0
    new_p = 0
    #new_count =0
    cigar = re.findall(r'(\d+)([MIDNS])',cigar)
    
    if strand == False:
        for count, group in cigar:
            if cigar[0][1] =='S':
                new_position = position - int(count)
                return new_position
            else:
                return position
    else:
        first_group=True
        for count, group in cigar:
            count = int(count)
            #print(count)
            if first_group and cigar[0][1] == 'S':
                first_group=False
                continue
            if group != 'I':
                #print('working?')
                new_p += count
        #print(f'new count {new_p}')
        adjusted_pos = position + new_p
        return adjusted_pos
    

           

#Dictionary, then check againt the dictionary to see if it is a duplicate
    #key: tuple(chrom, 5' start, strand, umi)
    #value: maybe count
    #first time we see something write it and add a counter
    #when chromosome changes empty dictionary and restart



# def main():
#     '''main function to organize workflow'''
#     #umis = store_umi(umi_file)
#     # print(umis)
#     #creating dictionar to compare duplicates
#     duplicate = 0
#     record =0
#     unknown_umis = 0
#     dup_dict={}
#     with open(sam_file, 'r') as sam, open(sam_output, 'w') as sam_out, open(dup_file, 'w') as dupfile:
#         while True:
#             sam_line1 = sam.readline().strip()
#             #sam_line2 = sam.readline().strip()

#             if sam_line1 == "" :
#                 break
#             #print(sam_line1)
#             #check if the line is a header line and write to output file
#             # if sam_line1.startswith('@'):
#             #     sam_out.write(f'{sam_line1}\n')
#             if sam_line1.startswith('@') :
#                 sam_out.write(f'{sam_line1}\n')
#                 #sam_out.write(f'{sam_line2}\n')
#             else: #else it is not a header line so we can turn the lines into a list and get the columns we need
                
#                 line =sam_line1.split()
#                 #print(sam_line1[3])
#             #get the columns we need for more analysis
#                 line1_qname = line[0]
                
                
                
#                 #getting the correct known Umis
#                 #line1_umi = check_umi(umis, line1_qname)
#                 umi_set = store_umi(umi_file)
#                 umi = line1_qname.split(':')[7]
#                 umi = umi.split()[0]
#                 if umi in umi_set:
#                     umi_exist = umi
#                     line1_flag = line[1]
#                     chromosome = line[2]
#                     line1_position = line[3]
#                     #print(f'position class {type(line1_position)}')
#                     line1_cigar = line[5]
#                     strand = check_strandedness(line1_flag)
#                     #getting the accurate position
#                     position = adjust_position(line1_position, line1_cigar, strand)
#                     #create a tuple that stores all of the duplicate information
#                     duplicate_tuple = (chromosome, umi_exist, strand, position)
#                     chrom_check = True
#                     if chrom_check:
#                         if duplicate_tuple not in dup_dict:
#                             sam_out.write(f'{sam_line1}\n')
#                             dup_dict[duplicate_tuple]=0
#                             #print(f'first {dup_dict}')
#                             record +=1
#                             chrom_check=False
#                     else:
#                         if duplicate_tuple[0] == chromosome:
#                             if duplicate_tuple not in dup_dict:
#                                 sam_out.write(f'{sam_line1}\n')
#                                 dup_dict[duplicate_tuple] =1
#                                 record +=1
#                                 #print(dup_dict)
#                             else:
#                                 dup_dict[duplicate_tuple] +=1
#                                 duplicate+=1
#                                 record+=1
#                                 dupfile.write(f'{sam_line1}\n')
#                         else:
#                             #duplicate +=1
#                             #record+=1
#                             dup_dict = {}
#                 else:
#                     unknown_umis+=1    
#                 #getting the correct strand
#                 #the dictionary is empty so we just assume that that the chromosomes match               
#         print(duplicate)
#         print(record)
#         print(unknown_umis)
def main():
    '''main function to organize workflow'''
    umi_set = store_umi(umi_file)
    # print(umis)
    #creating dictionar to compare duplicates
    duplicate = 0
    record =0
    unknown_umis = 0
    dup_dict={}
    #dup_dict=set()
    prev_chrom =None
    with open(sam_file, 'r') as sam, open(sam_output, 'w') as sam_out:
        while True:
            sam_line1 = sam.readline().strip()

            if sam_line1 == "" :
                break
            if sam_line1.startswith('@') :
                sam_out.write(f'{sam_line1}\n')
                
            else: #else it is not a header line so we can turn the lines into a list and get the columns we need
                
                line =sam_line1.split()
                
            #get the columns we need for more analysis
                line1_qname = line[0]
                chromosome = line[2]
                if chromosome!= prev_chrom:
                    prev_chrom=chromosome
                    dup_dict.clear()
                
                #getting umi information      
                #umi_set = store_umi(umi_file)
                umi = line1_qname.split(':')[7]
                umi = umi.split()[0]
                if umi in umi_set:
                    umi_exist = umi    
                    line1_position = line[3]
                    
                    flag = line[1]
                #getting the correct known Umis
          
                    line1_cigar = line[5]
                    strand = check_strandedness(flag)
                    #getting the accurate position
                    position = adjust_position(int(line1_position), line1_cigar, strand)
                    
                    #duplicate_tuple = (chromosome, umi_exist, strand, position)
                    duplicate_tuple = (umi_exist, strand, position)
                    if duplicate_tuple in dup_dict:
                        duplicate +=1
                        dup_dict[duplicate_tuple]+=1
                        #continue
                    else:
                        sam_out.write(f'{sam_line1}\n')
                        #dup_dict.add(duplicate_tuple)
                        dup_dict[duplicate_tuple]=1
                        record +=1
                else:
                    unknown_umis+=1
                    record+=1
                    #continue
                
    with open('summary.txt', 'w')as summary:   
        summary.write(f'duplicate: {duplicate}\n')
        summary.write(f'Number of reads: {record}\n')
        summary.write(f'Unknown UMIs: {unknown_umis}\n')
        summary.write(f'{chromosome} : {len(dup_dict)}\n')  

if __name__ == "__main__":
    main()

