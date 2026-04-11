# Persistent Agents

💾 **What they are**: Agents that remember our data and progress, even after you close and reopen the app

🔗 **How they work**: All our habits and state are saved in a local SQLite database using Google ADK's DatabaseSessionService

🎯 **Why use them**: For Memory persistence, even if we close our application we will have access to it

## Process

🌱 For this section, we will be building a Habit Tracking Agent!

- When you start the app, it checks if you already have a session. If yes, it loads our habits; if not, it creates a new session for you.
- You can **add new habits**, **view our current habits**, or **delete habits** you no longer want to track.
- All our changes are **saved to a local database**—so our data is safe and persistent.
- The agent always greets you by name and confirms any action it takes, making the experience personal and interactive.

## Goal 🎯

We should be able to do this:

- **Add a habit:** "run 5k every day"
- **View our habits:** See our full list, even after restarting the app
- **Delete a habit:** Remove any habit you no longer want to track

## 🛠️ What is Tool Context?

- **Tool context** is a special object passed to each tool (function) our agent uses.
- It gives our tool direct access to the current session state—so you can read and update habits, user info, and more.
- When you update `tool_context.state`, those changes are automatically saved to the database by ADK. No extra code needed!
- This makes our tools both powerful and simple: just change the state, and persistence is handled for you.

**In short:** Tool context is how our agent's tools "see" and "remember" everything about the user.

---

**TLDR:** Think of persistent agents as our personal memory-keepers. They make sure our progress and preferences are always remembered!
