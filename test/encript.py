from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

# Initialize the analyzer and anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

config = {"PERSON": OperatorConfig("replace", {"new_value": "[PII-Person]"}),
          "URL": OperatorConfig("replace", {"new_value": "[PII-URlL]"})
          }

def mask_text(text_care_note):
  # Analyze the text for PII
  analysis_results = analyzer.analyze(text_care_note,language='en')
  filtered_analysis_results = [result for result in analysis_results if (result.entity_type=="PERSON" or result.entity_type=="ADDRESS")]

  # Anonymize the detected PII using the configuration
  masked_care_note = anonymizer.anonymize(text_care_note, filtered_analysis_results,operators=config)

  return masked_care_note.text


def process_care_notes(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        care_notes_text = file.read()

    # Mask PII in the care notes
    masked_text = mask_text(care_notes_text)

    # Print the masked text
    print(masked_text)

# Specify the path to the CareNotes.txt file
file_path = "/home/gobbishangar/Downloads/Elder/CareNotes.txt"

# Process and print the result
process_care_notes(file_path)

# text = "Gobi chose to have a bowl of cornflakes with powder milk,cream,sugar and cooked breakfast such as two sausage, tomato, mushroom, boiled egg and a pot of yogurt.Maureen was playing with the breakfast meal, but she had only yogurt.Had drunk 560ml of milk. had meal served in the lounge,  Had some porridge and some yoghurt ."

# print(mask_text(text))


# import sqlite3
# from cryptography.fernet import Fernet

# # Generate a key for encryption and decryption
# # You should securely store this key in a secure location
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)

# # Create a SQLite database connection
# conn = sqlite3.connect('secure_database.db')
# cursor = conn.cursor()

# # Create a table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL
# )
# ''')

# # Function to encrypt data
# def encrypt_data(data):
#     return cipher_suite.encrypt(data.encode()).decode()

# # Function to decrypt data
# def decrypt_data(encrypted_data):
#     return cipher_suite.decrypt(encrypted_data.encode()).decode()

# # Insert encrypted data into the database
# name = "John Doe"
# email = "john.doe@example.com"

# encrypted_name = encrypt_data(name)
# encrypted_email = encrypt_data(email)

# cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (encrypted_name, encrypted_email))
# conn.commit()

# # Retrieve and decrypt data from the database
# cursor.execute('SELECT name, email FROM users')
# rows = cursor.fetchall()

# for row in rows:
#     decrypted_name = decrypt_data(row[0])
#     decrypted_email = decrypt_data(row[1])
#     print(f'Name: {decrypted_name}, Email: {decrypted_email}')

# # Close the database connection
# conn.close()


