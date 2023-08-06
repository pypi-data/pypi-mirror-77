# PyDyImport
Dynamically import python file to aviod mess when you are using a different directory structure from python suggested.

## Usage
Just construct a `DynamicImport` instance and call `DynamicImport.require` 
````python
from pydyimport import DynamicImport
require = DynamicImport(__file__).require

mod = require("path/to/file.py")
````

If you only need some of fields in the module, use `DynamicImport.require_only`, which *always* return a tuple.
````python
from pydyimport import DynamicImport
require_only = DynamicImport(__file__).require_only

foo, = require_only("path/to/file.py", 'foo') # still return tuple even if only one field described
Spam1, Spam2 = require_only("path/to/file.py", 'Spam1', 'Spam2')
````

You can inject environment variables to the modules you will import by the use of `env_injector` option of `DynamicImport`.
````python
from pydyimport import DynamicImport

def meaningless_env_injector(path: str, code: bytes):
    return {
        '__meaning__': 'no',
    }

importer = DynamicImport(__file__, env_injector=meaningless_env_injector)
importer.require("path/to/file.py")
````

You can inject require* functions by `RequireEnvInjector`,
````python
from pydyimport import DynamicImport
from pydyimport.injector import RequireEnvInjector
require = DynamicImport(__file__, env_injector=RequireEnvInjector(next_injector=None))

require('path/to/module.py')
````
or just set `inject_require` `True`.
````python
from pydyimport import DynamicImport
require = DynamicImport(__file__, inject_require=True)

require('path/to/module.py')
````
If your source contains `# inject_require`, the require* functions will automatically inject require* functions to the module.
````python
#!/usr/bin/env python
# inject_require

require('path/to/module.py')
Spam1, foo = require_only('path/to/module2.py', 'Spam1', 'foo')
````


## License
GNU GENERAL PUBLIC LICENSE, version 3 or later.
````
    PyDyImport - dynamically importing and avoid mess in python
    Copyright (C) 2020 thisLight

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
````
