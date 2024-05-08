import requests
import py3Dmol
code = 'P00698'
requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/" + code

response = requests.get(requestURL, headers={ "Accept" : "application/json"})

# if not response.ok:
#   response.raise_for_status()
#   sys.exit()

if response.status_code == 200:
    try:
        # Parse the response text as JSON
        data = response.json()

        # Check if the 'sequence' key exists in the JSON data
        protein_info = data.get('sequence', 'Sequence data not found')

        # Print the sequence
        sequence = protein_info['sequence']
        print(sequence)
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

view = py3Dmol.view()
view.setBackgroundColor('white')
view.addModel(open('2lyz.pdb', 'r').read(),'pdb')
# view.addModel(open('5rh2_aligned.pdb', 'r').read(),'pdb')
view.setStyle({'model':0}, {'cartoon': {'color':'purple'}})
view.setStyle({'model':1}, {'cartoon': {'color':'yellow'}})
view.zoomTo()
view.show()