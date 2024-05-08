import py3Dmol
import streamlit as st
from stmol import *
import ipython_genutils
import requests

#st.set_page_config(layout = 'wide')
st.sidebar.title('Molecule Visualizer')
st.sidebar.write('This molecule visualizer is able to visualize the protein based on the protein ID, and label residues you wish to visualize')


# stmol
def render_mol(pdb):
    
    xyzview = py3Dmol.view(query=pdb) 
    xyzview.setStyle({'cartoon':{'color':'spectrum'}})
    xyzview.zoomTo()
    showmol(xyzview, height = 500,width=800)

# Protein sequence input
protein_id = "2lyz"
txt1 = st.sidebar.text_area('Input Protein Id', protein_id, height=50)

residue = "HIS"
txt2 = st.sidebar.text_area('Input residues you want to visualize', residue, height=50)

accession = "P00698"
txt3 = st.sidebar.text_area("Input protein accession number to obtain its sequence (can be different from the protein you wish to visualize)", accession, height=50)
def update(sequence=txt1):
    st.subheader('Visualization of predicted protein structure')
    render_mol(txt1)

    st.download_button(
        label="Download PDB",
        data=txt1,
        file_name='predicted.pdb',
        mime='text/plain',
    )

def annotate(residue=txt2,sequence=txt1):
    xyzview = py3Dmol.view(query=sequence) 
    xyzview.setStyle({'cartoon':{'color':'spectrum'}})
    xyzview.zoomTo()
    showmol(render_pdb_resn(xyzview,resn_lst = [txt2,]))

def view_sequence(accession=txt3):
    base_url = "https://www.ebi.ac.uk/proteins/api/proteins"
    data = None
    request_url = f"{base_url}/{txt3}"
    response = requests.get(request_url, headers={"Accept": "application/json"})

    if response.status_code == 200:
        try:
            # Parse the response text as JSON
            data = response.json()

            # Check if the 'sequence' key exists in the JSON data
            protein_info = data.get('sequence', 'Sequence data not found')

            # Print the sequence
            sequence = protein_info['sequence']
            st.info('Sequence based on the accession number provided:')
            st.info(sequence)
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
visualize = st.sidebar.button('Visualize!', on_click=update(txt1))
annotate = st.sidebar.button('Annotate!', on_click=annotate(txt2, txt1))
view_sequence = st.sidebar.button('View Sequence!', on_click=view_sequence(txt3))

