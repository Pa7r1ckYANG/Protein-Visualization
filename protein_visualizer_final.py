import py3Dmol
import streamlit as st
from stmol import *
import ipython_genutils
import requests

st.sidebar.title('Molecule Visualizer')
st.sidebar.write('This molecule visualizer is able to visualize'
                 'the protein based on the protein ID, and label'
                 'residues you wish to visualize')


# stmol
def render_mol(pdb):
    """
    This function encrypts a user defined message
    and returns the encrypted message as a list of integers
    **Parameters**
        message: *str*
            User defined message
        N: *int*
            Key component
        E: *int*
            Public key component
    **Returns**
        encrypted_message: *list*
            The encrypted message as a list of integers
    """
    xyzview = py3Dmol.view(query=pdb)
    xyzview.setStyle({'cartoon': {'color': 'spectrum'}})
    xyzview.zoomTo()
    showmol(xyzview, height=500, width=800)


# Protein sequence input
protein_id = "2lyz"
txt1 = st.sidebar.text_area('Input Protein Id', protein_id, height=50)

residue = "HIS"
txt2 = st.sidebar.text_area('Input residues you want to'
                            'visualize', residue, height=50)

accession = "P00698"
txt3 = st.sidebar.text_area('Input protein accession number to'
                            'obtain its sequence (can be different from'
                            'the protein you wish to visualize)',
                            accession, height=50)


def update(sequence=txt1):
    """
    This function updates everytime the user clicks
    on the "visualize" button and generate a
    visualization of the protein.
    **Parameters**
        sequence: *str*
            id of the protein
    **Returns**
    """
    st.subheader('Visualization of protein structure')
    render_mol(txt1)


def annotate(residue=txt2, sequence=txt1):
    """
    This function labels the residue that
    the user specifies.
    **Parameters**
        residue: *str*
            abbreviation of the residue user
            wish to visualize
        sequence: *str*
            id of the protein
    **Returns**
    """
    st.subheader('Annotation of protein structure')
    xyzview = py3Dmol.view(query=sequence)
    xyzview.setStyle({'cartoon': {'color': 'spectrum'}})
    xyzview.zoomTo()
    showmol(render_pdb_resn(xyzview, resn_lst=[txt2, ]))


def view_sequence(accession=txt3):
    """
    This function access the Europe
    Bioinformatics Institute API to obtain
    the sequence of the protein based
    on protein accession number.
    **Parameters**
        accession: *str*
            Protein accession number
    **Returns**
    """
    st.subheader('API application for protein sequence acquirement')
    base_url = "https://www.ebi.ac.uk/proteins/api/proteins"
    data = None
    request_url = f"{base_url}/{txt3}"
    response = requests.get(request_url, headers={"Accept":
                                                  "application/json"})

    if response.status_code == 200:
        try:
            # Parse the response text as JSON
            data = response.json()

            # Check if the 'sequence' key exists in the JSON data
            protein_info = data.get('sequence', 'Sequence data not found')

            # Print the sequence
            sequence = protein_info['sequence']
            st.info('API used: "https://www.ebi.ac.uk/proteins/api/proteins"')
            st.info(sequence)
        except ValueError as e:
            # Handle JSON decode error
            print("Failed to decode JSON:", e)
        except KeyError as e:
            # Handle cases where key might not exist
            print("Key error:", e)
        except IndexError as e:
            # Handle cases where the index might be
            # out of range
            print("Index error:", e)
    else:
        print("Failed to retrieve data:", response.status_code)
        # This will show more details about the error
        print("Response text:", response.text)


# Interactive Buttons
visualize = st.sidebar.button('Visualize!', on_click=update(txt1))
annotate = st.sidebar.button('Annotate!', on_click=annotate(txt2, txt1))
view_sequence = st.sidebar.button('View Sequence!',
                                  on_click=view_sequence(txt3))
