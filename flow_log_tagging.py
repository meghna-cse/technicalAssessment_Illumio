import csv
import time
import os
import sys

# Start timing the execution
start_time = time.time()

# Define the paths to the input files
input_table_log_tags_file_path = 'input/log_tags.csv'
#input_table_log_tags_file_path = 'input/log_tags_large.csv'
#input_table_log_tags_file_path = 'input/log_tags_empty.csv'

input_table_protocol_mapping_file_path = 'input/protocol-numbers-1.csv'

input_logs_file_path = 'input/sample_logs.txt'
#input_logs_file_path = 'input/sample_10MB_logs.txt'
#input_logs_file_path = 'input/sample_logs_empty.txt'

output_count_tags_file_path = 'output/count_tags.csv'
output_count_port_protocol_file_path = 'output/count_port_protocol.csv'

# Check whether files are empty
if os.path.getsize(input_table_log_tags_file_path) == 0:
    print(f"Error: The log mapping table '{input_table_log_tags_file_path}' is empty.")
    sys.exit()

if os.path.getsize(input_logs_file_path) == 0:
    print(f"Error: The log file '{input_logs_file_path}' is empty.")
    sys.exit()

''' 
Import the log tags table from the csv file and protocol mapping and store them in a dictionary
'''
table_log_tags = {}
with open(input_table_log_tags_file_path, mode = 'r') as tags:
    reader = csv.reader(tags)
    next(reader)
    for row in reader:
        dstport, protocol, tag = row
        table_log_tags[(dstport, protocol)] = tag

protocol_mapping = {}
with open(input_table_protocol_mapping_file_path, mode='r') as protocols:
    reader = csv.reader(protocols)
    next(reader)
    for row in reader:
        protocol_number = row[0].strip()
        protocol_name = row[1].strip().lower()
        protocol_mapping[protocol_number] = protocol_name


'''
Import the flow logs from the csv file, and count the tag and the port/protocol combination in the logs.
As per the https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields document,
dstport and protocol will be the 6th and 7th fields respectively (0-based indexing).
'''
tag_counts = {}
port_protocol_counts = {}

with open(input_logs_file_path, mode='r') as logs:
    for line in logs:
        parts = line.split()
        dstport = parts[6]
        protocol_number = parts[7].lower()
        protocol = protocol_mapping.get(protocol_number, None)

        if protocol:
            tagkey = (dstport, protocol)

            # Tag count: for EACH existing combination of dstport and protocol in the lookup table, count the number of logs
            if tagkey in table_log_tags:
                tag = table_log_tags[tagkey]
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # Port/Protocol count: for ALL combinations of dstport and protocol in the logs, count the number of logs
            port_protocol_counts[tagkey] = port_protocol_counts.get(tagkey, 0) + 1
        else:
            tagkey = (dstport, protocol_number)

            # Port/Protocol count: for ALL combinations of dstport and protocol in the logs, count the number of logs
            port_protocol_counts[tagkey] = port_protocol_counts.get(tagkey, 0) + 1


'''
Output the counts and errors to files
'''
with open(output_count_tags_file_path, mode = 'w') as tagsCount:
    writer = csv.writer(tagsCount)
    writer.writerow(['Tag','Count'])
    for tag, count in tag_counts.items():
        writer.writerow([tag, count])

with open(output_count_port_protocol_file_path, mode = 'w') as portProtocolCount:
    writer = csv.writer(portProtocolCount)
    writer.writerow(['Port','Protocol','Count'])
    for (port, protocol), count in port_protocol_counts.items():
        writer.writerow([port, protocol, count])

# Calculate and print the total execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds for log file: " + input_logs_file_path + " and tag file: " + input_table_log_tags_file_path)