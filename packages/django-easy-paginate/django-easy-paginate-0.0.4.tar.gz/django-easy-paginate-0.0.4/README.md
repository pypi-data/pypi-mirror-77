Django Easy Paginator for API Response
=====

django-easy-paginate is a simple Django app to conduct pagination for api responses. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "api_paginator" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'api_paginator',
    ]

2. Import paginate from api_paginator.api_paginator in views.py as::

		from api_paginator.api_paginator import paginate

3. Use paginate as ::
            
            result = paginate(data_as_array, page_number, per_page_count_integer_value)
