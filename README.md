# Log Data Tagging

## Overview

This project contains a Python script that processes flow log data and maps each row to a tag based on a lookup table. The script generates output files containing:
- The count of matches for each tag.
- The count of matches for each port/protocol combination.


## Execution Instructions

1. **Prerequisites**:
   - Python 3.x
   - No additional libraries required.

2. **Running the Script**:
   - **Uncomment the appropriate input files** in the script based on the test you want to run. The script includes several predefined input file paths:
     ```python
     input_table_log_tags_file_path = 'input/log_tags.csv'
     #input_table_log_tags_file_path = 'input/log_tags_large.csv'
     #input_table_log_tags_file_path = 'input/log_tags_empty.csv'

     input_logs_file_path = 'input/sample_logs.txt'
     #input_logs_file_path = 'input/sample_10MB_logs.txt'
     #input_logs_file_path = 'input/sample_logs_empty.txt'
     ```
        Uncomment the desired lines by removing the `#` at the beginning of the line, and comment out the others.
   - Run the script using the following command:
     ```bash
     python flow_log_tagging.py
     ```
   - The output files will be generated in the `output/` directory.

### More on Input and Output Files

1. **Input Files**:
   - Log mapping table as plain text ASCII files.
        - `input/log_tags.csv` : A small lookup table mapping destination ports and protocols to tags. 
        - `input/log_tags_large.csv` : lookup table containing 10,000 mappings.
        - `input/log_tags_empty.csv` : empty lookup table for testing.
   - Protocol mapping table as plain text ASCII files.
        - `input/protocol-numbers-1.csv`: A CSV file mapping protocol numbers to protocol names. Obtained from [here](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml).
   - Log file: The flow log file can be up to 10 MB in size. Sample log files:
        - `input/sample_logs.txt` : a small log file for testing.
        - `input/sample_logs_empty.txt` : an empty log file for testing
        - `input/sample_10MB_logs.txt` : a 10 MB large log file for testing

2. **Output Files**:
   - The script outputs the count of matches for each tag and port/protocol combination.
        - `output/count_tags.csv` : Output file containing the count of matches for each tag.
        - `output/count_port_protocol.csv` : Output file containing the count of matches for each port/protocol combination.




## Performance

### Test Results

1. **Small Log File with Large Tag File**:
   - **Log File**: `input/sample_logs.txt`
   - **Tag File**: `input/log_tags_large.csv`
   - **Execution Time**: 0.06 seconds

2. **Small Log File with Small Tag File**:
   - **Log File**: `input/sample_logs.txt`
   - **Tag File**: `input/log_tags.csv`
   - **Execution Time**: 0.02 seconds

3. **Large Log File with Small Tag File**:
   - **Log File**: `input/sample_10MB_logs.txt`
   - **Tag File**: `input/log_tags.csv`
   - **Execution Time**: 108.48 seconds

4. **Large Log File with Large Tag File**:
   - **Log File**: `input/sample_10MB_logs.txt`
   - **Tag File**: `input/log_tags_large.csv`
   - **Execution Time**: 117.23 seconds

## Assumptions

- The script only supports the default log format (version 2) as per the AWS documentation.
- The script expects well-formatted input files with correct headers.
- The script handles empty input files by terminating the execution with an appropriate message.

## Limitations

- The script may not handle custom log formats or additional versions beyond version 2.
- Performance may vary based on system resources and file sizes beyond 10MB.

## Error Handling

- If any of the input files are empty, the script will terminate with an error message.

