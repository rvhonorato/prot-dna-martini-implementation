"""Creates a scorers file ready to be sent"""

import os
import sys

remarks = """AUTHOR   1 Alexandre M.J.J. Bonvin, Cunliang Geng, Jorge Roel,
AUTHOR   2 Li Xue, Adrien Melquiond, Mikael Trellet, Joerg Schaarschmidt,
AUTHOR   3 Panagiotis Koukos, Francesco Ambrosetti, Brian Jimenez Garcia,
AUTHOR   3 Rodrigo Vargas Honorato
REMARK   1
REMARK   1 Models scored by the HADDOCK server
REMARK   2
REMARK   2 REFERENCE 1
REMARK   2  AUTH   S.J.de Vries, M. van Dijk, A.M.J.J. Bonvin
REMARK   2  TITL   The HADDOCK web server for data-driven biomolecular docking
REMARK   2  TITL 2 of HADDOCK2.0 on the CAPRI targets
REMARK   2  REF    Nature Protocols              V.5      883 2010
REMARK   3
REMARK   3 REFERENCE 2
REMARK   3  AUTH   G.C.P van Zundert, J.P.G.L.M. Rodrigeus, M. Trellet,
REMARK   3  AUTH 2 C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond
REMARK   3  AUTH 3 M. van Dijk, S.J. de Vries, A.M.J.J. Bonvin
REMARK   3  TITL   The HADDOCK2.2 webserver: User-friendly integrative
REMARK   3  TITL 2 modeling of biomolecular complexes.
REMARK   3  REF    J.Mol.Biol., 428, 720-725 (2015).
REMARK     CASP ID AUTHOR 3472-4644-8807
"""


def usage():
    """Prints an usage message"""
    print("Usage: %s md5_file list_of_pdb_files scorers_file.pdb" % (sys.argv[0]))
    print("  example: %s Target152.MD5 top10.list T152-scorers-top10.pdb" % (sys.argv[0]))
    raise SystemExit("ERROR: Wrong parameters")


def read_models_list(file_name):
    """Reads the list of models"""
    models = []
    with open(file_name) as input_models:
        for line in input_models:
            model_file = line.rstrip(os.linesep)
            if model_file:
                models.append(model_file)
    return models


def parse_md5_file(file_name):
    """Parses the file containing the MD5 records and returns them"""
    hashes = {}
    with open(file_name) as hashes_file:
        for line in hashes_file:
            if line.startswith("REMARK   9"):
                # REMARK   9 MODEL        0 MD5 f5974f4bb9e784387fdbf48a977c4303
                line = line.rstrip(os.linesep)
                fields = line.split()
                md5 = fields[-1]
                model = int(fields[-3])
                hashes[model] = md5
    return hashes


if __name__ == "__main__":

    if len(sys.argv[1:]) < 3:
        usage()

    # Check for input files
    hashes_file = sys.argv[1]
    models_file = sys.argv[2]
    output_file_name = sys.argv[3]

    if not os.path.isfile(hashes_file):
        raise SystemExit("ERROR: CAPRI MD5 hashes file %s does not exist" % (hashes_file))

    if not os.path.isfile(models_file):
        raise SystemExit("ERROR: Models file %s does not exist" % (models_file))

    if os.path.isfile(output_file_name):
        raise SystemExit("ERROR: Output file %s already exists" % (output_file_name))

    # Read models
    models_list = read_models_list(models_file)

    # Parse brk file:
    hashes = parse_md5_file(hashes_file)

    # Write selection to prediction file:
    with open(output_file_name, 'w') as output:
        # Write current HEADER
        output.write(remarks)
        for model_file_name in models_list:
            model_id = int(model_file_name.split('_')[1])
            output.write("REMARK     MODEL   %6d MD5 %s" % (model_id, hashes[model_id]) + os.linesep)

        for model_file_name in models_list:
            print("Reading model from file %s..." % (model_file_name))
            with open(model_file_name) as model_file:
                model_id = int(model_file_name.split('_')[1])
                output.write("MODEL   %6d" % model_id + os.linesep)
                for line in model_file:
                    if line[0:6].strip() not in ["REMARK", "END"]:
                        output.write(line)
                output.write("ENDMDL" + os.linesep)

        output.write("END" + os.linesep)

    print("Scorers file %s generated." % (output_file_name))

