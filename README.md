# nonocycle

*Prevent circular imports before they happen*

Nonocycle analyzes your Python project for circular imports between its sub-packages.

Use nonocycle to:
* Prevent circular imports
* Discover potential circular imports in an existing project
* Enforce separation of concerns between modules
* Help contributors follow and understand the codebase
* Help maintainers review code without worrying about future circular imports


## Installation

```bash
pip install nonocycle
```


## Usage

```bash
nonocycle path/to/my_package
```

Which will output something like:

```
my_package
  Num Potential Cycles: 1
  Cycle 0
    my_package.subpackage_a imports
      my_package.subpackage_b
      my_package.subpackage_b.d
    my_package.subpackage_b imports
      my_package.subpackage_a
      my_package.subpackage_a.b

Oh no! Found 1 potential cycle(s) in 3 module(s).
```

The path must point to the directory of your project with the `__init__.py` file.


## How it works

Circular imports are a common problem in Python projects and are the cause of the
following error message:

```
ImportError: cannot import name 'abc' from partially initialized module 'xyz' (most likely due to a circular import)
```

They happen when two or more modules depend on each other and the Python interpreter
cannot load one before the other. For example:

```bash
src/my_package
├── a.py     # imports from b.py
└── b.py     # imports from a.py
```

Oftentimes, circular imports are not immediately obvious and can span multiple files
and sub-packages:

```bash
src/my_package
├── subpackage_a
│   ├── a.py    # imports from subpackage_b/d.py
│   └── b.py    # imports from subpackage_a/a.py
└── subpackage_b
    ├── c.py    # imports from subpackage_a/b.py
    └── d.py    # imports from subpackage_b/c.py
```

Once a circulare import is detected, the code has to be refactored to break the cycle.
The earlier a potential circular import is detected, the easier it is to fix.
The problem is that potential circular imports can sneak into the codebase without
being noticed. The following code will usually not raise an error:

```bash
src/my_package
├── subpackage_a
│   ├── a.py    # imports from subpackage_b/d.py
│   └── b.py
└── subpackage_b
    ├── c.py    # imports from subpackage_a/b.py
    └── d.py
```

But if an unsuspecting developer now imports `subpackage_b/c.py` in `subpackage_b/d.py`
(note that both modules are in the same sub-package!), a circular import can happen.

Nonocycle prevents this by raising an error if a circular dependency between
sub-packages is detected. In the above example, it detects that `subpackage_a`
depends on `subpackage_b` and vice versa and raises an error. This makes sure that your
sub-packages (and sub-packages of sub-packages etc.) form a directed acyclic graph.

> Note: There are many alternative solutions to fix circular imports, such as
> delaying the import until it is needed, importing a module instead of a function,
> or introducing a new module to break the cycle (nonocycle encourages the latter).
>
> Sometimes circular imports are also unavoidable and that is fine.


## Examples

Examples from popular Python projects that contain circular dependencies between their
sub-packages.

