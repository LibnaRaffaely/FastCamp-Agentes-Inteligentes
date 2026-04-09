# Structured Outputs

Normally, a language model replies with text like:

```
"John's number is 12345."
```

But sometimes we want clean, structured data like this:

```python
{  "name": "John",
"contact": "12345"}
```

There are many reasons for this such as making it easier to:

1. Use in code and make it more readable
2. Save in a database
3. Pass between agents

Google ADK lets you force the agent to reply in this clean format using `output_schema`.

There are 2 formats we would want to control - **Input and Output Schema.**

1. Input Schema: What the user must send
2. Output Schema: What the agent/model must return

We define these using Pydantic models.

```python
from pydantic import BaseModel, Field

# Input format (what we send)
class PersonInput(BaseModel):
    person: str = Field(description="The name of the person.")

# Output format (what agent must return)
class ContactOutput(BaseModel):
    contact: str = Field(description="The contact of the person.")
```

**Note:** If we use Output Schema, we cannot use Tools! It must generate the answer by itself, using the LLM’s internal knowledge.
