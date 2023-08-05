=====
Django Easy Paginator for API Response
=====

django-easy-paginate is a simple Django app to conduct pagination for api responses. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "paginate_api" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'paginate_api',
    ]

2. Import paginate from paginate_api.paginate

3. Use paginate as 
            
            result = paginate(data_as_array, page_number, per_page_count_integer_value)
