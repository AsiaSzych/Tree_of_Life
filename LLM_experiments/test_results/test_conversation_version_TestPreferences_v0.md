# Tests of prompts for Conversational Code Generation - version TestPreferences
## Prompt number 1

**User:** I'm planning of using chatbot based on LLM to help me on a coding project. Please provide me a guide, how to create a perfect prompt. What should I always remember to provide?


**LLM Response:**

Of course! Using an LLM as a coding partner can be incredibly powerful, but its usefulness is directly proportional to the quality of your prompts. A well-crafted prompt can save you hours, while a poor one will lead to frustration and incorrect code.

Here is a comprehensive guide on how to create the perfect prompt for your coding projects.

---

## The Anatomy of a Perfect Coding Prompt

Think of the LLM as a brilliant but very literal junior developer who has zero context about your project. You need to provide that context clearly and concisely. A perfect prompt almost always contains these six key components.

### The 6 Core Components to Always Provide

#### 1. **Role & Goal (Set the Persona)**
Tell the chatbot *who* it should be. This primes the model to access a specific style of thinking and knowledge. Then, state your high-level objective.

*   **Bad:** "Help me with my code."
*   **Good:** "Act as a senior Python developer specializing in backend systems. My goal is to create a reliable API endpoint."

**Examples of Roles:**
*   "Act as a database architect..."
*   "You are a front-end developer with expertise in React and accessibility (WCAG) standards..."
*   "Behave as a cybersecurity expert reviewing this code for vulnerabilities..."

#### 2. **Context (The "What" and "Why")**
This is the most critical part. The LLM knows nothing about your project, your constraints, or your intentions.

*   **Technology Stack:** What language, framework, libraries, and versions are you using? (e.g., "I'm using Python 3.11 with FastAPI 0.95 and Pydantic v2.")
*   **Project Background:** What does the application do? What is the purpose of the code you're working on? (e.g., "This is for an e-commerce site. The function I need is supposed to calculate shipping costs based on weight and destination.")
*   **Existing Code (if any):** Provide the relevant, minimal code snippets. Don't paste your entire application.

#### 3. **Task (The "Do This")**
Be explicit and use action verbs. What do you want the LLM to *do*?

*   **Write:** "Write a new function that..."
*   **Debug:** "Find the bug in this code. It's supposed to do X, but it's doing Y instead."
*   **Explain:** "Explain this regular expression line by line."
*   **Refactor:** "Refactor this code to be more readable and efficient."
*   **Optimize:** "Optimize this database query for a PostgreSQL database."
*   **Suggest:** "Suggest three alternative ways to implement this feature."

#### 4. **Constraints & Requirements (The "How")**
This is where you guide the *quality* and *style* of the output.

*   **Rules:** "Do not use any external libraries." or "You must use the `requests` library."
*   **Style Guides:** "Follow the PEP 8 style guide." or "Use functional programming principles."
*   **Performance:** "The solution must be memory-efficient."
*   **Specifics:** "The function must include error handling for `FileNotFoundError` and network issues." or "Add comprehensive docstrings and type hints."

#### 5. **Input & Error Details (For Debugging)**
When debugging, you must provide more than just the code.

*   **The Code:** The function or block of code that is failing.
*   **The Exact Error Message:** Copy and paste the full traceback. This is non-negotiable.
*   **The Expected Outcome:** "I expected it to return `True`."
*   **The Actual Outcome:** "Instead, it's crashing with a `TypeError`."
*   **What You've Tried:** "I've already confirmed that the file path is correct." This saves time and prevents basic suggestions.

#### 6. **Output Format (The "Shape" of the Answer)**
Tell the LLM exactly how you want the answer presented. This saves you a lot of reformatting time.

*   "Provide only the code, inside a single Python code block."
*   "Give me the code first, followed by a bullet-point explanation of the changes."
*   "Present the alternatives in a Markdown table with columns for 'Approach', 'Pros', and 'Cons'."
*   "Generate the configuration in JSON format."