<details>
    <summary>Django</summary>

    ```
    django
      Num Potential Cycles: 44
      Cycle 0
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.utils imports
          django.core.management
          django.core.signals
          django.core.management.color
          django.core.serializers.json
          django.core.cache
          django.core.serializers
          django.core.exceptions
          django.core.mail
      Cycle 1
        django.conf imports
          django.core.exceptions
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 2
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.http imports
          django.core.serializers
          django.core.files
          django.core.signals
          django.core.exceptions
          django.core.signing
          django.core.serializers.json
          django.core.files.uploadhandler
        django.urls imports
          django.http
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 3
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.urls imports
          django.core.checks
          django.core.checks.urls
          django.core.exceptions
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 4
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.core.paginator
          django.core.exceptions
      Cycle 5
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.template imports
          django.core.checks
          django.core.exceptions
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 6
        django.apps imports
          django.core.exceptions
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.template imports
          django.apps
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 7
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.middleware imports
          django.core.exceptions
          django.core.mail
          django.core.cache
        django.template imports
          django.middleware
          django.middleware.csrf
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 8
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.forms imports
          django.core.validators
          django.core.exceptions
        django.template imports
          django.forms
          django.forms.renderers
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 9
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.db imports
          django.core.management
          django.core.files
          django.core.checks.model_checks
          django.core.files.utils
          django.core.management.base
          django.core.files.storage
          django.core.files.images
          django.core.signals
          django.core.validators
          django.core.checks
          django.core.files.base
          django.core.serializers
          django.core.exceptions
        django.forms imports
          django.db.models
          django.db.models.utils
          django.db
        django.template imports
          django.forms
          django.forms.renderers
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 10
        django.conf imports
          django.urls
        django.contrib imports
          django.core.management
          django.core.files
          django.core.signing
          django.core.management.base
          django.core.handlers.asgi
          django.core.management.color
          django.core.checks
          django.core.files.base
          django.core.files.storage
          django.core.management.commands.inspectdb
          django.core.serializers.base
          django.core.serializers
          django.core.handlers.exception
          django.core.signals
          django.core.handlers
          django.core.serializers.json
          django.core.paginator
          django.core.mail
          django.core.handlers.wsgi
          django.core.management.commands
          django.core.validators
          django.core.management.commands.runserver
          django.core.cache
          django.core.exceptions
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 11
        django.conf imports
          django.urls
        django.contrib imports
          django.test.selenium
          django.test
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.test imports
          django.core.management
          django.core.files
          django.core.management.sql
          django.core.handlers.base
          django.core.files.storage
          django.core.handlers.asgi
          django.core.servers
          django.core.signals
          django.core.management.color
          django.core.checks.registry
          django.core.handlers
          django.core.checks
          django.core.serializers.json
          django.core.files.locks
          django.core.cache
          django.core.serializers
          django.core.exceptions
          django.core.mail
          django.core.servers.basehttp
          django.core.handlers.wsgi
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 12
        django.conf imports
          django.urls
        django.core imports
          django.utils.connection
          django.utils.log
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.http
          django.utils.xmlutils
          django.utils.version
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.archive
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.termcolors
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.encoding
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.core.cache.utils
          django.core.cache
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 13
        django.contrib imports
          django.test.selenium
          django.test
        django.test imports
          django.contrib.auth.handlers
          django.contrib.auth.management.commands.changepassword
          django.contrib.auth.forms
          django.contrib.auth.password_validation
          django.contrib.auth.management.commands
          django.contrib.staticfiles
          django.contrib.auth
          django.contrib
          django.contrib.auth.management
          django.contrib.staticfiles.finders
          django.contrib.staticfiles.storage
          django.contrib.auth.views
          django.contrib.auth.backends
          django.contrib.auth.handlers.modwsgi
      Cycle 14
        django.conf imports
          django.urls
        django.middleware imports
          django.utils.log
          django.utils.functional
          django.utils.cache
          django.utils.deprecation
          django.utils.regex_helper
          django.utils.text
          django.utils.crypto
          django.utils.http
          django.utils.translation
        django.template imports
          django.middleware
          django.middleware.csrf
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 15
        django.conf imports
          django.urls
        django.contrib imports
          django.middleware
          django.middleware.csrf
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.middleware imports
          django.utils.log
          django.utils.functional
          django.utils.cache
          django.utils.deprecation
          django.utils.regex_helper
          django.utils.text
          django.utils.crypto
          django.utils.http
          django.utils.translation
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 16
        django.conf imports
          django.urls
        django.middleware imports
          django.utils.log
          django.utils.functional
          django.utils.cache
          django.utils.deprecation
          django.utils.regex_helper
          django.utils.text
          django.utils.crypto
          django.utils.http
          django.utils.translation
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.middleware
          django.middleware.cache
          django.middleware.gzip
          django.middleware.csrf
          django.middleware.http
      Cycle 17
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.conf imports
          django.urls
        django.template imports
          django.apps
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 18
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.conf imports
          django.urls
        django.db imports
          django.apps.registry
          django.apps
        django.forms imports
          django.db.models
          django.db.models.utils
          django.db
        django.template imports
          django.forms
          django.forms.renderers
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 19
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.conf imports
          django.urls
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.apps
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 20
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.conf imports
          django.urls
        django.contrib imports
          django.apps
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.template.Context
          django.template.Engine
          django.template
          django.template.response
          django.template.loader
          django.template.defaultfilters
      Cycle 21
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.conf imports
          django.urls
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.apps
      Cycle 22
        django.apps imports
          django.utils.functional
          django.utils.module_loading
        django.utils imports
          django.apps
      Cycle 23
        django.conf imports
          django.urls
        django.urls imports
          django.views
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.utils.log
          django.utils.functional
          django.utils.formats
          django.utils.http
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.cache
          django.utils.translation
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.decorators
          django.utils.encoding
      Cycle 24
        django.conf imports
          django.views.static
          django.views.i18n
          django.views
          django.views.defaults
        django.utils imports
          django.conf
          django.conf.locale
        django.views imports
          django.utils.log
          django.utils.functional
          django.utils.formats
          django.utils.http
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.cache
          django.utils.translation
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.decorators
          django.utils.encoding
      Cycle 25
        django.contrib imports
          django.views.decorators.cache
          django.views.generic.list
          django.views.i18n
          django.views.generic.edit
          django.views.decorators.common
          django.views.decorators
          django.views.decorators.debug
          django.views.generic.base
          django.views.decorators.csrf
          django.views
          django.views.static
          django.views.generic
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.utils imports
          django.template.base
          django.template
        django.views imports
          django.utils.log
          django.utils.functional
          django.utils.formats
          django.utils.http
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.cache
          django.utils.translation
          django.utils._os
          django.utils.module_loading
          django.utils.translation.trans_real
          django.utils.decorators
          django.utils.encoding
      Cycle 26
        django.db imports
          django.utils.connection
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.choices
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.asyncio
          django.utils.safestring
          django.utils.dateparse
          django.utils.module_loading
          django.utils.tree
          django.utils.encoding
        django.forms imports
          django.db.models
          django.db.models.utils
          django.db
        django.template imports
          django.forms
          django.forms.renderers
        django.utils imports
          django.template.base
          django.template
      Cycle 27
        django.contrib imports
          django.db.models.lookups
          django.db.migrations.operations
          django.db.models.query_utils
          django.db.backends.postgresql.features
          django.db.models.fields
          django.db.models.manager
          django.db.migrations.operations.base
          django.db.backends.mysql.introspection
          django.db.migrations.serializer
          django.db.backends.mysql.features
          django.db.models.fields.related
          django.db.models.deletion
          django.db.models.expressions
          django.db.backends.sqlite3.base
          django.db.backends.postgresql
          django.db.models.utils
          django.db.backends
          django.db
          django.db.backends.oracle.base
          django.db.backends.mysql.base
          django.db.backends.sqlite3.introspection
          django.db.backends.base.base
          django.db.models.sql.where
          django.db.backends.postgresql.operations
          django.db.models.sql
          django.db.backends.oracle
          django.db.backends.base
          django.db.migrations
          django.db.backends.signals
          django.db.models.constants
          django.db.backends.postgresql.schema
          django.db.backends.oracle.features
          django.db.models.query
          django.db.backends.oracle.introspection
          django.db.backends.oracle.schema
          django.db.backends.postgresql.base
          django.db.backends.sqlite3.operations
          django.db.models
          django.db.models.sql.Query
          django.db.backends.postgresql.introspection
          django.db.backends.ddl_references
          django.db.backends.utils
          django.db.backends.sqlite3.schema
          django.db.migrations.writer
          django.db.models.signals
          django.db.backends.oracle.operations
          django.db.models.functions
          django.db.backends.oracle.oracledb_any
          django.db.backends.mysql
          django.db.backends.postgresql.psycopg_any
          django.db.models.indexes
          django.db.backends.sqlite3.features
          django.db.transaction
          django.db.models.constraints
          django.db.models.fields.mixins
          django.db.models.sql.query
          django.db.backends.mysql.schema
          django.db.backends.sqlite3
          django.db.backends.sqlite3.client
          django.db.backends.mysql.operations
          django.db.models.base
        django.db imports
          django.utils.connection
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.choices
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.asyncio
          django.utils.safestring
          django.utils.dateparse
          django.utils.module_loading
          django.utils.tree
          django.utils.encoding
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.utils imports
          django.template.base
          django.template
      Cycle 28
        django.db imports
          django.utils.connection
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.choices
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.asyncio
          django.utils.safestring
          django.utils.dateparse
          django.utils.module_loading
          django.utils.tree
          django.utils.encoding
        django.template imports
          django.db
        django.utils imports
          django.template.base
          django.template
      Cycle 29
        django.db imports
          django.utils.connection
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.inspect
          django.utils.deconstruct
          django.utils.choices
          django.utils.version
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.ipv6
          django.utils.text
          django.utils.crypto
          django.utils.translation
          django.utils.asyncio
          django.utils.safestring
          django.utils.dateparse
          django.utils.module_loading
          django.utils.tree
          django.utils.encoding
        django.utils imports
          django.db.models
          django.db.models.enums
          django.db
      Cycle 30
        django.dispatch imports
          django.utils.inspect
        django.utils imports
          django.dispatch
      Cycle 31
        django.dispatch imports
          django.utils.inspect
        django.template imports
          django.dispatch
        django.utils imports
          django.template.base
          django.template
      Cycle 32
        django.contrib imports
          django.dispatch
        django.dispatch imports
          django.utils.inspect
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.template imports
          django.forms
          django.forms.renderers
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
        django.utils imports
          django.template.base
          django.template
      Cycle 33
        django.forms imports
          django.utils.duration
          django.utils.functional
          django.utils.deprecation
          django.utils.formats
          django.utils.choices
          django.utils.regex_helper
          django.utils.datastructures
          django.utils.timezone
          django.utils.hashable
          django.utils.html
          django.utils.ipv6
          django.utils.text
          django.utils.translation
          django.utils.dates
          django.utils.safestring
          django.utils.dateparse
          django.utils.module_loading
        django.template imports
          django.forms
          django.forms.renderers
        django.utils imports
          django.template.base
          django.template
      Cycle 34
        django.contrib imports
          django.forms
          django.forms.utils
          django.forms.formsets
          django.forms.models
          django.forms.widgets
        django.forms imports
          django.templatetags
          django.templatetags.static
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
      Cycle 35
        django.contrib imports
          django.templatetags
          django.templatetags.static
        django.templatetags imports
          django.contrib.staticfiles
          django.contrib.staticfiles.storage
          django.contrib
      Cycle 36
        django.conf imports
          django.urls
        django.http imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.http
          django.utils.datastructures
          django.utils.timezone
          django.utils.encoding
        django.urls imports
          django.http
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 37
        django.http imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.http
          django.utils.datastructures
          django.utils.timezone
          django.utils.encoding
        django.template imports
          django.http
        django.utils imports
          django.template.base
          django.template
      Cycle 38
        django.http imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.http
          django.utils.datastructures
          django.utils.timezone
          django.utils.encoding
        django.utils imports
          django.http
      Cycle 39
        django.conf imports
          django.urls
        django.urls imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.module_loading
          django.utils.datastructures
          django.utils.deprecation
          django.utils.http
          django.utils.translation
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 40
        django.urls imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.module_loading
          django.utils.datastructures
          django.utils.deprecation
          django.utils.http
          django.utils.translation
        django.utils imports
          django.urls
      Cycle 41
        django.template imports
          django.urls
        django.urls imports
          django.utils.functional
          django.utils.regex_helper
          django.utils.module_loading
          django.utils.datastructures
          django.utils.deprecation
          django.utils.http
          django.utils.translation
        django.utils imports
          django.template.base
          django.template
      Cycle 42
        django.conf imports
          django.utils.functional
          django.utils.deprecation
        django.utils imports
          django.conf
          django.conf.locale
      Cycle 43
        django.template imports
          django.utils.functional
          django.utils.formats
          django.utils.regex_helper
          django.utils.autoreload
          django.utils.timezone
          django.utils.html
          django.utils.text
          django.utils.timesince
          django.utils.dateformat
          django.utils.translation
          django.utils.safestring
          django.utils._os
          django.utils.module_loading
          django.utils.lorem_ipsum
          django.utils.encoding
        django.utils imports
          django.template.base
          django.template
    django.contrib
      Num Potential Cycles: 3
      Cycle 0
        django.contrib.admin imports
          django.contrib.contenttypes
          django.contrib.contenttypes.models
          django.contrib.contenttypes.views
        django.contrib.contenttypes imports
          django.contrib.admin
          django.contrib.admin.checks
          django.contrib.admin.options
      Cycle 1
        django.contrib.admin imports
          django.contrib.contenttypes
          django.contrib.contenttypes.models
          django.contrib.contenttypes.views
        django.contrib.contenttypes imports
          django.contrib.sites
          django.contrib.sites.shortcuts
        django.contrib.sites imports
          django.contrib.admin
      Cycle 2
        django.contrib.admin imports
          django.contrib.auth.decorators
          django.contrib.auth.forms
          django.contrib.auth
          django.contrib.auth.views
        django.contrib.auth imports
          django.contrib.admin.utils
          django.contrib.admin
          django.contrib.admin.options
    django.contrib.admin
      Num Potential Cycles: 11
      Cycle 0
        django.contrib.admin.checks imports
          django.contrib.admin.sites
        django.contrib.admin.models imports
          django.contrib.admin.utils
        django.contrib.admin.options imports
          django.contrib.admin.checks
        django.contrib.admin.sites imports
          django.contrib.admin.models
        django.contrib.admin.templatetags imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.utils imports
          django.contrib.admin.templatetags.admin_list
          django.contrib.admin.templatetags
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 1
        django.contrib.admin.models imports
          django.contrib.admin.utils
        django.contrib.admin.options imports
          django.contrib.admin.models
        django.contrib.admin.templatetags imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.utils imports
          django.contrib.admin.templatetags.admin_list
          django.contrib.admin.templatetags
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 2
        django.contrib.admin.checks imports
          django.contrib.admin.sites
        django.contrib.admin.options imports
          django.contrib.admin.checks
        django.contrib.admin.sites imports
          django.contrib.admin.views.autocomplete
          django.contrib.admin.views
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 3
        django.contrib.admin.actions imports
          django.contrib.admin.decorators
        django.contrib.admin.decorators imports
          django.contrib.admin.sites
        django.contrib.admin.sites imports
          django.contrib.admin.actions
      Cycle 4
        django.contrib.admin.checks imports
          django.contrib.admin.options
        django.contrib.admin.options imports
          django.contrib.admin.checks
      Cycle 5
        django.contrib.admin.options imports
          django.contrib.admin.utils
        django.contrib.admin.templatetags imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.utils imports
          django.contrib.admin.templatetags.admin_list
          django.contrib.admin.templatetags
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 6
        django.contrib.admin.options imports
          django.contrib.admin.templatetags
          django.contrib.admin.templatetags.admin_urls
        django.contrib.admin.templatetags imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 7
        django.contrib.admin.helpers imports
          django.contrib.admin.templatetags
          django.contrib.admin.templatetags.admin_list
        django.contrib.admin.options imports
          django.contrib.admin.helpers
        django.contrib.admin.templatetags imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 8
        django.contrib.admin.options imports
          django.contrib.admin.widgets
        django.contrib.admin.views imports
          django.contrib.admin.options
        django.contrib.admin.widgets imports
          django.contrib.admin.views
          django.contrib.admin.views.main
      Cycle 9
        django.contrib.admin.options imports
          django.contrib.admin.views.main
          django.contrib.admin.views
        django.contrib.admin.views imports
          django.contrib.admin.options
      Cycle 10
        django.contrib.admin.filters imports
          django.contrib.admin.options
        django.contrib.admin.options imports
          django.contrib.admin.filters
    django.contrib.auth
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.auth.decorators imports
          django.contrib.auth.views
        django.contrib.auth.views imports
          django.contrib.auth.decorators
    django.contrib.flatpages
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.flatpages.models imports
          django.contrib.flatpages.views
        django.contrib.flatpages.views imports
          django.contrib.flatpages.models
    django.contrib.gis
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.gis.gdal imports
          django.contrib.gis.geos
        django.contrib.gis.geos imports
          django.contrib.gis.gdal
    django.contrib.gis.db.models
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.gis.db.models.fields imports
          django.contrib.gis.db.models.lookups
        django.contrib.gis.db.models.lookups imports
          django.contrib.gis.db.models.fields
    django.contrib.gis.geos
      Num Potential Cycles: 8
      Cycle 0
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.point
        django.contrib.gis.geos.point imports
          django.contrib.gis.geos.geometry
      Cycle 1
        django.contrib.gis.geos.Point imports
          django.contrib.gis.geos.geometry
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.point
        django.contrib.gis.geos.point imports
          django.contrib.gis.geos.prototypes
        django.contrib.gis.geos.prototypes imports
          django.contrib.gis.geos.Point
      Cycle 2
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.prepared
        django.contrib.gis.geos.prepared imports
          django.contrib.gis.geos.geometry
      Cycle 3
        django.contrib.gis.geos.collections imports
          django.contrib.gis.geos.geometry
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.collections
      Cycle 4
        django.contrib.gis.geos.collections imports
          django.contrib.gis.geos.linestring
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.collections
        django.contrib.gis.geos.linestring imports
          django.contrib.gis.geos.geometry
      Cycle 5
        django.contrib.gis.geos.collections imports
          django.contrib.gis.geos.polygon
        django.contrib.gis.geos.geometry imports
          django.contrib.gis.geos.collections
        django.contrib.gis.geos.polygon imports
          django.contrib.gis.geos.geometry
      Cycle 6
        django.contrib.gis.geos.Point imports
          django.contrib.gis.geos.prototypes
        django.contrib.gis.geos.prototypes imports
          django.contrib.gis.geos.Point
      Cycle 7
        django.contrib.gis.geos.libgeos imports
          django.contrib.gis.geos.prototypes.threadsafe
          django.contrib.gis.geos.prototypes
        django.contrib.gis.geos.prototypes imports
          django.contrib.gis.geos.libgeos
    django.contrib.postgres
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.postgres.expressions imports
          django.contrib.postgres.fields
        django.contrib.postgres.fields imports
          django.contrib.postgres.lookups
        django.contrib.postgres.lookups imports
          django.contrib.postgres.expressions
    django.contrib.sessions
      Num Potential Cycles: 1
      Cycle 0
        django.contrib.sessions.backends imports
          django.contrib.sessions.models
        django.contrib.sessions.models imports
          django.contrib.sessions.backends
          django.contrib.sessions.backends.db
    django.db
      Num Potential Cycles: 2
      Cycle 0
        django.db.backends imports
          django.db.models.sql.where
          django.db.models
          django.db.models.sql
          django.db.models.sql.Query
          django.db.models.constants
          django.db.models.expressions
          django.db.models.sql.compiler
          django.db.models.functions
        django.db.models imports
          django.db.utils
        django.db.utils imports
          django.db.backends
      Cycle 1
        django.db.backends imports
          django.db.models.sql.where
          django.db.models
          django.db.models.sql
          django.db.models.sql.Query
          django.db.models.constants
          django.db.models.expressions
          django.db.models.sql.compiler
          django.db.models.functions
        django.db.models imports
          django.db.backends.oracle
          django.db.backends.base
          django.db.backends.utils
          django.db.backends.base.operations
          django.db.backends.oracle.functions
          django.db.backends
    django.db.backends.oracle
      Num Potential Cycles: 3
      Cycle 0
        django.db.backends.oracle.base imports
          django.db.backends.oracle.client
        django.db.backends.oracle.client imports
          django.db.backends.oracle.utils
        django.db.backends.oracle.utils imports
          django.db.backends.oracle.base
      Cycle 1
        django.db.backends.oracle.base imports
          django.db.backends.oracle.utils
        django.db.backends.oracle.utils imports
          django.db.backends.oracle.base
      Cycle 2
        django.db.backends.oracle.base imports
          django.db.backends.oracle.operations
        django.db.backends.oracle.operations imports
          django.db.backends.oracle.base
    django.db.backends.sqlite3
      Num Potential Cycles: 2
      Cycle 0
        django.db.backends.sqlite3.base imports
          django.db.backends.sqlite3.features
        django.db.backends.sqlite3.features imports
          django.db.backends.sqlite3.base
      Cycle 1
        django.db.backends.sqlite3.base imports
          django.db.backends.sqlite3.operations
        django.db.backends.sqlite3.operations imports
          django.db.backends.sqlite3.base
    django.db.migrations
      Num Potential Cycles: 1
      Cycle 0
        django.db.migrations.serializer imports
          django.db.migrations.writer
        django.db.migrations.writer imports
          django.db.migrations.serializer
    django.db.models
      Num Potential Cycles: 22
      Cycle 0
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.sql imports
          django.db.models.query
          django.db.models.query_utils
      Cycle 1
        django.db.models.Manager imports
          django.db.models.query
        django.db.models.fields imports
          django.db.models.signals
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.options imports
          django.db.models.Manager
        django.db.models.query imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.signals imports
          django.db.models.options
        django.db.models.sql imports
          django.db.models.fields
      Cycle 2
        django.db.models.base imports
          django.db.models.query
        django.db.models.fields imports
          django.db.models.base
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.sql imports
          django.db.models.fields
      Cycle 3
        django.db.models.base imports
          django.db.models.manager
        django.db.models.fields imports
          django.db.models.base
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.manager imports
          django.db.models.query
        django.db.models.query imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.sql imports
          django.db.models.fields
      Cycle 4
        django.db.models.fields imports
          django.db.models.query_utils
          django.db.models.query
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.sql imports
          django.db.models.fields
      Cycle 5
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.sql imports
          django.db.models.lookups
      Cycle 6
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query_utils imports
          django.db.models.lookups
        django.db.models.sql imports
          django.db.models.query_utils
      Cycle 7
        django.db.models.fields imports
          django.db.models.lookups
        django.db.models.functions imports
          django.db.models.fields.json
          django.db.models.fields
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query_utils imports
          django.db.models.functions
        django.db.models.sql imports
          django.db.models.query_utils
      Cycle 8
        django.db.models.functions imports
          django.db.models.lookups
        django.db.models.lookups imports
          django.db.models.sql.query
          django.db.models.sql
        django.db.models.query_utils imports
          django.db.models.functions
        django.db.models.sql imports
          django.db.models.query_utils
      Cycle 9
        django.db.models.aggregates imports
          django.db.models.functions.mixins
          django.db.models.functions.comparison
          django.db.models.functions
        django.db.models.fields imports
          django.db.models.query_utils
        django.db.models.functions imports
          django.db.models.fields.json
          django.db.models.fields
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.aggregates
      Cycle 10
        django.db.models.fields imports
          django.db.models.signals
        django.db.models.options imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.signals imports
          django.db.models.options
        django.db.models.sql imports
          django.db.models.fields
      Cycle 11
        django.db.models.deletion imports
          django.db.models.signals
        django.db.models.fields imports
          django.db.models.deletion
        django.db.models.options imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.signals imports
          django.db.models.options
        django.db.models.sql imports
          django.db.models.fields
      Cycle 12
        django.db.models.base imports
          django.db.models.signals
        django.db.models.fields imports
          django.db.models.base
        django.db.models.options imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.signals imports
          django.db.models.options
        django.db.models.sql imports
          django.db.models.fields
      Cycle 13
        django.db.models.base imports
          django.db.models.options
        django.db.models.fields imports
          django.db.models.base
        django.db.models.options imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.fields
      Cycle 14
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.query_utils
      Cycle 15
        django.db.models.fields imports
          django.db.models.query_utils
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.fields
      Cycle 16
        django.db.models.expressions imports
          django.db.models.query_utils
        django.db.models.fields imports
          django.db.models.expressions
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.fields
      Cycle 17
        django.db.models.deletion imports
          django.db.models.query_utils
        django.db.models.fields imports
          django.db.models.deletion
        django.db.models.query_utils imports
          django.db.models.sql.constants
          django.db.models.sql.query
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.fields
      Cycle 18
        django.db.models.expressions imports
          django.db.models.fields
        django.db.models.fields imports
          django.db.models.expressions
      Cycle 19
        django.db.models.fields imports
          django.db.models.functions
        django.db.models.functions imports
          django.db.models.fields.json
          django.db.models.fields
      Cycle 20
        django.db.models.fields imports
          django.db.models.sql.where
          django.db.models.sql
          django.db.models.sql.Query
        django.db.models.sql imports
          django.db.models.fields
      Cycle 21
        django.db.models.base imports
          django.db.models.fields
          django.db.models.fields.related
        django.db.models.fields imports
          django.db.models.base
    django.db.models.sql
      Num Potential Cycles: 1
      Cycle 0
        django.db.models.sql.query imports
          django.db.models.sql.subqueries
        django.db.models.sql.subqueries imports
          django.db.models.sql.query
    django.template
      Num Potential Cycles: 4
      Cycle 0
        django.template.base imports
          django.template.engine
        django.template.engine imports
          django.template.library
        django.template.library imports
          django.template.base
      Cycle 1
        django.template.backends imports
          django.template.library
        django.template.base imports
          django.template.engine
        django.template.engine imports
          django.template.backends.django
          django.template.backends
        django.template.library imports
          django.template.base
      Cycle 2
        django.template.base imports
          django.template.engine
        django.template.engine imports
          django.template.base
      Cycle 3
        django.template.backends imports
          django.template.engine
        django.template.engine imports
          django.template.backends.django
          django.template.backends
    django.urls
      Num Potential Cycles: 1
      Cycle 0
        django.urls.converters imports
          django.urls.resolvers
        django.urls.resolvers imports
          django.urls.converters
    django.utils
      Num Potential Cycles: 1
      Cycle 0
        django.utils.html imports
          django.utils.text
        django.utils.text imports
          django.utils.html
    
    Oh no! Found 109 potential cycle(s) in 187 module(s).

    ```
