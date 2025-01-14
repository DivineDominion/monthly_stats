import os, pathlib
import prettytable as pt
from datetime import datetime
from plistlib import load
from urllib.parse import urlparse

####
# Function for finding the path to The Archive
#####
def TheArchivePath():
    """
    Find the path to The Archive's plist file.

    Returns:
        A string representing the path to The Archive.
    """
    bundle_id = "de.zettelkasten.TheArchive"
    team_id = "FRMDA3XRGC"
    #`fileName` is the path to the plist file that contains the path to the ZK.
    fileName = os.path.expanduser(
        "~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
    with open(fileName, 'rb') as fp:
        # load is a special function for use with a plist
        pl = load(fp) 
        # 'archiveURL' is the key that pairs with the zk path
        path = urlparse(pl['archiveURL']) 
    # path is the part of the path that is formatted for use as a path.
    return (path.path) 

####
# Function for finding monthly stats
#####        

def count_files_zettelkasten(partial_UID):
    """
    Counts the number of files in the directory specified by `TheArchivePath()` that contain the given `partial_UID` in their filename.

    Args:
        UID (str): The unique identifier to search for in the filenames.

    Returns:
        int: The number of files that contain the given `partial_UID` in their filename.
    """
    directory = TheArchivePath() # gets the path to the directory
    count = 0 # initializes the counter 
    for filename in os.listdir(directory): # iterates over the files in the directory
        if partial_UID in filename: # checks if the partial_UID is in the filename
            file_path = os.path.join(directory, filename) # constructs the full file path
            if os.path.isfile(file_path): # checks if the file is a regular file
                count += 1 # increments the counter variable
    return count # returns the count of files

# Generate year and month strings for the past 5 years
today = datetime.today()
partial_UIDs = []
for y in range(today.year-5, today.year+1): # 5 years ago to this year
    for m in range(1, 13):
        partial_UIDs.append(f" {y}{m:02d}")

# Create a list of lists to store the counts for each year
counts_by_year = []
for i in range(6):
    year_counts = [count_files_zettelkasten(partial_UIDs[j]) for j in range(i*12, (i+1)*12)]
    counts_by_year.append(year_counts)

# Convert month numbers to month names
month_names = [datetime(2000, i, 1).strftime('%b') for i in range(1, 13)]

# Create a table with the month names as the first column
table = pt.PrettyTable()
table.field_names = ['Stats'] + [str(y) for y in range(today.year-5, today.year+1)]
for i in range(12):
    table.add_row([month_names[i]] + [str(counts_by_year[j][i]) for j in range(6)])

# Print the table
print(table)  