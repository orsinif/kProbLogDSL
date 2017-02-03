from collections import defaultdict
import networkx as nx
import atexit, inspect, io, os, signal, subprocess, sys

from .config import GRINGO_BIN_FILE_PATH
from .core import FACT_IDENTIFIER, QUERY_IDENTIFIER, INFIX_OPERATORS, INV_INFIX_OPERATORS
from .core import Term, symbols, Clause, RoleTerm
from .semirings import CommutativeMonoid, Meta, VoidMonoid
from .parse.parser import parse_clause
from .utils import stratify_dag, make_relevant_digraph

BUILTIN_PREDICATE_SIGNATURES = [op/2 for op in symbols('==, !=, <=, >=, <, >')]

def remove_builtins(digraph):
    non_builtin_nodes = {
        node
            for node in digraph.nodes()
                if node.signature not in BUILTIN_PREDICATE_SIGNATURES
    }
    return digraph.subgraph(non_builtin_nodes)
    
class MetaClause(Clause):
    def __init__(self, head, body, mf_id, meta_function):
        super(self.__class__, self).__init__(head, body, mf_id)
        self.meta_function = meta_function
        assert not isinstance(self.meta_function, MetaClause) # XXX
    
    def is_cyclic(self, atoms):
        return any((b in atoms) for b in self.body)
    
    def eval(self, atom2label, pred_signature2monoid):
        args = []
        body_idx = 0
        vnames = inspect.getfullargspec(self.meta_function).args
        for varname in vnames:
            atom = self.meta_function.__annotations__[varname].strip_role()
            monoid, _ = pred_signature2monoid[atom.signature]
            if isinstance(monoid, Meta):
                arg = self._ground_annotations(pred_signature2monoid)
            else:
                atom = self.body[body_idx]
                if atom.signature not in BUILTIN_PREDICATE_SIGNATURES:
                    # arg = monoid.parse_function_arg(atom=atom, value=atom2label[atom])
                    arg = monoid.parse_function_arg(
                        atom=atom,
                        value=atom2label.get(atom, monoid.zero)
                    )
                else:
                    arg = None # FIXME we need the identity. In this case since builtins all use the VoidMonoid we just use None (which is the identity of the VoidMonoid)
                body_idx += 1
            args.append(arg)
        return self.meta_function(*args)
    
    def _ground_annotations(self, pred_signature2monoid):
        annotations = {}
        body_idx = 0
        vnames = inspect.getfullargspec(self.meta_function).args
        for varname in vnames:
            atom = self.meta_function.__annotations__[varname]
            atom_norole = atom.strip_role()
            monoid, _ = pred_signature2monoid[atom_norole.signature]
            if not isinstance(monoid, Meta):
                ground_atom = self.body[body_idx]
                if isinstance(atom, RoleTerm):
                    ground_atom = RoleTerm(ground_atom, atom.role)
                annotations[varname] = ground_atom
                body_idx += 1
        annotations['return'] = self.head
        return annotations
            
    def to_gringo4_str(self, pred_signature2monoid):
        # TODO remove pred_signature2monoid from the arguments
        return str(self.strip_roles())

def make_metaclause(meta_function):
    vnames = inspect.getfullargspec(meta_function).args
    vname2term = meta_function.__annotations__
    head = vname2term['return']
    body = [vname2term[vname].strip_role() for vname in vnames]
    if not isinstance(head, Term):
        raise TypeError
    if not all(isinstance(b, Term) for b in body):
        raise TypeError
    mf_id = meta_function.__name__
    if mf_id.startswith('_') or mf_id[0].isupper():
        raise ValueError            
    if mf_id == FACT_IDENTIFIER or mf_id == QUERY_IDENTIFIER:
        raise ValueError
    return MetaClause(head, body, mf_id, meta_function)


def kill_gringo(child_pid):
    if child_pid is not None:
        os.kill(child_pid, signal.SIGTERM)


class DeclareHelper(object):
    def __init__(self, kproblog, additive_flag):
        if not isinstance(kproblog, KProbLog):
            raise TypeError
        self.kproblog = kproblog
        self.additive_flag = additive_flag
    
    def __getitem__(self, monoid_type):
        if not isinstance(monoid_type, CommutativeMonoid) and not isinstance(monoid_type, Meta):
            raise TypeError
        
        pred_signature2monoid = self.kproblog.pred_signature2monoid
        def declaration(*pred_signature_list):
            for pred_signature in pred_signature_list:
                assert pred_signature.functor == '/'
                pred_signature2monoid[pred_signature] = monoid_type, self.additive_flag

        return declaration
            

