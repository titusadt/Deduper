#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program for removing PCR duplicates")
    parser.add_argument("-f", "--sam_file", help="to specify the input sam file to read in", required=True)
    parser.add_argument("-u", "--umi_file", help="to specify the input umi file to read in", required=True)
    parser.add_argument("-o", "--sam_out", help="to specify the output sam file to write to", required=True)
    return parser.parse_args()

args=get_args() 
sam_file:str =args.sam_file
umi_file:str =args.umi_file
sam_output:str = args.sam_out



def store_umi(umi_file):
    '''this function takes in the known umi file and stores it into a set'''
    umi_set= set()
    with open(umi_file, 'r') as umi:
        for line in umi:
            umi_set.add(line.strip())
    return umi_set




def check_strandedness(flag):
    '''this function returns a bool based on if the sequence is reversed or not'''
    #flag:int =0
    if((flag & 16) == 16):
        #yes reverse complemented on the '-'strand
        return True
    else:
        # + PLUS strand
        return False

def adjust_position(position, cigar, strand):
    '''this function uses the cigar string to adjust the position based on strandedness'''
    new_p = 0

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
            if group =='M' or group =='D' or group =='S'or group =='N':
            #if group != 'I':
                
                new_p += count
        #print(f'new count {new_p}')
        adjusted_pos = position + new_p
        return adjusted_pos
    


#REAL MAIN-----------------------------------------------------------------------------------------
def main():
    '''main function to organize workflow'''
    umi_set = store_umi(umi_file)
    # print(umis)
    #creating dictionar to compare duplicates
    duplicate = 0
    record =0
    unknown_umis = 0
    dup_dict={}
    chrom_count={}
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
                    strand = check_strandedness(int(flag))
                    #getting the accurate position
                    position = adjust_position(int(line1_position), line1_cigar, strand)
                   
                    duplicate_tuple = (umi_exist, strand, position)
                    if duplicate_tuple in dup_dict:
                        duplicate +=1
                        dup_dict[duplicate_tuple]+=1
                        #continue
                    else:
                        sam_out.write(f'{sam_line1}\n')
                        #if chromosome not in dictionary add it to the dictionary
                        #dup_dict.add(duplicate_tuple)
                        dup_dict[duplicate_tuple]=1
                        record +=1
                        if not chrom_count.get(prev_chrom):
                            chrom_count[prev_chrom] =1
                        else:
                            chrom_count[prev_chrom]+=1
                else:
                    unknown_umis+=1
                    record+=1
                    #continue
                
    with open('summary.txt', 'w')as summary:   
        summary.write(f'duplicate: {duplicate}\n')
        summary.write(f'Number of reads: {record}\n')
        summary.write(f'Unknown UMIs: {unknown_umis}\n')
        
        for chrom, count in chrom_count.items():
            summary.write(f'{chrom} : {count}\n')
#------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()

