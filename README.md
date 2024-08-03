## AutoAnkiCards

AutoAnkiCards is a Python script that automates the creation of Anki flashcards from a CSV file. This tool helps you streamline your study workflow and focus more on learning by converting your notes or study materials directly into Anki flashcards.

### Features

- Automatically generate Anki flashcards from a CSV file.
- Create multiple decks based on CSV data.
- Simple and easy to use.

### Installation

#### Option 1: Using the Executable

1. **Download the Executable:**

   Navigate to the `dist` directory and locate the `Genanki.exe` file.

2. **Prepare Your CSV File:**

   Create a CSV file with the following format:

   ```
   Deck,Card_Question,Card_Answer
   DECK_NAME,Card_Question,Card_Answer
   DECK_NAME2,Card_Question2,Card_Answer2
   ```

   You can use the provided `Sample_CSV.csv` as a reference.

3. **Run the Executable:**

   Open a terminal or command prompt, navigate to the directory containing `Genanki.exe`, and run:

   ```
   Genanki.exe Sample_CSV.csv
   ```

   Optionally, you can specify an output directory for the Anki package files:

   ```
   Genanki.exe Sample_CSV.csv output_directory
   ```

#### Option 2: Running the Python Script Manually

1. **Clone the Repository:**

   Open a terminal or command prompt and run the following commands:

   ```
   git clone https://github.com/yourusername/AutoAnkiCards.git
   cd AutoAnkiCards
   ```

2. **Ensure Python is Installed:**

   Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

3. **Install Required Dependencies:**

   If you don’t have the `genanki` library installed, you can install it using the following command:

   ```
   pip install -r requirements.txt
   ```

4. **Prepare Your CSV File:**

   Create a CSV file with the following format:

   ```
   Deck,Card_Question,Card_Answer
   DECK_NAME,Card_Question,Card_Answer
   DECK_NAME2,Card_Question2,Card_Answer2
   ```

   You can use the provided `Sample_CSV.csv` as a reference.

   You can generate the CSV file using AI through these steps
   [AI CSV Generator](./Using%20AI%20to%20make%20your%20own%20csv%20file.md)

5. **Run the Script:**

   Execute the script to generate your Anki flashcards:

   ```
   python Genanki.py Sample_CSV.csv
   ```

   Optionally, you can specify an output directory for the Anki package files:

   ```
   python Genanki.py Sample_CSV.csv output_directory
   ```

### Importing the Generated Deck into Anki

To import the generated `.apkg` files into Anki:

1. Open Anki.
2. Go to `File` > `Import`.
3. Select the `.apkg` file you generated.
4. Click `Open` and follow the prompts.

### Example

Check out the provided `Sample_CSV.csv` file to see an example of the expected format.

### License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.
