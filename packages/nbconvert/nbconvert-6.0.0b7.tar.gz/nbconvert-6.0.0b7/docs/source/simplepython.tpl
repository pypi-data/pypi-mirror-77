
{% extends 'python/index.py.j2'%}

## remove markdown cells
{% block markdowncell %}
{% endblock markdowncell %}

## change the appearance of execution count
{% block in_prompt %}
# [{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endblock in_prompt %}
