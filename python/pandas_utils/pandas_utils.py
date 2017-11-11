import pandas as pd

def hdf5_to_ascii(inp, out, separator, float_format="%.4e"):
    
    df = pd.read_hdf(inp)
    df.to_csv(out, sep=separator, index=False, float_format=float_format)

def ascii_to_hdf5(inp, out, key, format='table', complib='blosc'):
    
    df = pd.read_table(inp, delim_whitespace=True)
    df.to_hdf(out, key=key, format=format, complib=complib)

def test():
    print('Test.')