---

## Examples: Bad vs. Perfect Prompts

Let's see this in action with a few common scenarios.

### Scenario 1: Writing a New Function

> **Bad Prompt:**
> "write a python function to upload a file to s3"

*   *Why it's bad:* No context, no libraries mentioned, no error handling, no specifics. The LLM has to guess everything.

> **Perfect Prompt:**
> **Role:** "Act as a senior Python developer using AWS."
>
> **Context:** "I am building a data processing pipeline in Python 3.10 using the `boto3` library to interact with AWS S3. I need a utility function for uploading files."
>
> **Task:** "Write a Python function named `upload_file_to_s3`."
>
> **Constraints & Requirements:** "The function should take `file_path`, `bucket_name`, and `s3_object_name` as arguments. It must include robust error handling for common `boto3` exceptions (e.g., `ClientError`, `NoCredentialsError`) and for `FileNotFoundError`. The function should return `True` on success and `False` on failure. Please include a docstring explaining what it does, its parameters, and what it returns. Add type hints."
>
> **Output Format:** "Provide the complete function in a single Python code block."

### Scenario 2: Debugging Code

> **Bad Prompt:**
> "My javascript code is broken, fix it.
> `const data = fetch('api/user');`
> `const name = data.name;`"

*   *Why it's bad:* "Broken" is not an error message. No context on what `fetch` does or what the expected `data` structure is.

> **Perfect Prompt:**
> **Role:** "You are a JavaScript expert specializing in asynchronous operations."
>
> **Context:** "I'm trying to fetch user data from an API endpoint (`/api/user`) in a simple web app. The API is expected to return a JSON object like `{'id': 1, 'name': 'Alice'}`."
>
> **Task:** "I need to debug the following code snippet. My goal is to get the user's name and log it to the console."
>
> **Input & Error Details:**
> *   **Code:**
>     ```javascript
>     const data = fetch('/api/user');
>     const name = data.name;
>     console.log(name);
>     ```
> *   **Actual Outcome:** `console.log(name)` prints `undefined`.
> *   **Expected Outcome:** I expect it to print the user's name, e.g., "Alice".
> *   **My Suspicion:** I think it's a problem with how `fetch` works, but I'm not sure.
>
> **Output Format:** "Please explain why my code is not working and provide the corrected, modern JavaScript code using `async/await`."

---

## Pro-Tips for Advanced Interaction

*   **Iterative Prompting:** You don't have to get it perfect the first time. Treat it like a conversation.
    *   *Initial Prompt:* (A good prompt like the ones above)
    *   *Follow-up:* "That's great, thank you. Now, can you add logging to that function using Python's built-in `logging` module?"
    *   *Another Follow-up:* "Perfect. Now refactor it into a class called `S3Uploader`."
*   **Ask for Alternatives:** If you're unsure about the best approach, ask the LLM to be creative. "Give me three different ways to solve this problem in C#, and list the pros and cons of each."
*   **"Think Step-by-Step":** For complex logic or algorithms, add the phrase "Think step-by-step before you give the final answer." This forces the model to lay out its reasoning, which often leads to a more accurate result and helps you understand its logic.
*   **Always Verify:** **Never blindly trust the code.** Always read, understand, and test the code the LLM generates. It can make subtle mistakes, use outdated practices, or introduce security vulnerabilities. It's your assistant, not your replacement.
## Prompt number 2

