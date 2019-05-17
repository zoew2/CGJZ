#!/bin/sh

ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
RESULTS_FILE_PATH='../results'

/opt/python-3.6/bin/python3 test_preprocessor.py

# run mead on test xml files
#time /opt/python-3.6/bin/python3 run_summarization.py ././tests/test_data/test_topics.xml mead
# evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run.xml &> "$RESULTS_FILE_PATH"/test_mead_rouge_scores.out
