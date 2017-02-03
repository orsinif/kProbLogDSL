from ..core import symbols
from collections import defaultdict
import glob, os

vertex, edge_asymm = symbols('vertex, edge_asymm')


MUTAG_PL_FOLDER = 'data/mutagenesis/188/'
ATOM_BOND_FILE_NAME = 'data/mutagenesis/common/atom_bond.pl'

class ParseFacts(object):
    def parse_fact(self, fact_str):
        assert fact_str.endswith(').'), fact_str
        functor, *args_str = fact_str[:-2].split('(')
        args_str  = '('.join(args_str)
        args = tuple(map(lambda x:x.strip(), args_str.split(',')))
        return functor, args

def parse_pl_atom_bond_file(fact_parser):
    molecule_id2fact_dict = defaultdict(dict)
    functor_set = set()
    with open(ATOM_BOND_FILE_NAME) as pl_file:
        for line in pl_file:
            line = line.strip()
            if line == '': continue
            functor, args = fact_parser.parse_fact(line)
            functor_set.add(functor)
            if functor == 'atm':
                molecule_id, atom_id, atom_label, _, _ = args
                atom_id, = symbols(atom_id)
                atom_label, = symbols(atom_label)
                molecule_id2fact_dict[molecule_id][vertex(atom_id)] = {
                    atom_label:1.
                }
            elif functor == 'bond':
                molecule_id, atom_id1, atom_id2, bond_label = args
                atom_id1, = symbols(atom_id1)
                atom_id2, = symbols(atom_id2)
                edge_label, = symbols(bond_label) 
                molecule_id2fact_dict[molecule_id][edge_asymm(atom_id1, atom_id2)] = {
                    edge_label:1.
                }
            else:
                raise ValueError
    return dict(molecule_id2fact_dict)

def parse_pl_ground_truth():
    fact_parser = ParseFacts()
    for pl_file_name in glob.iglob('data/mutagenesis/188/*.pl'):
        with open(pl_file_name) as pl_file:
            for line in pl_file:
                line = line.strip()
                target = 1
                if line.startswith(':-'):
                    target = -1
                    line = line[2:].strip()
                functor, (molecule_id,) = fact_parser.parse_fact(line)
                assert functor == 'active'
                yield (target, molecule_id)
        
def mutag_gen():
    fact_parser = ParseFacts()
    molecule_id2fact_dict = parse_pl_atom_bond_file(fact_parser)
    
    for y_i, mol_id in parse_pl_ground_truth():
        data_i = molecule_id2fact_dict[mol_id]
        yield y_i, data_i