**User:** Can you tell me what kind of prompt is better for LLM to work on? The first one is provided as a free text,
like "Let's shortly align technical expectations. I need this program to be written in python 3.11, but you can choose necessary libraries freely. I will be using pyenv to create the environment and pip to install packages. If anything is saved to the file system or read from it, you should start all the paths from current directory and eventually use subfolders. I need my code to follow PEP formatting standards. When providing me a code samples or scritps, always include name of the file in which the code should be put. Could you please confirm specified limitations? Do not generate any code yet."
The second one is provided in a more structured text, for example: "Goal: Setting up technical requirements for all code solutions generated through the conversation. 
Instruction: I need this program to be written in python 3.11, but you can choose necessary libraries freely. I will be using pyenv to create the environment and pip to install packages. If anything is saved to the file system or read from it, you should start all the paths from current directory and eventually use subfolders. I need my code to follow PEP formatting standards. When providing me a code samples or scritps, always include name of the file in which the code should be put. 
Expected Output: Confirmation of specified requirement. Apply it to every code generated in further parts of conversation, but do not generate any code for this answer."


**LLM Response:**

Excellent question. This gets to the heart of moving from casual LLM use to professional, effective use.

The short answer is: **The second, more structured prompt is vastly superior.**

Let's break down exactly why and how this structured approach will give you better, more reliable results throughout your coding project.

---

### Head-to-Head Comparison

| Aspect | Prompt 1 (Free Text) | Prompt 2 (Structured Text) | Winner & Why |
| :--- | :--- | :--- | :--- |
| **Clarity & Ambiguity** | The instructions are mixed with conversational filler ("Let's shortly align..."). The final request ("Could you please confirm...") is a soft question at the end of a paragraph. | Each part of the request has a clear, labeled purpose: **Goal**, **Instruction**, **Expected Output**. There is zero ambiguity. | **Prompt 2**. The LLM doesn't have to guess what's important. The labels act as signposts, telling the model exactly how to interpret each piece of information. |
| **Parsing Difficulty (for the LLM)** | The model must parse natural language to separate the constraints from the immediate task. It might get confused and think the main task is "write a program" before it gets to the final sentence. | The structure does the parsing *for* the model. It knows that the "Instruction" section contains rules for the future, and the "Expected Output" section is the *only* thing it needs to act on for this specific response. | **Prompt 2**. You are reducing the "cognitive load" on the LLM. Less parsing means less chance for error and a higher probability of getting exactly what you asked for. |
| **Reliability & Consistency** | There's a higher chance the LLM might ignore the "Do not generate any code yet" instruction because it's buried at the end of a request that talks a lot about code. | The `Expected Output` field is a powerful and direct command. It explicitly states the desired outcome for *this turn* of the conversation, making it extremely unlikely the model will deviate. | **Prompt 2**. This structure gives you fine-grained control over the model's output at each step, leading to highly reliable and consistent behavior. |
| **Scalability & Reusability** | This format is a one-off. For your next prompt, you'd have to re-explain or hope the model remembers the context from the previous turn (which is not always reliable). | This format is a **template**. You can reuse this structure for every subsequent request in your project. You simply update the `Instruction` and `Expected Output` sections. This is incredibly efficient for complex projects. | **Prompt 2**. It establishes a clear, reusable protocol for your entire interaction with the LLM, making your workflow much more scalable. |

---

### The Core Principle: You Are an API Designer

Think of prompting an LLM not as having a conversation, but as **making an API call**.

*   **Prompt 1 (Free Text)** is like sending a long, unformatted string to an API endpoint and hoping it figures out the parameters.
    `POST /api/execute?request="Let's align... I need python... do this... but don't do it yet."`
    This is messy and prone to failure.

*   **Prompt 2 (Structured Text)** is like sending a well-formed JSON payload to an API.
    ```json
    POST /api/execute
    {
      "goal": "Setting up technical requirements...",
      "context_rules": [
        "language: python 3.11",
        "packaging: pyenv + pip",
        "filesystem: relative paths",
        "formatting: PEP8",
        "output_style: include filenames"
      ],
      "immediate_task": "Confirm understanding of rules. Do not generate code."
    }
    ```
    This is clean, unambiguous, and easy for a machine to process correctly. Your structured prompt emulates this clarity.

### The Analogy: The Junior Developer vs. The Formal Ticket

Imagine you're a senior developer giving instructions.

