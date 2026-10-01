"""Curated content. Add questions here without changing the web routes."""

QUESTIONS = [
    {
        "id": "problem", "kind": "choice", "topic": "Problem definition",
        "prompt": "A team says, ‘Build an AI support bot.’ What should you clarify first?",
        "options": ["Which model has the most parameters?", "Who needs help, with which tasks, and how will success be measured?", "Which color should the chat button be?", "How many servers should we buy?"],
        "correct": 1,
        "explanation": "Start with the user, the problem, and a measurable result. For example: reduce the time to answer common billing questions while keeping incorrect answers below a chosen threshold. This guides every later design choice.",
        "wrong": "Model size, visual design, and infrastructure matter later. None tells you whether the service solves a real problem.",
        "hints": ["Think about what you would need to judge whether the project worked."]
    },
    {
        "id": "flow", "kind": "choice", "topic": "Service flow",
        "prompt": "A user clicks ‘Show my orders.’ Which flow best describes a typical service?",
        "options": ["Database → UI → API → user", "UI → API → application logic → database → API response → UI", "UI → model training → database → browser", "API → UI → database → application logic"],
        "correct": 1,
        "explanation": "The browser sends a request to an API. Application logic checks it and reads the database. The API sends data back, and the UI displays it.",
        "wrong": "The browser usually cannot safely query the service database directly, and model training is not part of each ordinary request.",
        "diagram": ["UI", "API", "Logic", "Database", "Response"],
        "hints": ["Start at the click in the browser, then follow the request to stored data."]
    },
    {
        "id": "methods", "kind": "choice", "topic": "FastAPI routes",
        "prompt": "Which route is the best starting point for creating a new note?",
        "options": ["GET /notes with the note text in the URL", "POST /notes with the note data in the request body", "DELETE /notes with the note data in a cookie", "GET /health with the note data"],
        "correct": 1,
        "explanation": "POST is commonly used to create a resource. A FastAPI route such as @app.post('/notes') receives a request body, validates it, and stores the new note.",
        "wrong": "GET is meant for reading and may be cached. DELETE removes resources. A health route should report service status.",
        "hints": ["Which HTTP method normally creates something?"]
    },
    {
        "id": "validation", "kind": "choice", "topic": "Validation",
        "prompt": "An API expects an order quantity greater than zero. Why validate it at the API boundary?",
        "options": ["It makes the browser load faster", "It rejects bad input before business logic or the database uses it", "It replaces all database constraints", "It hides the endpoint from attackers"],
        "correct": 1,
        "explanation": "Validation catches malformed or impossible input early and returns a clear error. In FastAPI, a typed request model can do much of this work. Database constraints still protect stored data.",
        "wrong": "Validation does not replace database constraints or access control.",
        "hints": ["Think about where a negative quantity should be stopped."]
    },
    {
        "id": "dependencies", "kind": "choice", "topic": "FastAPI dependencies",
        "prompt": "Several FastAPI routes need the current user and a database session. What is a useful role for dependencies?",
        "options": ["They make SQL unnecessary", "They provide shared setup such as authentication and a database session", "They force every route to use the same HTTP method", "They store all user data in Python globals"],
        "correct": 1,
        "explanation": "A dependency supplies a value or performs shared setup for a route. Authentication checks and managed database sessions are common examples.",
        "wrong": "Dependencies organize shared work; they do not remove the need for queries or make global variables a database.",
        "hints": ["Look for the repeated setup each route needs."]
    },
    {
        "id": "relationships", "kind": "choice", "topic": "PostgreSQL relationships",
        "prompt": "You have users and orders. Each order belongs to one user. Which design best represents that relationship?",
        "options": ["Store all orders as comma-separated text in users", "Put a user_id foreign key on orders", "Copy the entire user record into each order", "Give users and orders identical primary keys"],
        "correct": 1,
        "explanation": "orders.user_id points to users.id. A foreign key keeps references valid and lets a JOIN combine order and user information.",
        "wrong": "Comma-separated values are hard to query; copies drift; matching primary keys incorrectly implies a one-to-one relationship.",
        "hints": ["Which column lets many order rows point to one user row?"]
    },
    {
        "id": "crud", "kind": "choice", "topic": "CRUD and constraints",
        "prompt": "A signup service must prevent two accounts from using the same email. Which protection should the database enforce?",
        "options": ["A UNIQUE constraint on email", "An ORDER BY email clause", "A SELECT before every INSERT, with no constraint", "A larger VARCHAR length"],
        "correct": 0,
        "explanation": "UNIQUE protects the rule even if two requests arrive at once. INSERT creates rows, SELECT reads, UPDATE changes, and DELETE removes them: the four CRUD actions.",
        "wrong": "A separate SELECT can race with another request. ORDER BY sorts results; column length does not prevent duplicates.",
        "hints": ["Think about a rule the database can enforce even under simultaneous requests."]
    },
    {
        "id": "joins", "kind": "choice", "topic": "Filtering and joins",
        "prompt": "You need paid orders and each buyer's email. Which SQL idea is needed?",
        "options": ["JOIN orders to users, then filter with WHERE", "ORDER BY alone", "DELETE orders that are unpaid", "Create an index instead of querying"],
        "correct": 0,
        "explanation": "JOIN connects related tables through keys. WHERE filters rows, for example WHERE orders.status = 'paid'. An index may speed the query but does not change its meaning.",
        "wrong": "Sorting, deleting, or indexing cannot by itself combine the buyer information with paid orders.",
        "hints": ["You need columns from two tables and only some rows."]
    },
    {
        "id": "transactions", "kind": "choice", "topic": "Transactions",
        "prompt": "A purchase must reduce stock and create an order. What should happen if creating the order fails?",
        "options": ["Keep the stock reduction", "Roll back both changes in one transaction", "Retry forever without logging", "Delete all other orders"],
        "correct": 1,
        "explanation": "A transaction makes related writes succeed together or fail together. Without it, stock can fall even though no order exists.",
        "wrong": "Keeping only one change leaves inconsistent data. Endless retry and unrelated deletes create new problems.",
        "hints": ["These two database changes must agree."]
    },
    {
        "id": "indexes", "kind": "choice", "topic": "Indexes",
        "prompt": "A large orders table is often filtered by customer_id. What is a likely benefit and cost of an index on that column?",
        "options": ["Faster matching reads; extra storage and write work", "Guaranteed correct answers; no cost", "All queries become faster; inserts become free", "The database no longer needs a primary key"],
        "correct": 0,
        "explanation": "An index helps PostgreSQL find matching rows without scanning every row. It occupies space and must be updated when data changes. Measure the real query before adding many indexes.",
        "wrong": "Indexes affect access speed, not correctness, and they have maintenance costs.",
        "hints": ["Think of an index in a book, plus the work of keeping it current."]
    },
    {
        "id": "deep-learning", "kind": "choice", "topic": "Deep learning",
        "prompt": "What does training a deep learning model mainly change?",
        "options": ["Its learned parameters, based on many examples", "The rows in your live customer database", "Every answer into a verified fact", "The user's browser source code"],
        "correct": 0,
        "explanation": "Training adjusts many numerical parameters so the model learns patterns. A trained model can still be wrong, so a service needs evaluation and safeguards.",
        "wrong": "Training does not automatically verify facts or update an application's live data.",
        "hints": ["What numerical parts of a neural network are learned?"]
    },
    {
        "id": "rag", "kind": "choice", "topic": "RAG and embeddings",
        "prompt": "A policy assistant needs answers from the latest approved documents. What is a sensible RAG flow?",
        "options": ["Retrieve relevant documents, pass their text to the model, and cite them", "Retrain the whole model after every question", "Let the model guess from memory and call it current", "Only store document titles"],
        "correct": 0,
        "explanation": "Retrieval-augmented generation finds relevant source passages before generation. Embeddings can help find semantically similar passages, but retrieval quality and document freshness still need checks.",
        "wrong": "A model's memory may be stale. Titles alone lack evidence, and full retraining per question is impractical.",
        "diagram": ["Question", "Retrieve", "Source text", "Model", "Cited answer"],
        "hints": ["Find evidence first, then form the answer from it."]
    },
    {
        "id": "agents", "kind": "choice", "topic": "Agents and permissions",
        "prompt": "An AI agent can read support tickets and issue refunds. Which design is safest for a first release?",
        "options": ["Give it admin access to every tool", "Use narrow tool permissions, limits, logs, and approval for refunds", "Hide all actions from operators", "Treat every ticket as a trusted instruction"],
        "correct": 1,
        "explanation": "An agent chooses actions using tools. Limit each tool's authority, validate its inputs, log actions, and require approval for costly or irreversible operations. Ticket text is untrusted data.",
        "wrong": "Broad permissions and untrusted ticket instructions can produce unauthorized actions.",
        "hints": ["What if a ticket contains a malicious instruction or a refund is wrong?"]
    },
    {
        "id": "testing", "kind": "choice", "topic": "Testing and errors",
        "prompt": "A service works for the happy path but occasionally times out when a database is unavailable. What test is most useful next?",
        "options": ["Only test a button's color", "Simulate database failure and check the API returns a useful error without corrupting data", "Remove error logs", "Assume the next deployment fixes it"],
        "correct": 1,
        "explanation": "Reliability tests include failure paths. The service should time out sensibly, report a safe error, log enough detail for operators, and avoid partial writes.",
        "wrong": "Visual polish and hope do not tell you how the service behaves during failure.",
        "hints": ["Reproduce the failure and inspect both the response and stored data."]
    },
    {
        "id": "operations", "kind": "choice", "topic": "Privacy, freshness, cost, monitoring, evaluation",
        "prompt": "An AI answer service is accurate in demos but becomes expensive and sometimes quotes old policy. What should the team track?",
        "options": ["Only total page views", "Answer quality, source age, latency, error rate, token cost, and exposure of private data", "Only the model name", "Only CSS bundle size"],
        "correct": 1,
        "explanation": "A working service needs ongoing evaluation and monitoring. Track quality and freshness alongside speed, failures, cost, and privacy. Set alerts and review real failures with protected user data.",
        "wrong": "A single popularity or technical metric misses reliability, safety, and cost.",
        "hints": ["What would reveal stale answers, outages, rising bills, or a privacy leak?"]
    },
    {
        "id": "py-normalize", "kind": "code", "language": "Python", "topic": "Python functions",
        "prompt": "Write a function normalize_email(email) that returns the email with surrounding whitespace removed and letters lowercased.",
        "starter": "def normalize_email(email):\n    # return the cleaned email\n",
        "hints": ["A string has a .strip() method for surrounding whitespace.", "A string has a .lower() method. You can call one method after the other.", "Return email.strip().lower()."],
        "reference": "def normalize_email(email):\n    return email.strip().lower()",
        "syntax": "def names a function; email is its input; return sends the result back. .strip() removes outer whitespace and .lower() changes letters to lowercase.",
        "service": "An API might normalize a submitted email before looking up an account.",
        "pitfall": "Calling the methods without returning the result leaves the caller with None. Strings are immutable, so the original input is not changed."
    },
    {
        "id": "py-filter", "kind": "code", "language": "Python", "topic": "Python filtering",
        "prompt": "Write paid_ids(orders). Each order is a dictionary with id and status. Return a list of ids for orders whose status is 'paid'.",
        "starter": "def paid_ids(orders):\n    # example: [{'id': 3, 'status': 'paid'}] -> [3]\n",
        "hints": ["Loop through each dictionary in orders.", "Check order['status'] == 'paid', then append order['id'] to a result list.", "A list comprehension is also valid: [o['id'] for o in orders if o['status'] == 'paid']."],
        "reference": "def paid_ids(orders):\n    return [order['id'] for order in orders if order['status'] == 'paid']",
        "syntax": "The expression before for becomes each output item. for visits every order; if keeps only matching ones. Square brackets build a list.",
        "service": "Application logic may filter fetched records before shaping an API response, though large datasets should usually be filtered in SQL.",
        "pitfall": "Using = instead of == does not compare values. Returning the full order dictionaries misses the requested ids."
    },
    {
        "id": "py-count", "kind": "code", "language": "Python", "topic": "Python dictionaries",
        "prompt": "Write count_statuses(orders) to return a dictionary counting orders by status. Example: ['paid', 'paid', 'new'] statuses become {'paid': 2, 'new': 1}.",
        "starter": "def count_statuses(orders):\n    # each order is a dict with a 'status' key\n",
        "hints": ["Start with counts = {} and loop through orders.", "For each status, use counts.get(status, 0) to get its current count or zero.", "Increase that count by one and return counts after the loop."],
        "reference": "def count_statuses(orders):\n    counts = {}\n    for order in orders:\n        status = order['status']\n        counts[status] = counts.get(status, 0) + 1\n    return counts",
        "syntax": "{} makes a dictionary. for repeats the indented block. .get(key, 0) supplies zero when the key is absent; assignment stores the new count.",
        "service": "A dashboard endpoint might summarize statuses for a small in-memory result; a large production table is better aggregated with SQL GROUP BY.",
        "pitfall": "Using counts[status] before the first value exists raises KeyError. Returning inside the loop counts only the first order."
    },
    {
        "id": "sql-join", "kind": "code", "language": "PostgreSQL", "topic": "SQL joins and filtering",
        "prompt": "Tables: users(id, email) and orders(id, user_id, status). Write a query returning each paid order's id and its buyer's email.",
        "starter": "SELECT ...\nFROM orders ...",
        "hints": ["Start FROM orders and JOIN users using orders.user_id = users.id.", "SELECT orders.id and users.email.", "Use WHERE orders.status = 'paid'."],
        "reference": "SELECT orders.id, users.email\nFROM orders\nJOIN users ON orders.user_id = users.id\nWHERE orders.status = 'paid';",
        "syntax": "SELECT names output columns. FROM chooses the starting table. JOIN ... ON matches related rows. WHERE keeps only paid orders.",
        "service": "A FastAPI route could execute a parameterized version of this query to show a paid-order report.",
        "pitfall": "Leaving out the JOIN condition can pair every order with every user. Filtering on the wrong status returns the wrong set."
    },
    {
        "id": "py-error", "kind": "code", "language": "Python", "topic": "Python error handling",
        "prompt": "Write parse_quantity(raw). Convert raw to an integer. Return None if it is not an integer or if the value is less than 1.",
        "starter": "def parse_quantity(raw):\n    # return a positive int or None\n",
        "hints": ["int(raw) can raise ValueError or TypeError.", "Use try/except around int(raw), then compare the result with 1.", "Return quantity if quantity >= 1 else None."],
        "reference": "def parse_quantity(raw):\n    try:\n        quantity = int(raw)\n    except (ValueError, TypeError):\n        return None\n    return quantity if quantity >= 1 else None",
        "syntax": "try runs code that may fail; except catches named errors. int converts a value. The conditional expression chooses a return value.",
        "service": "An API may convert input before business logic, though FastAPI request models can perform common validation automatically.",
        "pitfall": "A broad except hides programming mistakes. Accepting zero or negative values violates the stated rule."
    },
    {
        "id": "sql-table", "kind": "code", "language": "PostgreSQL", "topic": "SQL tables and constraints",
        "prompt": "Write SQL to create a notes table with an auto-generated integer id, a required body, and a user_id that references users(id).",
        "starter": "CREATE TABLE notes (\n    ...\n);",
        "hints": ["Use CREATE TABLE notes (...).", "An identity column can be id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY.", "Use body text NOT NULL and user_id integer NOT NULL REFERENCES users(id)."],
        "reference": "CREATE TABLE notes (\n    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n    body text NOT NULL,\n    user_id integer NOT NULL REFERENCES users(id)\n);",
        "syntax": "CREATE TABLE defines storage. PRIMARY KEY uniquely identifies a row. NOT NULL requires a value. REFERENCES creates a foreign key to users.",
        "service": "The database schema supports a notes API; route code inserts, reads, updates, or deletes rows against it.",
        "pitfall": "Without NOT NULL, blank missing values can be stored. Without the foreign key, a note can point to a user who does not exist."
    },
]

from .curriculum import ADDITIONAL_QUESTIONS, CATEGORIES, ORIGINAL_CATEGORIES

# Preserve every original ID, prompt, answer, and position for saved progress.
LEGACY_IDS = [question["id"] for question in QUESTIONS]
for category, ids in ORIGINAL_CATEGORIES.items():
    for question in QUESTIONS:
        if question["id"] in ids:
            question["category"] = category
QUESTIONS += ADDITIONAL_QUESTIONS
BY_ID = {question["id"]: question for question in QUESTIONS}
if len(BY_ID) != len(QUESTIONS):
    raise ValueError("Question IDs must be unique")


def public_question(question):
    """Send prompts and hints, but withhold answers until submission."""
    keys = ("id", "kind", "category", "topic", "prompt", "options", "language", "starter", "hints", "example")
    return {key: question[key] for key in keys if key in question}