</details>

<details>
    <summary>Flask</summary>

    ```
    flask
      Num Potential Cycles: 23
      Cycle 0
        flask.app imports
          flask.helpers
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.wrappers
        flask.json imports
          flask.globals
        flask.wrappers imports
          flask.json
      Cycle 1
        flask.app imports
          flask.ctx
        flask.ctx imports
          flask.sessions
        flask.globals imports
          flask.app
        flask.json imports
          flask.globals
        flask.sessions imports
          flask.json.tag
          flask.json
      Cycle 2
        flask.app imports
          flask.helpers
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.globals
      Cycle 3
        flask.app imports
          flask.ctx
        flask.ctx imports
          flask.sessions
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.globals
        flask.sessions imports
          flask.wrappers
        flask.wrappers imports
          flask.helpers
      Cycle 4
        flask.app imports
          flask.ctx
        flask.blueprints imports
          flask.helpers
        flask.ctx imports
          flask.sessions
        flask.debughelpers imports
          flask.blueprints
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.globals
        flask.sessions imports
          flask.wrappers
        flask.wrappers imports
          flask.debughelpers
      Cycle 5
        flask.app imports
          flask.ctx
        flask.blueprints imports
          flask.cli
        flask.cli imports
          flask.helpers
        flask.ctx imports
          flask.sessions
        flask.debughelpers imports
          flask.blueprints
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.globals
        flask.sessions imports
          flask.wrappers
        flask.wrappers imports
          flask.debughelpers
      Cycle 6
        flask.app imports
          flask.templating
        flask.globals imports
          flask.app
        flask.helpers imports
          flask.globals
        flask.templating imports
          flask.helpers
      Cycle 7
        flask.app imports
          flask.ctx
        flask.ctx imports
          flask.globals
        flask.globals imports
          flask.app
      Cycle 8
        flask.ctx imports
          flask.globals
        flask.globals imports
          flask.ctx
      Cycle 9
        flask.app imports
          flask.wrappers
        flask.blueprints imports
          flask.globals
        flask.debughelpers imports
          flask.blueprints
        flask.globals imports
          flask.app
        flask.wrappers imports
          flask.debughelpers
      Cycle 10
        flask.app imports
          flask.wrappers
        flask.globals imports
          flask.app
        flask.wrappers imports
          flask.globals
      Cycle 11
        flask.app imports
          flask.testing
        flask.globals imports
          flask.app
        flask.sessions imports
          flask.wrappers
        flask.testing imports
          flask.sessions
        flask.wrappers imports
          flask.globals
      Cycle 12
        flask.app imports
          flask.debughelpers
        flask.debughelpers imports
          flask.wrappers
        flask.globals imports
          flask.app
        flask.wrappers imports
          flask.globals
      Cycle 13
        flask.globals imports
          flask.wrappers
        flask.wrappers imports
          flask.globals
      Cycle 14
        flask.app imports
          flask.cli
        flask.cli imports
          flask.globals
        flask.globals imports
          flask.app
      Cycle 15
        flask.app imports
          flask.testing
        flask.cli imports
          flask.globals
        flask.globals imports
          flask.app
        flask.testing imports
          flask.cli
      Cycle 16
        flask.app imports
          flask.debughelpers
        flask.debughelpers imports
          flask.globals
        flask.globals imports
          flask.app
      Cycle 17
        flask.app imports
          flask.templating
        flask.debughelpers imports
          flask.globals
        flask.globals imports
          flask.app
        flask.templating imports
          flask.debughelpers
      Cycle 18
        flask.app imports
          flask.testing
        flask.testing imports
          flask.app
      Cycle 19
        flask.app imports
          flask.templating
        flask.globals imports
          flask.app
        flask.templating imports
          flask.globals
      Cycle 20
        flask.app imports
          flask.globals
        flask.globals imports
          flask.app
      Cycle 21
        flask.app imports
          flask.templating
        flask.templating imports
          flask.app
      Cycle 22
        flask.app imports
          flask.sessions
        flask.sessions imports
          flask.app
    
    Oh no! Found 23 potential cycle(s) in 2 module(s).
    ```
