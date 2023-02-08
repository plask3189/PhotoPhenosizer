#variable_support

# pass in images here from kickoff window.
global tif_files
class Variable_Support:
  def __init__(self, tif_files):
    self.tif_files = tif_files




    def return_tif_names(self):
        print("returning works!")
        return tif_files

def storing_variables():
    print("returning works here!")
    return tif_files
