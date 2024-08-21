import os
import csv
import time
import streamlit as st
import pandas as pd

def get_recently_modified_files(directory, time_interval):
    modified_files = []
    current_time = time.time()

    # Strip extra quotes or spaces from the directory path and ensure it's a valid path
    directory = directory.strip().strip('"').strip("'")

    if not os.path.exists(directory):
        st.error(f"Directory '{directory}' does not exist.")
        return []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            modification_time = os.path.getmtime(filepath)
            if current_time - modification_time <= time_interval:
                modified_files.append((filename, time.ctime(modification_time)))

    return modified_files

def write_to_csv(modified_files, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'Modification Time'])
        csvwriter.writerows(modified_files)

def main():
    st.title("File Monitor Dashboard")

    folder_name = st.text_input("Enter folder path:", "")
    time_interval = st.number_input("Enter time interval (in seconds):", min_value=0, value=3600)

    if st.button("Check Modified Files"):
        if folder_name:
            modified_files = get_recently_modified_files(folder_name, time_interval)
            if modified_files:
                output_file = 'modified_files.csv'
                write_to_csv(modified_files, output_file)
                st.success(f"Modified files list has been written to {output_file}")

                st.write("### Recently Modified Files")
                df = pd.read_csv(output_file)
                with st.expander("Click to view the modified files table"):
                    st.dataframe(df)
            else:
                st.info("No files modified within the specified time interval.")
        else:
            st.error("Please enter a valid folder path.")

if __name__ == "__main__":
    main()