</details>

<details>
    <summary>Pydantic</summary>

    ```
    pydantic
      Num Potential Cycles: 30
      Cycle 0
        pydantic._internal imports
          pydantic.config
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
      Cycle 1
        pydantic._internal imports
          pydantic.fields
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
        pydantic.fields imports
          pydantic.config
      Cycle 2
        pydantic._internal imports
          pydantic.fields
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
        pydantic.deprecated imports
          pydantic.type_adapter
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.type_adapter imports
          pydantic.config
        pydantic.types imports
          pydantic.json_schema
      Cycle 3
        pydantic._internal imports
          pydantic.fields
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.config
        pydantic.types imports
          pydantic.json_schema
      Cycle 4
        pydantic._internal imports
          pydantic.fields
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.config
        pydantic.types imports
          pydantic.json_schema
      Cycle 5
        pydantic._internal imports
          pydantic.dataclasses
        pydantic.config imports
          pydantic._internal
          pydantic._internal._utils
        pydantic.dataclasses imports
          pydantic.config
      Cycle 6
        pydantic._internal imports
          pydantic.fields
        pydantic.color imports
          pydantic._internal
          pydantic._internal._schema_generation_shared
          pydantic._internal._repr
        pydantic.deprecated imports
          pydantic.color
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.types imports
          pydantic.json_schema
      Cycle 7
        pydantic._internal imports
          pydantic.v1
        pydantic.color imports
          pydantic._internal
          pydantic._internal._schema_generation_shared
          pydantic._internal._repr
        pydantic.v1 imports
          pydantic.color
      Cycle 8
        pydantic._internal imports
          pydantic.dataclasses
        pydantic.dataclasses imports
          pydantic._internal
          pydantic._internal._config
          pydantic._internal._decorators
          pydantic._internal._dataclasses
          pydantic._internal._utils
          pydantic._internal._typing_extra
      Cycle 9
        pydantic._internal imports
          pydantic.aliases
        pydantic.aliases imports
          pydantic._internal._internal_dataclass
          pydantic._internal
      Cycle 10
        pydantic._internal imports
          pydantic.errors
        pydantic._migration imports
          pydantic._internal
          pydantic._internal._validators
        pydantic.errors imports
          pydantic._migration
      Cycle 11
        pydantic._internal imports
          pydantic.errors
        pydantic._migration imports
          pydantic.version
        pydantic.errors imports
          pydantic._migration
        pydantic.version imports
          pydantic._internal
          pydantic._internal._git
      Cycle 12
        pydantic._internal imports
          pydantic.fields
        pydantic.fields imports
          pydantic._internal._internal_dataclass
          pydantic._internal
          pydantic._internal._generics
          pydantic._internal._decorators
          pydantic._internal._fields
          pydantic._internal._utils
          pydantic._internal._repr
          pydantic._internal._typing_extra
      Cycle 13
        pydantic._internal imports
          pydantic.fields
        pydantic.fields imports
          pydantic.types
        pydantic.types imports
          pydantic._internal._internal_dataclass
          pydantic._internal
          pydantic._internal._validators
          pydantic._internal._fields
          pydantic._internal._utils
          pydantic._internal._typing_extra
          pydantic._internal._core_utils
      Cycle 14
        pydantic._internal imports
          pydantic.fields
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic._internal._internal_dataclass
          pydantic._internal
          pydantic._internal._config
          pydantic._internal._decorators
          pydantic._internal._schema_generation_shared
          pydantic._internal._core_metadata
          pydantic._internal._dataclasses
          pydantic._internal._mock_val_ser
          pydantic._internal._typing_extra
          pydantic._internal._core_utils
        pydantic.types imports
          pydantic.json_schema
      Cycle 15
        pydantic._internal imports
          pydantic.fields
        pydantic.deprecated imports
          pydantic._internal
          pydantic._internal._config
          pydantic._internal._import_utils
          pydantic._internal._decorators
          pydantic._internal._decorators_v1
          pydantic._internal._utils
          pydantic._internal._model_construction
          pydantic._internal._typing_extra
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.types imports
          pydantic.json_schema
      Cycle 16
        pydantic._internal imports
          pydantic.fields
        pydantic.deprecated imports
          pydantic.type_adapter
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.type_adapter imports
          pydantic._internal
          pydantic._internal._config
          pydantic._internal._generate_schema
          pydantic._internal._utils
          pydantic._internal._mock_val_ser
          pydantic._internal._typing_extra
        pydantic.types imports
          pydantic.json_schema
      Cycle 17
        pydantic._internal imports
          pydantic.fields
        pydantic.deprecated imports
          pydantic.networks
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.networks imports
          pydantic._internal
          pydantic._internal._schema_generation_shared
          pydantic._internal._fields
          pydantic._internal._repr
        pydantic.types imports
          pydantic.json_schema
      Cycle 18
        pydantic._internal imports
          pydantic.fields
        pydantic.deprecated imports
          pydantic.functional_validators
        pydantic.fields imports
          pydantic.types
        pydantic.functional_validators imports
          pydantic._internal._internal_dataclass
          pydantic._internal
          pydantic._internal._generics
          pydantic._internal._decorators
          pydantic._internal._core_metadata
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.types imports
          pydantic.json_schema
      Cycle 19
        pydantic._internal imports
          pydantic.fields
        pydantic.fields imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic._internal._decorators
          pydantic._internal._utils
          pydantic._internal
          pydantic._internal._fields
          pydantic._internal._repr
          pydantic._internal._typing_extra
          pydantic._internal._model_construction
          pydantic._internal._generics
          pydantic._internal._config
          pydantic._internal._import_utils
          pydantic._internal._forward_ref
          pydantic._internal._mock_val_ser
        pydantic.types imports
          pydantic.json_schema
      Cycle 20
        pydantic._internal imports
          pydantic.root_model
        pydantic.root_model imports
          pydantic._internal
          pydantic._internal._model_construction
          pydantic._internal._repr
      Cycle 21
        pydantic.deprecated imports
          pydantic.json_schema
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
      Cycle 22
        pydantic.deprecated imports
          pydantic.type_adapter
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.type_adapter imports
          pydantic.json_schema
      Cycle 23
        pydantic.deprecated imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.types imports
          pydantic.json_schema
      Cycle 24
        pydantic.annotated_handlers imports
          pydantic.json_schema
        pydantic.deprecated imports
          pydantic.types
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.types imports
          pydantic.annotated_handlers
      Cycle 25
        pydantic.deprecated imports
          pydantic.networks
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.networks imports
          pydantic.json_schema
      Cycle 26
        pydantic.json_schema imports
          pydantic.main
        pydantic.main imports
          pydantic.json_schema
      Cycle 27
        pydantic.deprecated imports
          pydantic.type_adapter
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
        pydantic.type_adapter imports
          pydantic.main
      Cycle 28
        pydantic.deprecated imports
          pydantic.main
        pydantic.main imports
          pydantic.deprecated.parse
          pydantic.deprecated.json
          pydantic.deprecated
          pydantic.deprecated.copy_internals
      Cycle 29
        pydantic._migration imports
          pydantic.errors
        pydantic.errors imports
          pydantic._migration
    pydantic._internal
      Num Potential Cycles: 10
      Cycle 0
        pydantic._internal._core_utils imports
          pydantic._internal._typing_extra
        pydantic._internal._dataclasses imports
          pydantic._internal._generate_schema
        pydantic._internal._discriminated_union imports
          pydantic._internal._core_utils
        pydantic._internal._generate_schema imports
          pydantic._internal._discriminated_union
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
      Cycle 1
        pydantic._internal._core_utils imports
          pydantic._internal._typing_extra
        pydantic._internal._dataclasses imports
          pydantic._internal._schema_generation_shared
        pydantic._internal._discriminated_union imports
          pydantic._internal._core_utils
        pydantic._internal._generate_schema imports
          pydantic._internal._discriminated_union
        pydantic._internal._schema_generation_shared imports
          pydantic._internal._generate_schema
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
      Cycle 2
        pydantic._internal._generate_schema imports
          pydantic._internal._std_types_schema
        pydantic._internal._std_types_schema imports
          pydantic._internal._generate_schema
      Cycle 3
        pydantic._internal._dataclasses imports
          pydantic._internal._decorators
        pydantic._internal._decorators imports
          pydantic._internal._typing_extra
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
      Cycle 4
        pydantic._internal._dataclasses imports
          pydantic._internal._fields
        pydantic._internal._decorators imports
          pydantic._internal._typing_extra
        pydantic._internal._fields imports
          pydantic._internal._decorators
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
      Cycle 5
        pydantic._internal._core_utils imports
          pydantic._internal._typing_extra
        pydantic._internal._dataclasses imports
          pydantic._internal._schema_generation_shared
        pydantic._internal._schema_generation_shared imports
          pydantic._internal._core_utils
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
      Cycle 6
        pydantic._internal._dataclasses imports
          pydantic._internal._signature
        pydantic._internal._repr imports
          pydantic._internal._typing_extra
        pydantic._internal._signature imports
          pydantic._internal._utils
        pydantic._internal._typing_extra imports
          pydantic._internal._dataclasses
        pydantic._internal._utils imports
          pydantic._internal._repr
      Cycle 7
        pydantic._internal._dataclasses imports
          pydantic._internal._fields
        pydantic._internal._fields imports
          pydantic._internal._dataclasses
      Cycle 8
        pydantic._internal._repr imports
          pydantic._internal._typing_extra
        pydantic._internal._typing_extra imports
          pydantic._internal._utils
        pydantic._internal._utils imports
          pydantic._internal._repr
      Cycle 9
        pydantic._internal._typing_extra imports
          pydantic._internal._utils
        pydantic._internal._utils imports
          pydantic._internal._typing_extra
    pydantic.v1
      Num Potential Cycles: 45
      Cycle 0
        pydantic.v1.class_validators imports
          pydantic.v1.fields
        pydantic.v1.fields imports
          pydantic.v1.class_validators
      Cycle 1
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.fields
        pydantic.v1.fields imports
          pydantic.v1.class_validators
      Cycle 2
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.utils imports
          pydantic.v1.fields
      Cycle 3
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.typing imports
          pydantic.v1.fields
        pydantic.v1.utils imports
          pydantic.v1.typing
      Cycle 4
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.fields
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 5
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.fields
      Cycle 6
        pydantic.v1.annotated_types imports
          pydantic.v1.fields
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 7
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.main imports
          pydantic.v1.fields
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 8
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.json
        pydantic.v1.networks imports
          pydantic.v1.fields
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 9
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.fields imports
          pydantic.v1.class_validators
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.schema imports
          pydantic.v1.fields
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 10
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.config
      Cycle 11
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.config
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 12
        pydantic.v1.class_validators imports
          pydantic.v1.config
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 13
        pydantic.v1.class_validators imports
          pydantic.v1.types
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.config
      Cycle 14
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.types
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.main imports
          pydantic.v1.config
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 15
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.types
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.json
        pydantic.v1.networks imports
          pydantic.v1.config
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 16
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.types
        pydantic.v1.config imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.error_wrappers imports
          pydantic.v1.config
        pydantic.v1.main imports
          pydantic.v1.error_wrappers
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 17
        pydantic.v1.class_validators imports
          pydantic.v1.typing
        pydantic.v1.dataclasses imports
          pydantic.v1.class_validators
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 18
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.class_validators imports
          pydantic.v1.typing
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.main imports
          pydantic.v1.class_validators
        pydantic.v1.types imports
          pydantic.v1.validators
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 19
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.types
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 20
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.types
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 21
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.types
      Cycle 22
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.types
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 23
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.parse
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.parse imports
          pydantic.v1.types
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 24
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.schema imports
          pydantic.v1.types
        pydantic.v1.types imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 25
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.typing
      Cycle 26
        pydantic.v1.errors imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.errors
      Cycle 27
        pydantic.v1.dataclasses imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 28
        pydantic.v1.color imports
          pydantic.v1.typing
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.color
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 29
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.networks imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 30
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.typing
      Cycle 31
        pydantic.v1.annotated_types imports
          pydantic.v1.typing
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 32
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.typing
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 33
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.networks
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.schema imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 34
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.typing
        pydantic.v1.typing imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 35
        pydantic.v1.color imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.json
        pydantic.v1.json imports
          pydantic.v1.color
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 36
        pydantic.v1.color imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.main
        pydantic.v1.json imports
          pydantic.v1.color
        pydantic.v1.main imports
          pydantic.v1.json
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 37
        pydantic.v1.color imports
          pydantic.v1.utils
        pydantic.v1.dataclasses imports
          pydantic.v1.main
        pydantic.v1.json imports
          pydantic.v1.color
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.schema imports
          pydantic.v1.json
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 38
        pydantic.v1.annotated_types imports
          pydantic.v1.main
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.schema imports
          pydantic.v1.networks
        pydantic.v1.validators imports
          pydantic.v1.annotated_types
      Cycle 39
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.utils
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.networks imports
          pydantic.v1.validators
        pydantic.v1.schema imports
          pydantic.v1.networks
        pydantic.v1.utils imports
          pydantic.v1.main
        pydantic.v1.validators imports
          pydantic.v1.dataclasses
      Cycle 40
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.dataclasses
      Cycle 41
        pydantic.v1.dataclasses imports
          pydantic.v1.error_wrappers
        pydantic.v1.error_wrappers imports
          pydantic.v1.utils
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.schema imports
          pydantic.v1.dataclasses
        pydantic.v1.utils imports
          pydantic.v1.main
      Cycle 42
        pydantic.v1.main imports
          pydantic.v1.schema
        pydantic.v1.schema imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.main
      Cycle 43
        pydantic.v1.error_wrappers imports
          pydantic.v1.utils
        pydantic.v1.main imports
          pydantic.v1.error_wrappers
        pydantic.v1.utils imports
          pydantic.v1.main
      Cycle 44
        pydantic.v1.main imports
          pydantic.v1.utils
        pydantic.v1.utils imports
          pydantic.v1.main
    
    Oh no! Found 85 potential cycle(s) in 6 module(s).
    ```
</details>


## Credits

This package relies on
- [pydeps](https://github.com/thebjorn/pydeps) to generate the import graphs
- [NetworkX](https://github.com/networkx/networkx) to analyze the graphs
