#!/bin/sh

DATA_DIR=/dropbox/18-19/573/Data/Documents/devtest
ROUGE_DIR='/dropbox/18-19/573/code/ROUGE'
RESULTS_FILE_PATH='../results'

# run lead
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml lead
# evaluate lead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/lead_rouge_run.xml &> "$RESULTS_FILE_PATH"/lead_rouge_scores.out

# run mead
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --c_threshold mean >> d3.out
## evaluate mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-B-mean-111.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-B-mean-111.out

#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --corpus R >> d3.out
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-R-max-111.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-R-max-111.out

#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --c_threshold zero >> d3.out
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-B-zero-111.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-R-zero-111.out

#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --c_threshold min
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --c_threshold mean
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --c_threshold zero
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_p 0 --w_f 0
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_c 0 --w_f 0
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_c 0 --w_p 0
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_c 0
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_p 0
#time python3 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_f 0

#run melda
time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml melda --lda_topics 4 --n 1
"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/melda_rouge_run-41.xml &> "$RESULTS_FILE_PATH"/melda_rouge_scores-41.out
#
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead --w_p 0 --w_f 0 >> d3.out
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-B-max-100.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-B-max-100.out

#run melda
#time /opt/python-3.6/bin/python3.6 run_summarization.py "$DATA_DIR"/GuidedSumm10_test_topics.xml mead
#"$ROUGE_DIR"/ROUGE-1.5.5.pl -e "$ROUGE_DIR"/data -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d "$RESULTS_FILE_PATH"/mead_rouge_run-B-max-111.xml &> "$RESULTS_FILE_PATH"/mead_rouge_scores-B-max-111.out

