**Deliverable 3**<br>
May 19, 2019

**Group 2**<br>
Claude Zhang<br>
Julia McAnallen<br>
Genevieve Peaslee<br>
Zoe Winkworth<br>


Both baseline systems - Lead Sentence (hereafter LEAD) and MEAD - can be run by executing `run_all.sh` from inside CGJZ/src, either directly or by submitting `D3.cmd` to Condor. `run_all.sh` executes the main module, `run_summarization.py`, which takes two arguments: the .xml file with the topics + document ids to be summarized and an integer indicating which system to run (1 for LEAD and 2 for MEAD).

Likewise, the new system MELDA can be run in the same way. This is the submitted default system, with default parameters: 3 topics, 5 sentences per topic, MEAD score weights: 1, 1, 1; Brown Corpus (from NLTK) for IDF score; max threshhold value.
