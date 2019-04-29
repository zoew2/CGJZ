**Deliverable 2**<br>
April 28, 2019

**Group 2**<br>
Claude Zhang<br>
Julia McAnallen<br>
Genevieve Peaslee<br>
Zoe Winkworth<br>


Both baseline systems - Lead Sentence (hereafter LEAD) and MEAD - are run from `run_all.sh` through the Condor file `D2.cmd`.


The variable parameters discussed in our write-up can be found in the following locations:
- The baseline system that is run is determined in `run_summarization`: 1 - LEAD, 2 - MEAD
- The background corpus for the IDF values is either Brown or Reuters (both from NLTK); this parameter is changed in `mead_summary_generator`, lines 43 and 44
- The centroid threshold value that words must exceed to appear in the Count*IDF is designated in the `mead_content_selector`'s function `__calculate_threshold` on line 57 and the subsequent helper functions to calculate a centroid threshold (i.e. `min_mean_threshold`, `max_mean_threshold` and `mean_threshold`)
- The weights for the different components of the Mead scores are entered in the `mead_content_selector`'s `get_score` function as input parameters: centroid score (`w_c`), position score (`w_p`) and overlap with first sentence score (`w_f`)

