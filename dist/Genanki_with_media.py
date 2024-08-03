import csv
import random
import genanki
import html
import os
import sys

# Function to generate a unique model ID


def generate_model_id():
    """
    Generates a unique model ID for Anki models.

    Returns:
        int: A unique model ID.
    """
    return random.randrange(1 << 30, 1 << 31)

# Define a function to create a custom note with a stable GUID


class CustomNote(genanki.Note):
    @property
    def guid(self):
        """
        Property method to generate a unique GUID for the note.

        The GUID is generated based on the first two fields of the note.

        Returns:
            int: A unique GUID for the note.
        """
        return genanki.guid_for(self.fields[0], self.fields[1])

# Function to read CSV and create decks


def create_decks_from_csv(csv_filename):
    """
    Creates decks from a CSV file and generates Anki cards for each row.

    Args:
        csv_filename (str): The name of the CSV file to read.

    Returns:
        dict: A dictionary of decks, where the keys are deck names and the values are `genanki.Deck` objects.

    This function reads a CSV file containing rows of data with columns for 'Deck', 'Command', 'Description', and 'Media'. 
    It creates a new deck for each unique 'Deck' value in the CSV file and adds an Anki card to the deck for each row. 
    The Anki card is created using a custom note with the 'Command', 'Description', and 'Media' fields. 
    The function returns a dictionary of decks, where the keys are deck names and the values are `genanki.Deck` objects.
    """
    decks = {}
    model_id = generate_model_id()
    model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Command'},
            {'name': 'Description'},
            {'name': 'Media'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Command}}<br>{{Media}}',
                'afmt': '{{Description}}',
            },
        ],
        css=".card { font-family: arial; font-size: 20px; color: black; background-color: white; }"
    )

    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            deck_name = row['Deck']
            if deck_name not in decks:
                deck_id = genanki.Deck.get_next_deck_id()
                decks[deck_name] = genanki.Deck(deck_id, deck_name)

            fields = [
                html.escape(row['Command']),
                html.escape(row['Description']),
                f'<img src="{os.path.basename(row["Media"])}">' if row["Media"] else ''
            ]
            note = CustomNote(
                model=model,
                fields=fields,
                sort_field=fields[0]
            )
            decks[deck_name].add_note(note)

    return decks

# Function to save decks to Anki package files


def save_decks(decks):
    """
    Saves the decks to Anki package files.

    Args:
        decks (dict): A dictionary where keys are deck names and values are `genanki.Deck` objects.

    Returns:
        None

    This function iterates over each deck in the `decks` dictionary and saves it to an Anki package file. 
    It first retrieves the media files associated with each note in the deck. It then creates a `genanki.Package` 
    object and sets its `media_files` attribute to the list of media files. Finally, it generates a filename 
    based on the deck name and writes the package to the file.
    """
    for deck_name, deck in decks.items():
        media_files = [note.fields[2] for note in deck.notes if note.fields[2]]
        media_files = [media for media in media_files if media]
        package = genanki.Package(deck)
        package.media_files = media_files
        filename = f"{deck_name.replace(' ', '_').lower()}.apkg"
        package.write_to_file(filename)

# Main function


def main():
    """
    The main function that executes the program.

    This function reads a CSV file specified by the first command-line argument, creates decks from the data in the file, 
    and saves the decks to Anki package files.

    Parameters:
        None

    Returns:
        None

    CSV file format:
        Deck,Command,Description,Media
        DECK_NAME,COMMAND,DESCRIPTION,MEDIA_FILE
        DECK_NAME2,COMMAND2,DESCRIPTION2,MEDIA_FILE2
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    decks = create_decks_from_csv(csv_filename)
    save_decks(decks)


if __name__ == "__main__":
    main()
