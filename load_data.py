import scipy.io

def load_data(file: str):
    mat = scipy.io.loadmat(file)
    return mat['TPO'], mat['s']