import py_compile, glob, sys

EXCLUDE_DIRS = {'venv', '.venv', '.git', '__pycache__'}
all_files = glob.glob('**/*.py', recursive=True)
files = [f for f in all_files if not any(part in EXCLUDE_DIRS for part in Path(f).parts)]
errors = []
for f in files:
    try:
        py_compile.compile(f, doraise=True)
    except Exception as e:
        errors.append((f, str(e)))

if errors:
    print('SYNTAX ERRORS FOUND:')
    for f, e in errors:
        print(f"{f}: {e}")
    sys.exit(1)

print('All python files compiled successfully')
