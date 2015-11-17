# -*- coding: utf-8 -*-
import sys
import os
import argparse

def main():
    '''Parte principal do programa onde as outras funcoes sao chamadas'''
    obj = argparse.ArgumentParser(description="Convert bam files in BigWig files. Can be used in multiples files"
                                              "separeted by space")
    obj.add_argument("-bam", nargs='+', help="Bam file path (Create a index before run)", required=True)
    obj.add_argument("-chrS", help="chrSize file sorted by number", required=True)
    arg = obj.parse_args()

    for bam_in in arg.bam:
        print 'Converting: {}'.format(bam_in)
        convert_bam_files(bam_in, arg.chrS)



def generate_index(bam_file):
    print 'Genrating index bam..'
    generate_bai_cmd = 'bamtools index  -in {}'.format(bam_file)
    print generate_bai_cmd
    os.system(generate_bai_cmd)


def convert_bam_files(bam_file, genome_size_file):
        genome_size_file = os.path.abspath(genome_size_file)
        possible_bai = bam_file.rsplit(".", 1)[0] + ".bai"
        out_cov = bam_file.rsplit(".", 1)[0] + ".cov"
        out_bw = bam_file.rsplit(".", 1)[0] + ".bw"

        if not os.path.exists(possible_bai):
            generate_index(bam_file)

        genome_coverage_cmd = "genomeCoverageBed -ibam {} -bg -split -g {} > {}".format(bam_file,

	                                                                                               genome_size_file,
                                                                                                   out_cov)
        print "Adding the chr prefix"
	fix_chr_file_cov = out_cov + "fix"
	cmd_perl = "perl -pe 's/^/chr/g' {}> {}".format(out_cov, fix_chr_file_cov)
	
	

	print genome_coverage_cmd
        os.system(genome_coverage_cmd)
        #print genome_coverage_cmd

	print cmd_perl
	os.system(cmd_perl)


        bed_graph_to_bw_cmd =  "bedGraphToBigWig  {} {}  {}".format(fix_chr_file_cov, genome_size_file + ".fix", out_bw)
        print bed_graph_to_bw_cmd
        os.system(bed_graph_to_bw_cmd)
        #print bed_graph_to_bw_cmd
	os.system("rm {};rm {}".format(out_cov, fix_chr_file_cov))

if __name__ == '__main__':
    sys.exit(main())
