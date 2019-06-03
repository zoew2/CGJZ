#!/bin/sh

DATA_DIR=/dropbox/18-19/573/Data/Documents/evaltest
ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
RESULTS_FILE_PATH='../results'

# run lead
#time python3 run_summarization.py "$dir"/GuidedSumm11_test_topics.xml lead --output_dir ../outputs/D4_eval/
# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/lead_rouge_evalset.xml &> "$RESULTS_FILE_PATH"/lead_rouge_evalset_scores.out

# run mead
#time /opt/python-3.6/bin/python3 run_summarization.py "$DATA_DIR"/GuidedSumm11_test_topics.xml mead --output_dir ../outputs/D4_eval/
## evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_evalset.xml &> "$RESULTS_FILE_PATH"/mead_rouge_evalset_scores.out

# run melda
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm11_test_topics.xml melda --output_dir ../outputs/D4_evaltest/
# evaluate melda
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/melda_rouge_evalset.xml &> "$RESULTS_FILE_PATH"/D4_evaltest_rouge_scores.out
