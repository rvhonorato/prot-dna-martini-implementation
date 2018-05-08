# DNA BB angles
bb_angles = []
angles_param = []
for i, p in enumerate(dna_con['angle']):
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    atomC = atom_name_dic[p[2]]
    #
    bb_angles.append('  ANGLE %s %s %s' % (atomA, atomB, atomC))
    #
    angle_type, equil, opts = dna_bb['angle'][i]
    
    # print m_beadA, m_beadB, m_beadC, angle_type, equil, opts
    m_beadA = beads[p[0]]
    m_beadB = beads[p[1]]
    m_beadC = beads[p[2]]
    h_beadA = [e for e in bead_dic if bead_dic[e] == m_bead and bead_type_key in e[:len(bead_type_key)]][0]
    h_beadB = [e for e in bead_dic if bead_dic[e] == m_bead and bead_type_key in e[:len(bead_type_key)]][0]
    h_beadC = [e for e in bead_dic if bead_dic[e] == m_bead and bead_type_key in e[:len(bead_type_key)]][0]
    
    angles_param.append('ANGLe %s %s %s %.3f %i' % (h_beadA, h_beadB, h_beadC, equil, opts))
