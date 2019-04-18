#!/bin/sh

ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
CONFIG_FILE_WITH_PATH='/home2/zoew2/Ling573/results/rouge_run.xml'


"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d ${CONFIG_FILE_WITH_PATH} &> D2_rouge_scores.out
