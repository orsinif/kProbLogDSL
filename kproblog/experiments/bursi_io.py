from itertools import groupby
from ..core import symbols

SKIP_PREFIX_LIST = {'con(', 'fus(', 'linked(', 'molecule_id(', 'molecule_name(', 'sub(', 'subat('}


vertex, edge_asymm = symbols('vertex, edge_asymm')

def parse_interpretaion_fact(line):
    START_INTERPRETATION = 'interpretation('
    END_INTERPRETATION = ').'
    assert line.startswith(START_INTERPRETATION) and line.endswith(END_INTERPRETATION)
    interpr_fact_str = line[len(START_INTERPRETATION) :- len(END_INTERPRETATION)]
    interpretation_id, *other = interpr_fact_str.split(',')
    return interpretation_id, ','.join(other)

class FactParser(object):
    def parse_interpretations_gen(self, pl_file_name):
        iids = set()
        for iid, t_it in groupby(self._parse(pl_file_name), lambda x:x[0]):
            if iid in iids:
                raise ValueError
            iids.add(iid)            
            facts = {
                self._parse_fact(fact_str)
                    for _, fact_str in t_it
                        if not any(fact_str.startswith(prefix) for prefix in SKIP_PREFIX_LIST)
            }
            yield self._facts2y_data(facts)

    def _parse_fact(self, fact_str):
        assert fact_str.count('(') == 1 and fact_str.count(')') == 1 and fact_str.endswith(')'), fact_str
        functor, *args_str = fact_str[:-1].split('(')
        assert len(args_str) == 1
        functor, = symbols(functor)
        args = [
            tuple(symbols(arg_str.strip()))[0]
                for arg_str in args_str[0].split(',')
        ]
        return functor(*args)
    
    def _parse(self, pl_file_name):
        with open(pl_file_name) as pl_file:
            for line in pl_file:
                line = line.strip()
                if line == '': continue
                interpretation_id, fact_str = parse_interpretaion_fact(line)
                yield interpretation_id, fact_str

    def _facts2y_data(self, facts):
        data = {}
        target = None
        for fact in facts:
            if fact.functor == 'a':
                assert fact.arity == 2
                v, label = fact.args
                data[vertex(v)] = {label:1.}
            elif fact.functor == 'b':
                assert fact.arity == 3
                v, w, label = fact.args
                data[edge_asymm(v, w)] = {label:1.}
            elif fact.functor == 'target':
                assert fact.arity == 1
                assert target is None
                target, = fact.args
            else:
                raise ValueError(('fact', fact))
        assert target is not None, ("target", target)
        y =  1 if target.functor == 'mutagen' else -1
        return y, data
