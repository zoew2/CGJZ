#!/bin/sh

ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
CURR_DIR=$(/usr/bin/pwd)
CONFIG_FILE_PATH="$CURR_DIR"

# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/lead_rouge_run.xml &> lead_rouge_scores.out

# evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/mead_rouge_run.xml &> mead_rouge_scores.out

# test_rouge_mead-no_first
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/melda_rouge_run-B-max-111.xml &> melda_rouge_scores-B-max-111.out
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/mead_rouge_run-B-max-111.xml &> mead_rouge_scores-B-max-111.out
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/mead_rouge_run-R-max-111.xml &> mead_rouge_scores-R-max-111.out
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$CONFIG_FILE_PATH"/mead_rouge_run-B-zero-111.xml &> mead_rouge_scores-R-zero-111.out