class KProbLog(object):
    def __init__(self, gringo_bin_file_path=GRINGO_BIN_FILE_PATH, debug_flag=False):
        self.gringo_bin_file_path = gringo_bin_file_path
        self.debug_flag = debug_flag
        self.mf_id2metaclause = {}
        self.pred_signature2monoid = {}
        # INIT BUILTIN DECLARATIONS
        self.declare[VoidMonoid()](*BUILTIN_PREDICATE_SIGNATURES) # TODO might not be needed anymore if the builtins have been stripped

    def __call__(self, func):
        mc = make_metaclause(func)
        self._check_metaclause_declaration(mc)    
        if mc.mf_id in self.mf_id2metaclause:
            raise ValueError('duplicate meta function identifier "{}"'.format(mc.mf_id))
        self.mf_id2metaclause[mc.mf_id] = mc
        return func
    
    @property
    def declare(self):
        return DeclareHelper(self, additive_flag=False)

    def _declare_many(self, monoid2pred_signature_list, additive_flag):
        for monoid, pred_signature_list in monoid2pred_signature_list.items():
            declare_helper = DeclareHelper(self, additive_flag=additive_flag)
            declare_helper[monoid](*pred_signature_list)

    def declare_destructive_many(self, monoid2pred_signature_list):
        self._declare_many(monoid2pred_signature_list, additive_flag=False)
        
    def declare_additive_many(self, monoid2pred_signature_list):
        self._declare_many(monoid2pred_signature_list, additive_flag=True)
        

    def _check_metaclause_declaration(self, mc):
        if not isinstance(mc, MetaClause):
            raise TypeError
        atom_list = [mc.head] + list(mc.body)
        for atom in atom_list:
            if atom.signature not in self.pred_signature2monoid:
                raise TypeError("atom {} has unknown signature {} in function {}"
                    .format(atom, atom.signature, mc.meta_function.__code__))
    
    def to_clause(self, obj, query_flag=False):
        conj, is_true, true, dont_care = symbols('conj is_true true _')
        if isinstance(obj, Term) and not query_flag:
            mf_id_const, = symbols(FACT_IDENTIFIER)
            clause_head = is_true(mf_id_const, obj, true)
            clause_body = ()
            meta_function = None
        elif isinstance(obj, Term) and query_flag:
            mf_id_const, = symbols(QUERY_IDENTIFIER)
            clause_head = is_true(mf_id_const, obj, true)
            clause_body = (is_true(dont_care, obj, dont_care),)
            meta_function = None
        elif isinstance(obj, MetaClause):
            obj = self.strip_meta(obj) # STRIP META-ARGUMENTS
            mf_id_const, = symbols(obj.mf_id)
            clause_head = is_true(mf_id_const, obj.head, conj(*obj.body))
            clause_body = []
            for arg in obj.body:
                if isinstance(arg, Term) and arg.functor in INFIX_OPERATORS:
                    clause_body.append(arg)
                else:
                    clause_body.append(is_true(dont_care, arg, dont_care))
            clause_body = tuple(clause_body)
            meta_function = self.mf_id2metaclause[mf_id_const.functor].meta_function
        else:
            raise TypeError(type(obj))
        return MetaClause(clause_head, clause_body, mf_id_const.functor, meta_function)
    
    def strip_meta(self, mf):
        assert isinstance(mf, MetaClause)
        if isinstance(self.get_monoid(mf.head), Meta):
            raise TypeError("Meta-heads are not allowed")
        
        new_body = [b for b in mf.body if not isinstance(self.get_monoid(b), Meta)]
        return MetaClause(mf.head, new_body, mf.mf_id, mf.meta_function)

    def program_gen(self, query, facts):
        objs = list(self.mf_id2metaclause.values()) + list(facts)
        clauses = list(map(self.to_clause, objs)) + [self.to_clause(query, True)]
        for clause in clauses:
            yield clause
        
    def ground_gen(self, query, facts):
        program_file = io.StringIO()
        for clause in self.program_gen(query, facts):
            clause_str = clause.to_gringo4_str(self.pred_signature2monoid)
            program_file.write(clause_str + '\n')
        
        grounding_file = io.StringIO()
        
        proc = subprocess.Popen(
            [self.gringo_bin_file_path, '-t'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        atexit.register(kill_gringo, proc.pid) # REGISTER GRINGO
        
        if self.debug_flag:
            print("DEBUG: BEGIN PROGRAM")
            print(program_file.getvalue())
            print("DEBUG: END PROGRAM")
        
        stdout_lines, stderr_lines = proc.communicate(program_file.getvalue())
        program_file.close()

        assert stderr_lines is None
        if self.debug_flag:
            print("DEBUG: BEGIN GROUND PROGRAM")
        for line in sorted(stdout_lines.split('\n')): # FIXME should not be necessary
            line = line.strip()
            if line and not line.startswith('#'):
                if self.debug_flag:
                    print(line)
                query_flag, clause = parse_clause(line, INV_INFIX_OPERATORS)
                yield query_flag, clause
        if self.debug_flag:
            print("DEBUG: END GROUND PROGRAM")
        atexit.unregister(kill_gringo) # UNREGISTER GRINGO
    
    def get_monoid(self, atom):
        return self.pred_signature2monoid[atom.signature][0]
    
    def parse_facts(self, facts):
        parsed_facts = {
            atom:self.get_monoid(atom).parse_value(atom, label) 
                for atom, label in facts.items()
        }
        return parsed_facts

    def ground(self, query, facts):
        if query.signature not in self.pred_signature2monoid:
            raise ValueError( "undeclared predicate {}".format(query.signature))
        facts = self.parse_facts(facts)
        clause_list = []
        query_set = set()
        for query_flag, clause in self.ground_gen(query, facts):
            if not query_flag:
                if clause.mf_id == FACT_IDENTIFIER:
                    meta_function = None # None in case it is a fact
                else:
                    meta_function = self.mf_id2metaclause[clause.mf_id].meta_function
                meta_clause = MetaClause(clause.head, clause.body, clause.mf_id, meta_function)
                clause_list.append(meta_clause)
            else:
                query_set.add(clause.head)

        obj = GroundCircuit(query_set, facts, clause_list, self.pred_signature2monoid)
        return obj

class GroundCircuit(object):
    def __init__(self, query_set, facts, clause_list, pred_signature2monoid):
        self.digraph = nx.DiGraph()
        self.query_set = query_set
        self.facts = facts
        self.pred_signature2monoid = pred_signature2monoid
        self._create_from(clause_list)
    
    def get_monoid(self, atom):
        return self.pred_signature2monoid[atom.signature][0]

    def _create_from(self, clause_list):
        for clause in clause_list:
            self.add_node(clause.head)
            if 'clauses' not in self.digraph.node[clause.head]:
                self.digraph.node[clause.head]['clauses'] = []
            self.digraph.node[clause.head]['clauses'].append(clause)
            for b in clause.body:
                self.add_node(b)
                self.add_edge(b, clause.head)
        self.digraph = remove_builtins(self.digraph)
        self.digraph = make_relevant_digraph(self.digraph, self.query_set)

    def add_node(self, atom):
        self.digraph.add_node(atom)
    
    def add_edge(self, u, v, **kwargs):
        if not self.digraph.has_node(u):
            raise ValueError
        if not self.digraph.has_node(v):
            raise ValueError
        self.digraph.add_edge(u, v, **kwargs)
    
    def nodes(self, *args, **kwargs):
        return self.digraph.nodes(*args, **kwargs)

    def edges(self, *args, **kwargs):
        return self.digraph.edges(*args, **kwargs)
        
    def compile(self):
        return StratumSequence(self, self.query_set, self.facts)


class Stratum(object):
    def __init__(self, ground_circuit, atoms):
        debug_flag = False
        
        self.pred_signature2monoid = ground_circuit.pred_signature2monoid
        self.acyclic_rules = set()
        self.cyclic_rules = set()
        self.debug_flag = debug_flag
        
        if self.debug_flag:
            self.atoms = atoms # TODO remove
        
        for atom in atoms:
            if atom.arity == 2 and atom.functor in INFIX_OPERATORS:
                raise ValueError # we assume that we stripped the builtins
            # meta_clauses = [mc for mc in ground_circuit.digraph.node[atom]['clauses'] if mc.meta_function is not None]
            meta_clauses = ground_circuit.digraph.node[atom]['clauses']
            for mc in meta_clauses:
                if mc.is_cyclic(atoms):
                    self.cyclic_rules.add(mc)
                else:
                    self.acyclic_rules.add(mc)

    def get_monoid(self, atom):
        return self.pred_signature2monoid[atom.signature][0]

    def pretty_print(self):
        print("acyclic_rules")
        for mc in self.acyclic_rules:
            print("\t", str(mc))
        print()
        print("cyclic_rules")
        for mc in self.cyclic_rules:
            print("\t", str(mc))
        print()
    
    def tp_update(self, atom2label):
        pred_signature2monoid = self.pred_signature2monoid
        
        # EVALUATE ACYCLIC RULES
        atom2new_label = self._tp_operator(self.acyclic_rules, atom2label)
        self.weight_update(atom2label, atom2new_label, acyclic_flag=True)

        # EVALUATE CYCLIC RULES
        if self.cyclic_rules and self.debug_flag:
            print('cyclic_rules progress ', end='')
        while self.cyclic_rules: # loop if there are cyclic rules (i.e. self.cyclic_rules is not empty)
            if self.debug_flag:
                print(".", end=''); sys.stdout.flush()
            if self.debug_flag: self._debug_cyclic_rules(self.cyclic_rules, self.atoms)
            delta_atom2label = self._tp_operator(self.cyclic_rules, atom2label)
            atom2label_old = dict(atom2label)
            self.weight_update(atom2label, delta_atom2label, acyclic_flag=False)
            if self.is_the_same(atom2label, atom2label_old):
                if self.debug_flag:
                    print()
                break
        return atom2label
    
    def is_the_same(self, atom2label, atom2label_old):
        if set(atom2label) == set(atom2label_old):
            for atom, value in atom2label.items():
                if not (value == atom2label_old[atom]):
                    # print("\tatom: {} vs {}".format(value, atom2label_old[atom]))
                    return False
            return True
        else:
            return False
    
    def weight_update(self, atom2label, delta_atom2label, acyclic_flag):
        for atom, value in delta_atom2label.items():
            if atom not in atom2label:
                atom2label[atom] = value
            else:
                monoid, additive_flag = self.pred_signature2monoid[atom.signature]
                if acyclic_flag or additive_flag:
                    atom2label[atom] = monoid.sum([atom2label[atom], value])
                else:
                    atom2label[atom] = value
                    

    def _debug_cyclic_rules(self, cyclic_rules, atoms):
        digraph = nx.DiGraph()
        for mc in self.cyclic_rules:
            assert any((b in atoms) for b in mc.body)
            for b in mc.body:
                if b.signature not in BUILTIN_PREDICATE_SIGNATURES:
                    digraph.add_edge(b, mc.head)
        print("CYCLIC DIGRAPH")
        print("\tnodes", digraph.nodes())
        print("\tedges", digraph.edges())
        if not nx.is_strongly_connected(digraph):
            raise ValueError
        else:
            print("DEBUG:\n\tis_strongly_connected!")

    def _tp_operator(self, meta_clauses, atom2label):
        atom2new_label_list = defaultdict(list)
        for mc in meta_clauses:
            if mc.meta_function is not None:
                value = mc.eval(atom2label, self.pred_signature2monoid)
                atom2new_label_list[mc.head].append(value)
        atom2new_label = {
            atom: self.get_monoid(atom).sum(values)
                for atom, values in atom2new_label_list.items()
        }
        return atom2new_label
    
    def __repr__(self):
        s = "Stratum(acyclic = {}, cyclic = {})" \
                .format(self.acyclic_rules, self.cyclic_rules)
        return s

class StratumSequence(object):
    def __init__(self, ground_circuit, query_set, facts):
        digraph = ground_circuit.digraph
        if digraph.nodes():
            C = nx.condensation(digraph)
        else:
            C = nx.DiGraph() # in case the ground_circuit is empty

        strata = []
        for stratum_id_list in stratify_dag(C):
            for stratum_id in stratum_id_list:
                atoms = C.node[stratum_id]['members']
                stratum = Stratum(ground_circuit, atoms)
                strata.append(stratum)

        self.ground_circuit = ground_circuit
        self.query_set = query_set
        self.facts = facts
        self.strata = strata
    
    def pretty_print(self):
        print('=' * 80)
        print('=' * 80)
        print('STRATUM')
        for stratum in self.strata:
            stratum.pretty_print()
        print('=' * 80)
    
    def query(self):
        # TODO make it a generator
        atom2label = dict(self.facts)
        for stratum in self.strata:
            atom2label = stratum.tp_update(atom2label)
        return {qatom: atom2label[qatom] for qatom in self.query_set}
