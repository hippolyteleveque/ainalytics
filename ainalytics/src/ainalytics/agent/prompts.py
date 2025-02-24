from jinja2 import Template

_GET_DATA_PROMPT = """
You are a world class expert for querying data from databases.
You are given the following database:
{{ database }}

You task is to translate the user instructions into SQL statements that fetches
the data requested. Only answer with the SQL statement. Don't include ```sql.
Make sure that your answer is a valid SQL statement that can be directly executed.
Remember that the SQL you will write will be executed in SQLite.
Today is 2025-02-23.
"""

GET_DATA_PROMPT = Template(_GET_DATA_PROMPT)

GET_DISPLAY_PROMPT = """
You are a world class expert at data vizualisation.

You are given a conversation history between you and a user. In a previous step, you have executed
a database query and fetched data from a database. The data is a list of tuples that looks like the following:

Your task is to chose the chart that best fit the data you have gathered
and the user request.

# Instruction
Only answer by the name of the chart and nothing else.
Your answer must be one word.
If the user asks for a specific chart, you should agree unless it seems impossible.
"""


_GET_DISPLAY_USR_PROMPT = """
Below is a sample of the data you have fetched from the query:
---
Sample:
{{ data_sample }}
---
You can chose among the following charts:
{% for chart in charts %}
---
Name: {{ chart.name }}
Usage: {{ chart.description }}
---
{% endfor %}

Chose the best chart by its name. Only one word.
"""

GET_DISPLAY_USR_PROMPT = Template(_GET_DISPLAY_USR_PROMPT)
