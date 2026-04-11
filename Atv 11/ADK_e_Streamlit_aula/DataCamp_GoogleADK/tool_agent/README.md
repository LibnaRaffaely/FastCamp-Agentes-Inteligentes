# Tools

Let's begin by defining a Tool.

A Tool is a **modular** component that extends an AI agent’s capabilities beyond just simple text generation.

Tools enable agents to perform **specific** actions, interact with external systems, and process real-world data dynamically.

**Examples**:

- ☀️ Checking the weather
- 🌐 Searching the web
- ➗ Doing math calculations
- ✈️ Booking a flight

## Characteristics of Tools:

1. **Action-Oriented:** Tools execute predefined tasks such as retrieving data (such as weather reports, stock prices).
2. **Extends Agent Functionality:** Agents leverage tools to overcome limitations of static training data by accessing live information.
3. **Deterministic Execution:** Tools follow strict logic defined by developers, unlike the agent’s LLM, which handles reasoning.

## Benefits of Tools:

You might have a question now.... what are the benefits of Tools?

-⏳**Real-Time Data Access**: Agents fetch live information (e.g., weather, financial data).

-🤖**Task Automation**: Execute backend processes (e.g., database updates, API calls).

-📈**Scalability**: Modular tools allow reusable, maintainable agent enhancements.

## Types of Tools:

For more details and examples, see the [official ADK Tools documentation](https://google.github.io/adk-docs/tools/).

1. **Function Tools:** These are custom tools defined by us developers.
2. **Built-In Tools:** These are _predefined_ tools for common tasks (such as web search, code execution). This means these are plug and play tools (can be imported with ease).
3. **Third-Party Tools:** Integrations with external services (such as Slack).
