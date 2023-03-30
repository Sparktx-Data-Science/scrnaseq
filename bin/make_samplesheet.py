#!/usr/bin/env python

import argparse
import os

class Sample:

    bucket = "s3://sparkds-device-dropin-rd-1249-nseq/Output/230214_VH00163_33_AAATGMKHV/Analysis/1/Data/fastq/"

    @staticmethod
    def get_name(fastq):
        if '_R1' in fastq:
            name = os.path.basename(fastq).split('_R1')[0]
        elif '_R2' in fastq:
            name = os.path.basename(fastq).split('_R2')[0]
        else:
            raise ValueError('Cannot get sample name from %s' % fastq)
        if '_S' in name:
            name = name.split('_S')[0]
        return name

    def __init__(self, name):
        self.name = name
        self.read1 = None
        self.read2 = None

    def check(self):
        if self.read1 and self.read2:
            return True
        return False

    def assign(self, fastq):
        if self.get_name(fastq) != self.name:
            raise ValueError('Cannot assign fastq %s to sample %s' % (fastq, self.name))
        if '_R1' in fastq:
            self.read1 = fastq
        elif '_R2' in fastq:
            self.read2 = fastq
        
    def as_string(self, strandedness):
        return ','.join([self.name, Sample.bucket + self.read1, Sample.bucket + self.read2, strandedness]) + '\n'

parser = argparse.ArgumentParser()
parser.add_argument('--strandedness', default='auto')
parser.add_argument('--fastqs', nargs='+')
parser.add_argument('--output')
args = parser.parse_args()

if len(args.fastqs) % 2 != 0:
    raise IOError('An even number of fastqs must be provided')

sampledict = {}

for fastq in args.fastqs:
    name = Sample.get_name(fastq)
    if name not in sampledict:
        sampledict[name] = Sample(name)
    sampledict[name].assign(fastq)

for sample in sampledict.values():
    sample.check()

with open(args.output, 'w') as output:
    output.write(','.join(['sample','fastq_1','fastq_2',args.strandedness]) + '\n')
    for sample in sampledict.values():
        output.write(sample.as_string(args.strandedness))
