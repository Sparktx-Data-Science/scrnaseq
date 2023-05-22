#!/usr/bin/env python3

import argparse
import glob
import subprocess
import sys

def make_count_html(samplenames, outdir):
    outstring = ''
    for name in samplenames:
        report_loc = '/mnt/groupdata/' + outdir[5:] + "cellranger/count/sample-" + name + "/outs/web_summary.html"
        outstring += "## %s\n\n```{r %s, echo=FALSE}\nhtmltools::includeHTML(\"%s\")\n```\n\n" % (name, name, report_loc)
        break
    return outstring

def replace_in_file(infile, outfile, replace_dict):
    """ In infile, replace instances of one or more strings and write
            the resulting modified file to outfile
        replace_dict matches strings to be replaced with their replacements
    """
    with open(infile, 'r') as inlines:
        with open(outfile, 'w') as outlines:
            for line in inlines:
                newline = line
                for instring, outstring in replace_dict.items():
                    newline = newline.replace(instring, outstring)
                outlines.write(newline)

def get_deployment_url(stdout):
    """ Extract content URL from deployment script standard output
        Returns None if URL cannot be found
    """
    for line in stdout.split('\n'):
        if line.startswith('Document successfully deployed'):
            url = line.rstrip().split(' ')[-1]
            return url
    return None

def addquotes(string):
    """ Put double quotes around a string """
    return '"' + string + '"'

parser = argparse.ArgumentParser()
parser.add_argument('--report-script')
parser.add_argument('--runid')
parser.add_argument('--publicid')
parser.add_argument('--urls', nargs='*')
parser.add_argument('--debug', default=False, action='store_true')
args = parser.parse_args()

deployproc = subprocess.run(['Rscript', args.report_script,
        '--appname', args.runid.replace('.', '_').replace('-', '_') + '_multiqc', '--document', 'multiqc_report.html'], capture_output=True)

if args.debug:
    print(deployproc.stdout.decode())
    print(deployproc.stderr.decode())
multiqc_url = get_deployment_url(deployproc.stdout.decode())
if not multiqc_url:
    raise RuntimeError('Deployment failed for %s' % args.runid)

with open('tmp.Rmd', 'w') as tmp:
    tmp.write('---\ntitle: %s\n---\n\n' % args.publicid)
    for index, url in enumerate(args.urls):
        tmp.write('* [Sample %s](%s)\n' % (index, url))
    tmp.write('* [MultiQC report](%s)\n' % multiqc_url)

deployproc = subprocess.run(['Rscript', args.report_script,
        '--appname', 'scrnaseq_' + args.runid.replace('.', '_').replace('-', '_'), '--document', 'tmp.Rmd'], capture_output=True)
url = get_deployment_url(deployproc.stdout.decode())
if not url:
    raise RuntimeError('Deployment failed for %s' % args.runid)
else:
    print("Report deployed to %s" % url)
