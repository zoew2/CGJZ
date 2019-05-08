#!/bin/sh

DATA_DIR=/dropbox/18-19/573/Data/Documents/devtest
ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
CURR_DIR=$(/usr/bin/pwd)
CONFIG_FILE_PATH="$CURR_DIR"

# run lead
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml 1
# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/lead_rouge_run.xml &> lead_rouge_scores.out

# run mead
time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml 2
# evaluate mead
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/mead_rouge_run.xml &> mead_rouge_scores.out
