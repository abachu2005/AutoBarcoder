RNA Barcode Processor

This project is a Python-based tool that processes RNA barcodes in sequencing data using Tkinter for the GUI and additional libraries for data processing. It clusters similar barcodes and outputs both raw text summaries and graphical visualizations of the barcode distributions.

Features

Allows input of sequencing data files (either .txt or .fastq format).
Processes barcodes based on user-defined row and column sequences.
Replaces long barcode sequences with shorter ones, if appropriate.
Clusters similar barcodes based on a user-defined edit distance tolerance.
Outputs a summary of the most common barcodes.
Generates a PDF with bar graphs showing barcode distributions per well.
Provides a friendly GUI interface using Tkinter.
Project Structure

__init__.py: Package initializer file.
app.py: Contains the GUI logic using Tkinter, handling user interaction and file input.
barcode_processing.py: Contains the core logic for reading, processing, and analyzing barcodes.
requirements.txt: Lists the dependencies required for the project.
README.md: Project documentation file (this file).
Setup Instructions

Clone the repository
To download the project files, use the following command in your terminal:

bash
Copy code
git clone https://github.com/yourusername/barcode_processor.git
Then navigate into the project directory:

bash
Copy code
cd barcode_processor
Create a virtual environment (optional but recommended)
It is a good practice to create a virtual environment for your project to manage dependencies in isolation. To create one:

Copy code
python -m venv venv
Activate the virtual environment:

On macOS/Linux:
bash
Copy code
source venv/bin/activate
On Windows:
Copy code
venv\Scripts\activate
Install dependencies
Install the required dependencies by running the following command:

Copy code
pip install -r requirements.txt
The dependencies listed in requirements.txt are:

tk: For creating the graphical user interface.
python-levenshtein: For calculating edit distances between barcodes.
networkx: For handling clustering of barcodes.
matplotlib: For generating graphs and visualizations.
Running the application
After installing the dependencies, you can run the application by executing:

Copy code
python app.py
This will launch the Tkinter-based graphical user interface.
Usage Instructions

Input File: In the GUI, use the "Browse" button to select the sequencing data file you want to process (in .txt or .fastq format).
Row Barcodes: Enter the row barcodes (one per line) in the designated text area.
Column Barcodes: Enter the column barcodes (one per line) in the designated text area.
Flanking Sequences: Specify the start and end flanking sequences that surround the RNA barcode in your data file.
Expected RNA Barcode Length: Enter the expected barcode length to ensure proper filtering and replacement of long sequences.
Edit Tolerance: Define the edit distance threshold for clustering similar barcodes.
Output Files: Use the "Browse" buttons to specify the file paths where the results (text and graphical data) will be saved.
Process Barcodes: Click the "Process Barcodes" button to start the processing. The results will be saved in the output files specified, and the program will show a confirmation message upon completion.
Troubleshooting

Ensure all required fields are filled out before clicking the "Process Barcodes" button.
If there are any errors during processing, they will be displayed in an error message box. Double-check the file paths and barcode parameters.
License

This project is open-source and licensed under the MIT License.
