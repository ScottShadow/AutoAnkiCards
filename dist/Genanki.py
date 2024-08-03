"""
Anki Auto Card Generator
"""
import csv
import random
import html
import sys
import os
import uuid
import genanki
from genanki import Model, Note, Deck, Package

# Function to generate a unique ID


def generate_id():
    """
    Generates a unique ID for Anki models or decks.

    Returns:
        int: A unique ID.
    """
    return random.randrange(1 << 30, 1 << 31)

# Define a function to create a custom note with a stable GUID


class CustomNote(genanki.Note):
    """
    CustomNote is a custom note class that extends the genanki.Note class.
    It adds a unique GUID for the note based on the first two fields of the note.
    """
    @property
    def guid(self):
        """
        Property method to generate a unique GUID for the note.

        The GUID is generated based on the first two fields of the note.

        Returns:
            str: A unique GUID for the note.
        """
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{self.fields[0]}|{self.fields[1]}"))

# Function to read CSV and create decks


def create_decks_from_csv(csv_filename):
    """
    Create decks from a CSV file and generate Anki cards for each row.

    Args:
        csv_filename (str): The name of the CSV file to read.

    Returns:
        dict: A dictionary of decks, where the keys are deck names and the
        values are `genanki.Deck` objects.

    This function reads a CSV file containing rows of data with columns for
    'Deck', 'Card_Question', and 'Card_Answer'.
    It creates a new deck for each unique 'Deck' value in the CSV file and
    adds an Anki card to the deck for each row.
    The Anki card is created using a custom note with the 'Card_Question' and
    'Card_Answer' fields. 
    The function returns a dictionary of decks, where the keys are deck names
    and the values are `genanki.Deck` objects.
    """
    decks = {}
    model_id = generate_id()
    model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Card_Question'},
            {'name': 'Card_Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Card_Question}}',
                'afmt': '{{Card_Answer}}',
            },
        ],
        css=".card { font-family: arial; font-size: 20px; color: black; background-color: white; }"
    )

    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            deck_name = row['Deck']
            if deck_name not in decks:
                deck_id = generate_id()
                decks[deck_name] = genanki.Deck(deck_id, deck_name)

            fields = [html.escape(row['Card_Question']),
                      html.escape(row['Card_Answer'])]
            note = CustomNote(
                model=model,
                fields=fields,
                sort_field=fields[0]
            )
            decks[deck_name].add_note(note)

    return decks

# Function to save decks to Anki package files


def save_decks(decks, output_dir=None):
    """
    Saves the decks to Anki package files.

    Args:
        decks (dict): A dictionary where keys are deck names and values are
        `genanki.Deck` objects.
        output_dir (str, optional): The directory to save the package files. Defaults to None.

    Returns:
        None
    """
    for deck_name, deck in decks.items():
        filename = f"{deck_name.replace(' ', '_').lower()}.apkg"
        if output_dir:
            filename = os.path.join(output_dir, filename)
        genanki.Package(deck).write_to_file(filename)

# Main function


def main():
    """
    This function reads a CSV file specified by the first Card_Question-line
    argument, creates decks from the data in the file, 
    and saves the decks to Anki package files.

    Parameters:
        None

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        ValueError: If the CSV file does not have the required columns
        ('Deck', 'Card_Question', and 'Card_Answer').

    CSV file format:
        Deck,Card_Question,Card_Answer
        DECK_NAME,Card_Question,Card_Answer
        DECK_NAME2,Card_Question2,Card_Answer2
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_filename> [output_dir]")
        sys.exit(1)

    csv_filename = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    decks = create_decks_from_csv(csv_filename)
    save_decks(decks, output_dir)


if __name__ == "__main__":
    main()
