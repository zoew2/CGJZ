#!/bin/sh

DATA_DIR=/dropbox/18-19/573/Data/Documents/devtest
ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
RESULTS_FILE_PATH='../results'

# run lead
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml lead
# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/lead_rouge_run.xml &> "$RESULTS_FILE_PATH"/lead_rouge_scores.out

# run mead
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead
# evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-B-max-111.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-B-max-111.out

#run melda
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml melda
# evaluate melda
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/melda_rouge_run-B-max-111-35-mead.xml &> "$RESULTS_FILE_PATH"/D4_rouge_scores.out

