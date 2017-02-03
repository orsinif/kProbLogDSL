import subprocess

proc = subprocess.Popen(
    ['hostname'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    universal_newlines=True
)

stdout_lines, stderr_lines = proc.communicate()

if stdout_lines.strip().endswith('.local'):
    GRINGO_BIN_FILE_PATH = '/usr/local/bin/gringo'
else:
    GRINGO_BIN_FILE_PATH = '/usr/bin/gringo'

CLAUSE_PARSER = 'tricky'
# CLAUSE_PARSER = 'parsimonious'
# CLAUSE_PARSER = 'antlr4'
# CLAUSE_PARSER = 'ply'
