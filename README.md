PROMETHEUS is the replacement for RIPLEY, currently development stage. It will contain far more flexible support scripts, allowing user additions of functions to the pipeline. It will eventually replace RIPLEY.

Note 1: ALIGN directory has some tricky syntax. For the purpose of potentially using a different aligner besides STAR someday, you have the option to align paired end data by strand, or by combining forward and reverse strand. RIPLEY handles this by adding a system defined variable called <REVERSE STRAND>, which will check if the data is indeed paired end, and then add both strands into a single alignment.
