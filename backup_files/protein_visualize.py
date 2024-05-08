import py3Dmol
import streamlit as st
import requests
import sys

class PDB_Parser:
    def __init__(self, protein_id):
        self.protein_id = protein_id
        self.base_url = "https://www.ebi.ac.uk/proteins/api/proteins"
        self.data = None

    def fetch_data(self):
        request_url = f"{self.base_url}/{self.protein_id}"
        response = requests.get(request_url, headers={"Accept": "application/json"})

        if response.status_code == 200:
            try:
                # Parse the response text as JSON
                data = response.json()

                # Check if the 'sequence' key exists in the JSON data
                protein_info = data.get('sequence', 'Sequence data not found')

                # Print the sequence
                sequence = protein_info['sequence']
                #print(sequence)
                return sequence
                # Example access (adjust according to the actual structure of your JSON response)
                # This assumes 'data' is a list of dictionaries and you're interested in 'sequence' of the first item
            except ValueError as e:
                # Handle JSON decode error
                print("Failed to decode JSON:", e)
            except KeyError as e:
                # Handle cases where key might not exist
                print("Key error:", e)
            except IndexError as e:     
                # Handle cases where the index might be out of range
                print("Index error:", e)
        else:
            print("Failed to retrieve data:", response.status_code)
            print("Response text:", response.text)  # This will show more details about the error


# Example of how to instantiate and use the visualizer:
if __name__ == "__main__":
    protein_id = "2lyz.pdb"  # Default or example protein ID
    parser = PDB_Parser(protein_id)
    visualizer = ProteinVisualizer(parser)
    visualizer.run()
