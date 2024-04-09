from lfv_parse import process_lfv
def sos_on(lfv: process_lfv , zone: int):
    lfv.Verkeerslicht.SetStand(1)
    while lfv.Verkeerslicht.Stand != 1:
        lfv.Verkeerslicht.update()
    lfv.Afsluitboom.SetStand(1)
    for z in lfv.Verlichting.Zones:
        z.SetAutoRegeling(False)
    lfv.Verlichting.SetStand(10)
    lfv.Matrix.SetStand(1)
    #TODO camera stand toevoegen


def sos_off(lfv: process_lfv ):
    lfv.Afsluitboom.SetStand(2)
    while lfv.Afsluitboom.Stand != 3:
        lfv.Afsluitboom.update()
    lfv.Verkeerslicht.SetStand(2)
    for zone in lfv.Verlichting.Zones:
        zone.SetAutoRegeling(True)
    lfv.Matrix.SetStand(0)
    

