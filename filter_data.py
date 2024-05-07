from mpi4py import MPI
import os
import re
import csv

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
root = 0  # Root process rank

FILE = 'twitter-100gb.json'

# Function to read the file and yield lines for each process
def read_json_file(rank, size, file):
    f_size = os.path.getsize(file)
    bytes_per_rank = f_size // size
    start = rank * bytes_per_rank
    bytes_read = 0

    f = open(file, 'rb')
    f.seek(start, 0)
    for line in f:
        if rank == 0 or bytes_read > 0:
            yield line.decode()
        bytes_read += len(line)
        if bytes_read >= bytes_per_rank:
            break
    f.close()

# Function to validate if the tag contains "Australia-based" or "Australia-located"
def validate_tag(line):
    tag_match = re.search(r'"tag":"(.*?)"', line)
    if tag_match:
        tag = tag_match.group(1)
        if "Australia-based" in tag or "Australia-located" in tag:
            return True
    return False

# Function to extract the desired fields from a tweet
def extract_fields(line):
    created_at_match = re.search(r'"created_at":"([^"]+)"', line)
    sentiment_match = re.search(r'"sentiment":([+-]?\d+(\.\d+)?)', line)
    text_match = re.search(r'"text":"([^"]+)"', line)

    created_at = created_at_match.group(1) if created_at_match else ""
    sentiment = float(sentiment_match.group(1)) if sentiment_match else 0.0
    text = text_match.group(1) if text_match else ""

    return created_at, sentiment, text

# Collect relevant tweets and their fields locally
local_results = [extract_fields(row) for row in read_json_file(rank, size, FILE) if validate_tag(row)]

# Gather all results at the root process
all_results = comm.gather(local_results, root=root)

# If this is the root process, combine all lists and write to a CSV file
if rank == root:
    combined_results = [item for sublist in all_results for item in sublist]
    csv_filename = 'tweets_100Gb_filtered.csv'
    headers = ['Created_At', 'Sentiment', 'Text']

    # Write combined results to a CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(combined_results)

    print(f"Exported {len(combined_results)} tweets to {csv_filename}.")