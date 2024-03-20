

from modbus import *



def get_barrier_data(reg):
    if reg:
        barrier_variables = {
            "beschikbaar": reg[0],
            "beweging": reg[1],
            "obstakel": reg[2],
            "storing": reg[3]
        }
    else:
        barrier_variables = {
            "beschikbaar": None,
            "beweging": None,
            "obstakel": None,
            "storing": None
        }
    
    return barrier_variables

#TODO
def get_sos_data(reg):
    if reg:
        variables = {
        }
    else:
        variables = {
        }
    
    return variables


def get_trafficl_data(reg):
    if reg:
        variables = {
            "niveau": reg[0],
            "capaciteit": reg[1],
            "energieverbr": reg[2],
            "branduren": reg[3]
        }
    else:
        variables = {
            "niveau": None,
            "capaciteit": None,
            "energieverbr": None,
            "branduren": None
        }
    
    return variables

def get_tunnell_data(reg):
    if reg:
        variables = {
            "stand": reg[0],
            "beschikbaar": reg[1],
            "storing": reg[2],
        }
    else:
        variables = {
            "stand": None,
            "beschikbaar": None,
            "storing": None,
        }
    
    return variables

def get_mtm_data(reg):
    if reg:
        variables = {
            "stand": reg[0],
            "beschikbaar": reg[1],
            "flash": reg[2],
            "storing": reg[3]
        }
    else:
        variables = {
            "stand": None,
            "beschikbaar": None,
            "flash": None,
            "storing": None
        }
    
    return variables
