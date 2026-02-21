from sorting_algos import create_folder, Folder

# Create root folder object [!DO NOT CHANGE!]
drop_point = Folder(name='Drop Point')

# 1. Create top level folders
mw = create_folder('Many Worlds', drop_point, {'composer': 'MW-'})
cc = create_folder('Coromandel Club', drop_point, {'composer': 'CC-'})
delete = create_folder('2_DELETE', drop_point, {'composer': 'DELETE'})
home = create_folder('Home', drop_point, {'composer': 'Home'})

# MW Solid folders
mw_solid = create_folder('Solid', mw, {'composer': 'MW-Solid'})
flow = create_folder('Flow', mw_solid, {'genre': ['Rap']})
ambitrap = create_folder('Ambi-trap', mw_solid, {'genre': ['Trap']})
pop_dilutions = create_folder('Pop dilutions', mw_solid, {'genre': ['Pop']})
trance_adj = create_folder('Trancy', mw_solid, {'genre': ['Trance']})

# MW Liquid folders
mw_liquid = create_folder('Liquid', mw, {'composer': 'MW-Liquid'})
spiral = create_folder('Spiral', mw_liquid, {'comment': ('Abstract', 'Deep')})

# MW Air folders
mw_air = create_folder('Air', mw, {'composer': 'MW-Air'})

# 1b. Create CC subfolders
cc_slow = create_folder('90-118', cc, {'bpm': (90, 118)})
cc_mid = create_folder('118-128', cc, {'bpm': (118, 128)})
cc_fast = create_folder('128-150', cc, {'bpm': (128, 150)})
cc_fastest = create_folder('150+', cc, {'bpm': (150, 300)})

# Test folder with lyricist condition
sparkling = create_folder('Sparkling', cc_fast, {'lyricist': ['Build', 'Sustain'],
                                                 'comment': ['Sparkling']})