*   **Prompt 1** is like grabbing a junior developer in the hallway and verbally telling them a bunch of requirements for a future task, ending with "got it?". They'll probably nod, but they might forget a detail or misunderstand the priority.

*   **Prompt 2** is like creating a formal ticket in a project management system (like Jira or Trello).
    *   **Goal:** This is the ticket's *Title* or *User Story*.
    *   **Instruction:** This is the *Description* and *Acceptance Criteria*.
    *   **Expected Output:** This is the *Definition of Done* for this specific task.

No developer would prefer the hallway conversation over the detailed ticket. The ticket is clear, documented, and leaves no room for error. **Treat your LLM the same way.**

### Conclusion

**Always use the second, structured approach.**

By providing a structured prompt with clear labels like `Goal`, `Context`, `Task`, `Constraints`, and `Expected Output`, you are:
1.  **Eliminating ambiguity.**
2.  **Improving reliability.**
3.  **Making your requests reusable and scalable.**
4.  **Forcing yourself to think more clearly about what you actually want.**

This initial setup prompt you've designed is a perfect example of "prompt engineering." You are setting the ground rules for the entire conversation. The LLM will now be primed to follow these rules for all subsequent code generation, making your entire project development process smoother and more efficient.
## Prompt number 3

**User:** Can you propose me a way to structure my prompts, so they will results in the best results?


**LLM Response:**

Of course. Building on your excellent intuition that structure is key, here is a universal, reusable prompt template designed to maximize clarity and produce the best possible results from an LLM for coding tasks.

This template, which I call the **"C.R.I.S.P." Prompting Framework** (Context, Role, Instruction, Specifics, Payout), formalizes the best practices into a structure you can copy and paste for every request.

---

### The C.R.I.S.P. Prompting Framework

This framework separates persistent rules from the immediate task, which is the most effective way to interact with an LLM for a multi-step project.

#### Part 1: The "Session Setup" Prompt

You only need to do this once at the very beginning of your chat session. This sets the ground rules for the entire project. Your structured prompt from the previous question was a perfect example of this.

**Goal:** To establish the foundational rules and context for the entire conversation.

```markdown
## 📜 SESSION CONTEXT & RULES

You are my expert programming assistant for this entire conversation. Adhere to the following rules for all responses unless I explicitly override them in a specific prompt.

- **Role:** Act as a Senior Python Developer with expertise in building robust, scalable web applications.
- **Technology Stack:**
  - Language: Python 3.11
  - Environment: `pyenv` for version management
  - Package Management: `pip` and `requirements.txt`
- **Coding Standards:**
  - Formatting: Strictly follow the PEP 8 style guide.
  - Naming: Use clear, descriptive variable and function names.
  - Documentation: Include type hints and Google-style docstrings for all functions and classes.
- **File System:**
  - All file paths must be relative to the project's root directory.
  - When suggesting code for a file, **always** specify the intended filename in a comment at the top, like `# filename: src/utils/helpers.py`.
- **Libraries:** You have the freedom to suggest and use well-known, reputable libraries (e.g., `requests`, `pydantic`, `fastapi`). For any new library added, you must also provide the command to add it to `requirements.txt`.

**Your Task for This Message:**
Acknowledge that you have understood these rules. Do not generate any code yet. Simply confirm with "Ready to start. All rules and context have been loaded."
```

---

#### Part 2: The "Task" Prompt Template (Use this for every subsequent request)

Once the LLM has confirmed the setup, you use this template for every task, from writing a function to debugging an error.

**Goal:** To get a specific, high-quality output for a single, well-defined task.

```markdown
## 🎯 INSTRUCTION

[Clearly and concisely state what you want the LLM to DO. Use action verbs. Examples: "Write a function...", "Refactor the following code...", "Find the bug...", "Explain this concept..."]

---

## 📝 SPECIFICS & CONSTRAINTS

