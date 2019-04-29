**Deliverable 2**<br>
April 28, 2019

**Group 2**<br>
Claude Zhang<br>
Julia McAnallen<br>
Genevieve Peaslee<br>
Zoe Winkworth<br>


Both baseline systems - Lead Sentence (hereafter LEAD) and MEAD - are run from `run_all.sh` through the Condor file `D2.cmd`. `run_all.sh` executes the main module, `run_summarization.py`, which takes two arguments: the .xml file with the topics + document ids to be summarized and an integer indicating which system to run (1 for LEAD and 2 for MEAD).


The variable parameters discussed in our write-up can be found in the following locations:
- The background corpus for the IDF values is either Brown or Reuters (both from NLTK); this parameter is changed in `mead_summary_generator`, lines 43 and 44. The default is Brown.
- The threshold that a word's Count*IDF value must exceed to appear in the centroid vector is designated in the `mead_content_selector`'s function `__calculate_threshold` on line 57 which indicates a helper function on the following lines to calculate a centroid threshold (i.e. `min_mean_threshold`, `max_mean_threshold` and `mean_threshold`).
- The weights for the different components of the Mead scores are entered in the `mead_content_selector`'s `get_score` function as input parameters: centroid score (`w_c`), position score (`w_p`) and overlap with first sentence score (`w_f`)

