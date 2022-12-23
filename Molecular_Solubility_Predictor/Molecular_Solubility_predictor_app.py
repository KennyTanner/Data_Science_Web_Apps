import pandas as pd
import numpy as np
import pickle
import streamlit as st
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Descriptors

# Calculate molecular descriptors
def AromaticProportion(m):
  aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
  aa_count = []
  for i in aromatic_atoms:
    if i==True:
      aa_count.append(1)
  AromaticAtom = sum(aa_count)
  HeavyAtom = Descriptors.HeavyAtomCount(m)
  AR = AromaticAtom/HeavyAtom
  return AR

def generate(smiles, verbose=False): # (Simplified Molecular Input Line Entry System) for users to enter in side panel

    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData= np.arange(1,1)
    i=0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

# Title
image = Image.open('logo.jpg')
st.image(image, use_column_width=True)
st.write("""
#### This app predicts the **aqueous solubility (LogS)** of any molecule you wish to enter. A key factor in drug efficacy. With poor aqueous solubilty a drug is difficult to make highly bioavailable.

This follows John S. Delaney's work, with the method outlined in, and data obtained from [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.

A excellent demonstration of how a simple linear regression model can achieve similar results to the "General Solubility Equation".

Making light work of a complex problem and setting the stage for ML to become a major player in bioinformatics [Molecular Machine Learning: The Future of Synthetic Chemistry?](https://doi.org/10.1002/anie.202008366). ***P. M. Pflüger, F. Glorius, Angew. Chem. Int. Ed.*** 2020, 59, 18860.

This app followed guidance by Chanin Nantasenamat (aka Data Professor) http://youtube.com/dataprofessor
""")

# Input molecules (Side Panel)
st.sidebar.header('User Input Features')

# Most molecule's SMILES can be found on https://pubchem.ncbi.nlm.nih.gov/
SMILES_input = "NCCCC\nCN\nCN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O\COO"

SMILES = st.sidebar.text_area("SMILES input", SMILES_input)
SMILES = "C\n" + SMILES # Adds C as a dummy first item   --- to work around a bug when only one molecule SMILES is entered
SMILES = SMILES.split('\n')

st.header('Input SMILES')
SMILES[1:] # Skips the dummy

# Calculate molecular descriptors
st.header('Computed Molecular Descriptors')
X = generate(SMILES)
X[1:] # Skips the dummy

# Reads the pre-built model saved
load_model = pickle.load(open('solubility_model.pkl', 'rb'))

prediction = load_model.predict(X)
#prediction_proba = load_model.predict_proba(X)

st.header('Predicted LogS values')
prediction[1:] # Skips the dummy