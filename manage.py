#!/use/bin/env python
import os
COV = None
if os.environ.get('FLASKY_CONVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

