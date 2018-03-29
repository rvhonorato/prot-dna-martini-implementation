
m_dic = collections.OrderedDict()

for aares in chain: 
    m_dic[aares] = collections.OrderedDict()
    resn = aares.resname.split()[0] # resname
    segid = aares.segid.strip() 
    resi = aares.id[1]
    # for each atom segment, calculate its center of mass and map the correct bead
    for atom_segment in cg_mapping[resn]:
        atoms = [aares[a] for a in atom_segment.split() if a in aares.child_dict]

        if '*' in atom_segment:
            # this * means it belongs to the previous residue... find it!
            target_previous_atom_list = [a for a in atom_segment.split() if '*' in a]

            for target_atom in target_previous_atom_list:
                # does it exist?
                target_atom_name = target_atom.split('*')[0]
                try:
                    previous_atom = chain[resi-1][target_atom_name]
                    # how far away the previous atom is from this atom segment? 
                    #  if it is too far away this could be the next chain...!
                    minimum_dist = min([(a-previous_atom) for a in atoms])
                    if minimum_dist < 2.0: # 2.0 A is very permissive
                        atoms.append(previous_atom) 
                except KeyError:
                    # previous atom not found, move on
                    pass
        if 'O1P' in atom_segment:
            if resn == 'DT':
                print atom_segment, atoms, resn, resi
            # exit(
        bead_name = cg_mapping[resn][atom_segment]
        if not atoms:
            print 'Residue %s %i of chain %s cannot be processed: missing atoms %s ' % (resn, resi, aares.parent.id, atom_segment)
            continue
        # get center of mass
        code = list(set([a.bfactor for a in aares if a.bfactor != 0]))
        # print aares, [a.bfactor for a in aares]
        # exit()
        #
        if len(code) > 1:
            print 'Something is wrong with HADDOCK codes'
            exit()
        if not code:
            code = 0.0
        else:
            code = code[0]
        # print , atoms, bead_name
        # exit()
        bead_coord = center_of_mass(atoms)
        # restrain for backmapping
        restrain = "assign (segid %sCG and resid %i and name %s) (segid %s and resid %i and (name %s)) 0 0 0" % (segid, resi, bead_name, segid, resi, ' or name '.join(atom_segment.split(' ')))