[Provide all the necessary details and rules for THIS specific task. This is where you add requirements that aren't part of the global session rules.]

- **Function Signature (if applicable):** `def my_function(arg1: str, arg2: int) -> bool:`
- **Requirements:**
  - Must handle `ValueError` and return `False`.
  - Must be optimized for speed.
  - Cannot use any external libraries for this specific function.
- **Existing Code (if refactoring or debugging):**
  ```python
  # filename: src/main.py
  # [Paste the relevant, minimal code snippet here]
  ```
- **Error Message (if debugging):**
  ```
  # [Paste the full, exact error traceback here]
  ```

---

## 📤 EXPECTED PAYOUT (Output)

[Describe the exact format of the answer you want to receive. This saves you immense time.]

- **Format:** Provide the complete, final code in a single Python code block.
- **Explanation:** After the code block, add a brief, bulleted list explaining the key logic or changes.
- **Example:** "First the code, then a Markdown table comparing this approach to another one."
```

---

### Examples in Action

Let's see how you'd use the **Task Prompt Template** for common scenarios after the initial setup.

#### Example 1: Creating the Project Structure

```markdown
## 🎯 INSTRUCTION
Create the initial directory structure and a basic `requirements.txt` file for our new project.

---

## 📝 SPECIFICS & CONSTRAINTS
- **Requirements:**
  - The project should have a `src` directory for our Python code.
  - Inside `src`, create an empty `__init__.py` file.
  - Create a main application file inside `src`.
  - Create an empty `tests` directory at the root level.
  - The `requirements.txt` should include `fastapi` and `uvicorn`.

---

## 📤 EXPECTED PAYOUT (Output)
- **Format:** Provide a list of shell commands (`mkdir`, `touch`) to create the structure. Then, provide the content for `requirements.txt` and the main application file, each in its own code block with the filename specified.
```

#### Example 2: Writing a New Function

```markdown
## 🎯 INSTRUCTION
Write a Python function that fetches data from a given URL and parses it as JSON.

---

## 📝 SPECIFICS & CONSTRAINTS
- **Function Signature:** `def fetch_json_data(url: str) -> dict | None:`
- **Requirements:**
  - Use the `requests` library.
  - The function must have a 5-second timeout.
  - It needs robust error handling for:
    - Network issues (`requests.exceptions.RequestException`).
    - Invalid JSON (`json.JSONDecodeError`).
    - Non-200 status codes.
  - In case of any error, the function should log the error (just use a `print` statement for now) and return `None`.
- **Filename:** This function should go in `src/utils/api_client.py`.

---

## 📤 EXPECTED PAYOUT (Output)
- **Format:** Provide the complete Python function in a single code block.
- **Explanation:** Below the code, briefly explain the error handling strategy in a bulleted list.
- **Dependencies:** Include the line to add to `requirements.txt`.
```

#### Example 3: Debugging Code

```markdown
## 🎯 INSTRUCTION
Find and fix the bug in my `add_user` function.

---

## 📝 SPECIFICS & CONSTRAINTS
- **Context:** This function is supposed to take a user dictionary and add it to a global `users` list.
- **Existing Code:**
  # filename: src/main.py
  users = []

  def add_user(user: dict):
      user['id'] = len(users) + 1
      users.append(user)

  user_a = {"name": "Alice"}
  add_user(user_a)
  print(f"User A: {user_a}")

  user_b = {"name": "Bob"}
  add_user(user_b)
  print(f"User B: {user_b}")
 
- **The Problem:** When I run this, the output shows that `user_a` is being modified after `user_b` is added. The `id` of `user_a` changes.
- **Expected Behavior:** `user_a` should remain unchanged after `user_b` is added.

---

## 📤 EXPECTED PAYOUT (Output)
- **Format:** First, explain the concept of "pass-by-object-reference" in Python and why it's causing this bug. Then, provide the corrected `add_user` function in a Python code block.
```

By consistently using this structured C.R.I.S.P. framework, you are essentially turning the LLM into a predictable, highly-efficient tool that understands both the global project context and the specific requirements of any given task.
