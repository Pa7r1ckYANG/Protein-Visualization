import matplotlib as mp
from Bio import SeqIO  # For reading and writing sequence files
from Bio.Seq import Seq  # For working with sequences
from Bio.PDB import PDBParser  # For working with protein data files
import py3Dmol
import tkinter

class PDBFileHandler:
    def __init__(self, pdb_file):
        self.pdb_file = pdb_file
        self.structure = None

    def load_structure(self):
        """Load structure from a PDB file."""
        parser = PDBParser()
        try:
            self.structure = parser.get_structure("PDB_structure", self.pdb_file)
            print("Structure loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading the structure: {e}")

    def display_info(self):
        """Display basic information about the structure."""
        if self.structure:
            for model in self.structure:
                for chain in model:
                    print(f"Model {model.id}, Chain {chain.id}, Number of residues: {len(list(chain))}")
        else:
            print("No structure loaded.")


from Bio.PDB import PDBIO
from io import StringIO

import py3Dmol

class ProteinVisualizer:
    def __init__(self, structure):
        self.structure = structure

    def structure_to_pdb_string(self):
        """Converts the structure to a PDB formatted string using Bio.PDB."""
        from Bio.PDB import PDBIO
        from io import StringIO
        io = PDBIO()
        io.set_structure(self.structure)
        stream = StringIO()
        io.save(stream)
        return stream.getvalue()

    def display_structure(self, style='cartoon', color='spectrum', filename='structure.html'):
        """Visualize the protein structure and save to an HTML file."""
        pdb_string = self.structure_to_pdb_string()
        view = py3Dmol.view(width=800, height=400)
        view.addModel(pdb_string, 'pdb')
        view.setStyle({style: {'color': color}})
        view.zoomTo()

        # Ensure filename is defined before using it
        with open(filename, 'w') as file:
            file.write(view.get_html())
        print(f"Visualization saved to {filename}")

# Example of how to instantiate and use the visualizer:
if __name__ == '__main__':
    from Bio.PDB.PDBParser import PDBParser

    # Make sure the parser and handler are correctly defined and used
    parser = PDBParser()
    structure = parser.get_structure('2lyz', '2lyz.pdb')  # Correct path required
    visualizer = ProteinVisualizer(structure)
    visualizer.display_structure()  # This will save the visualization to 'structure.html'
