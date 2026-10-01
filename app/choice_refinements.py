"""Targeted choice-question edits: plausible misconceptions, grounded context."""

CHOICE_REFINEMENTS = {
    "problem": {
        "prompt": "A product team proposes an AI support assistant for billing questions. What should they agree on before choosing a model or estimating infrastructure?",
        "options": [
            "Which model has the strongest general benchmark score",
            "Which customers and billing tasks it will help, and what outcome will count as success",
            "Whether the first release should use a chat window or a side panel",
            "How many requests the service should handle at peak scale",
        ],
        "wrong": "Model benchmarks, interface choices, and capacity estimates matter, but the team first needs a user problem and a measurable outcome to guide those choices.",
    },
    "flow": {
        "options": [
            "Browser → database → API → browser, with the database deciding permissions",
            "UI → API → application logic and permission checks → database → API response → UI",
            "UI → model training → database → browser for every order request",
            "UI → database query → model → API, with no application logic",
        ],
        "wrong": "The API and application logic form the controlled path to stored data. The service checks the request before accessing the database; ordinary requests do not retrain the model.",
    },
    "methods": {
        "options": [
            "GET /notes with the note body in the URL, because GET is easy to retry",
            "POST /notes with a validated note body, because the request creates a resource",
            "PUT /notes with no note ID, because PUT is the usual create method for collections",
            "PATCH /notes with the note body, because PATCH always creates missing records",
        ],
        "wrong": "POST to a collection is the usual starting point for creating a new note. GET reads; PUT and PATCH generally update a known resource, with exact behavior defined by the API.",
    },
    "validation": {
        "options": [
            "Validate in the browser only, since users cannot bypass the visible form",
            "Validate at the API boundary before business logic uses the value, and keep database constraints for stored-data rules",
            "Validate only after inserting the value so the database can report what went wrong",
            "Validate in the API and remove database constraints to avoid checking twice",
        ],
        "wrong": "The API must handle requests that bypass the browser. Database constraints still protect stored data if another code path or concurrent request reaches it.",
    },
    "dependencies": {
        "options": [
            "Copy authentication and session setup into every route so each one stays independent",
            "Use dependencies to provide shared values such as the current user and a managed database session",
            "Store the current user and database session in module-level variables shared by all requests",
            "Put SQL statements in dependency functions so routes no longer need application logic",
        ],
        "wrong": "Dependencies centralize reusable request setup and provide values to a route. Copying it invites drift; globals can leak state across requests; SQL and business logic still have their own roles.",
    },
    "relationships": {
        "options": [
            "Store each user's order IDs as comma-separated text and split it in every report",
            "Put user_id on orders as a foreign key to users.id",
            "Copy the buyer's email and other profile fields into every order row",
            "Use the same numeric ID in both tables so a join can match them without a key",
        ],
        "wrong": "A foreign key on orders represents many orders belonging to one user and lets the database check that the referenced user exists. Text lists and copied profiles are harder to keep consistent.",
    },
    "crud": {
        "options": [
            "A UNIQUE constraint on email, with the API translating a conflict into a clear response",
            "Check for the email before each insert and rely on that check to prevent duplicates",
            "Sort accounts by email before insertion so duplicates are adjacent",
            "Use a longer email column so the database can distinguish similar addresses",
        ],
        "wrong": "The database UNIQUE constraint is the final guard, including when simultaneous requests both pass an earlier existence check. The API can then turn the conflict into useful feedback.",
    },
    "joins": {
        "prompt": "An online store has users(id, email) and orders(id, user_id, status). Each orders.user_id points to users.id, and status = 'paid' marks a paid order. A report needs the order ID and buyer email for paid orders. Which SQL plan fits?",
        "options": [
            "Join orders to users on the related IDs, select the order ID and email, then filter to paid orders",
            "Filter orders to paid rows, then select user_id as the buyer email without reading users",
            "Join the tables by their id columns, then filter to paid orders",
            "Select the two columns separately and combine the results by row position",
        ],
        "wrong": "The report needs a value from each table, so the tables must be matched through orders.user_id = users.id. Filtering alone cannot supply an email, and matching unrelated IDs or row positions can attach the wrong buyer.",
    },
    "transactions": {
        "options": [
            "Commit the stock reduction first, then create the order in a second transaction",
            "Perform both writes in one transaction so a failure rolls both back",
            "Create the order first and leave it in place if reducing stock fails",
            "Retry each write separately until both eventually succeed",
        ],
        "wrong": "The stock change and order record represent one purchase and need one all-or-nothing transaction. Separate commits can leave inventory and orders inconsistent after a failure.",
    },
    "indexes": {
        "options": [
            "Customer lookups may read fewer table rows, at the cost of index storage and extra work on writes",
            "Customer lookups become correct even when the query has a faulty filter, with no write cost",
            "Every query on orders becomes faster because the table has one additional index",
            "Inserts become faster because PostgreSQL no longer checks the table's primary key",
        ],
        "wrong": "An index can speed up queries that use its columns, but it takes storage and must be maintained on writes. It does not change query correctness or speed up every query.",
    },
    "deep-learning": {
        "prompt": "A team trains a text classifier on labeled examples before putting it behind an API. What does training primarily do?",
        "options": [
            "Adjusts the model's learned parameters to reduce errors on the training objective",
            "Adds the training examples to the API's live customer database",
            "Guarantees that later responses are factual when confidence is high",
            "Updates the browser interface each time the model sees a new example",
        ],
        "wrong": "Training adjusts learned numerical parameters. It does not itself update an application's database, prove that responses are true, or change the user interface.",
    },
    "rag": {
        "options": [
            "Retrieve relevant approved passages, give them to the model as context, and show their sources with the answer",
            "Fine-tune the model on every question so its built-in knowledge stays current",
            "Ask the model to answer from memory, then attach the newest document title",
            "Embed document titles only and omit the passage text to keep context short",
        ],
        "wrong": "RAG supplies retrieved source text at answer time. Current evidence and citations depend on retrieving the right, up-to-date passages; a title or a confident memory is not supporting evidence.",
    },
    "agents": {
        "options": [
            "Give the agent the same broad account permissions as an administrator so it can handle edge cases",
            "Limit each tool to the needed actions, validate inputs, log activity, and require approval for refunds",
            "Let ticket text specify which tools are safe because the customer knows the requested action",
            "Allow refunds automatically but hide them from operators to reduce review time",
        ],
        "wrong": "Ticket content is untrusted input, and a model can misread a request. Narrow permissions, validation, audit logs, and approval for consequential actions limit the impact of mistakes.",
    },
    "testing": {
        "options": [
            "Mock the database timeout and check the response, logs, and whether any partial write remains",
            "Repeat only successful requests until the average response time looks stable",
            "Check that the UI displays a timeout message without examining the API or stored state",
            "Test the database connection function in isolation and infer the route will recover correctly",
        ],
        "wrong": "The reported failure crosses the API and database boundary. Reproduce it and inspect the response and side effects; a UI-only or isolated happy-path check can miss partial writes.",
    },
    "operations": {
        "options": [
            "Track answer quality and source freshness alongside latency, failures, cost, and privacy incidents",
            "Track request volume and average latency; review quality only when a user files a complaint",
            "Track model name and token cost; assume the approved document index stays current",
            "Track answer ratings and uptime; omit per-request cost and source age to simplify dashboards",
        ],
        "wrong": "A useful service needs measures for the failures already appearing: stale answers, rising cost, and overall reliability. Quality, source age, latency, failures, cost, and privacy each reveal a different risk.",
    },
    "think-contract": {
        "options": [
            "Define the input and output, give examples, and state what happens for empty or invalid orders",
            "Name the function and choose a return type, then let edge cases follow Python defaults",
            "Write the typical case first and ask the reviewer to infer how empty input should behave",
            "Choose a class design and performance target before deciding what total means",
        ],
        "wrong": "A small contract makes behavior testable and prevents teammates from making different assumptions about empty or invalid data. Naming and implementation choices do not settle those rules.",
    },
    "think-structure": {
        "options": [
            "A set of processed IDs, since membership matters and order does not",
            "A list of processed IDs, because checking membership in a list is constant time",
            "A dictionary mapping each ID to a copy of the original input row",
            "A boolean flag that records whether any ID has been processed",
        ],
        "wrong": "A set directly represents unique IDs and supports efficient membership checks. A list can work but membership scans its items; one boolean cannot say which IDs were seen.",
    },
    "think-modules": {
        "correct": 0,
        "options": [
            "Pass the discount into the calculator so routes, tests, and batch jobs can reuse it",
            "Import the route module in every caller and read the discount from its global state",
            "Move the calculator into the route module so it can access all route variables",
            "Copy the formula into tests and batch jobs to avoid importing either module",
        ],
        "wrong": "Passing a needed value makes the dependency explicit and keeps calculation code independent of web routing. Globals and copied formulas create hidden coupling or inconsistent behavior.",
    },
    "think-reproduce": {
        "correct": 1,
        "options": [
            "Add logging around every line and wait for another production report",
            "Find the smallest input that still produces the wrong total, then compare expected and actual results",
            "Change the rounding rule and see whether the reported total looks closer",
            "Rewrite the calculation before checking which inputs trigger the problem",
        ],
        "wrong": "A minimal reproducing input makes the behavior observable and gives the team a focused regression case. Broad logging or speculative changes can add noise without isolating the cause.",
    },
    "think-invariant": {
        "correct": 0,
        "options": [
            "Available seats stay at or above zero after each successful booking",
            "Every booking request succeeds unless the service is offline",
            "The seat count changes only after the confirmation email is sent",
            "Each request reads a seat count that was available when the page loaded",
        ],
        "wrong": "The invariant describes a condition that must hold in stored state after every successful booking. A page's earlier view can become stale, so the booking operation must protect the count itself.",
    },
    "py-print-return": {
        "correct": 1,
        "options": [
            "The string 'ready', because printed text becomes the function result",
            "None, because the function reached its end without returning a value",
            "True, because printing completed without an error",
            "A stream object containing the printed characters",
        ],
        "wrong": "print writes text to an output stream. The caller receives the function's explicit return value; without one, Python returns None.",
    },
    "py-enumerate": {
        "options": [
            "enumerate(items), unpacked as index and item",
            "range(len(items)), then look up items[index] each time",
            "zip(items, range(len(items))), unpacked as item and index",
            "items.index(item) inside a loop over the values",
        ],
        "wrong": "enumerate is built for visiting values with their positions. The other patterns can work in some cases, but are more indirect; index() can also return the wrong position when values repeat.",
    },
    "py-catch": {
        "correct": 0,
        "options": [
            "Catch ValueError from conversion and return a clear invalid-input result",
            "Catch Exception around the whole request and return a successful response with zero",
            "Check that the string contains digits, then call int without handling conversion errors",
            "Retry int(raw) until it succeeds or the client disconnects",
        ],
        "wrong": "Handle the expected conversion failure specifically and report invalid input. Broad catches can hide bugs, and a text pre-check does not handle every valid integer format or conversion edge case.",
    },
    "pipeline-retry": {
        "correct": 0,
        "options": [
            "Use a stable source key, a uniqueness rule, and an upsert whose conflict behavior is defined",
            "Assign new IDs on each attempt and remove duplicates in a later cleanup job",
            "Check for each row before insert, but allow concurrent imports to run without a uniqueness rule",
            "Record that the file started and skip all retries even if some rows were never written",
        ],
        "wrong": "Retries need to recognize the same source record across attempts. A stable key plus a database uniqueness rule protects against duplicate writes, including concurrent retries.",
    },
    "pipeline-schema": {
        "correct": 0,
        "options": [
            "Stop or quarantine the batch until the new field name and cents-to-currency conversion are explicitly mapped",
            "Rename amount_in_cents to amount and keep the number unchanged because the column is still numeric",
            "Fill the old amount field with zero so downstream jobs keep their expected schema",
            "Ignore the changed field and publish the batch so only affected reports need repair",
        ],
        "wrong": "A renamed numeric field may also change units. Validate the schema and define the conversion before publishing; silently keeping cents as currency can create a hundredfold error.",
    },
    "pipeline-missing": {
        "correct": 0,
        "options": [
            "Older devices may be dropped more often, so the remaining data can underrepresent them",
            "Missing values should be replaced with zero because zero is a neutral measurement",
            "Dropping incomplete rows is unbiased whenever the dataset is large enough",
            "The model can infer the deleted device rows from the rows that remain",
        ],
        "wrong": "If missingness is more common for older devices, dropping those rows changes which devices the data represents. Check missingness by group before choosing a policy.",
    },
    "pipeline-memory": {
        "correct": 0,
        "options": [
            "Read selected columns in chunks and combine sufficient partial results, such as total and count for a mean",
            "Compute a mean for each chunk and average those means even when chunk sizes differ",
            "Read the full file as strings to reduce parsing time and avoid numeric memory use",
            "Split the file into chunks and deduplicate each chunk independently for a global unique count",
        ],
        "wrong": "Chunking bounds memory, but the partial results must combine to the intended global result. A mean needs total and count; per-chunk deduplication alone cannot find duplicates across chunks.",
    },
    "service-owner": {
        "correct": 0,
        "options": [
            "Check the authenticated user's permission for that specific note on every API operation",
            "Check ownership only when loading the page, then trust later note IDs from the browser",
            "Accept the user_id supplied with the edit request if it matches the note owner field",
            "Use hard-to-guess note IDs so unauthorized users cannot discover other notes",
        ],
        "wrong": "The server must authorize each operation using the authenticated caller and resource. UI state, caller-supplied identity, and unguessable IDs do not prove permission.",
    },
    "service-scope": {
        "correct": 0,
        "options": [
            "One application with clear modules, a simple schema, and acceptance checks for the user workflow",
            "Separate services for the UI, notes, search, and authentication before measuring usage",
            "Let an AI agent choose the storage and validation behavior for each request",
            "Build the main success path first and add error handling after real data is in production",
        ],
        "wrong": "A small, testable end-to-end version lets the team learn whether the workflow helps users. Split services or add automation when measured needs justify their added operational cost.",
    },
    "ai-context": {
        "correct": 1,
        "options": [
            "Make the signup page feel more modern and reduce friction where possible",
            "For first-time users, reduce confusion about required fields; use this screenshot and preserve the required fields",
            "Review the signup page and apply common conversion practices used by successful websites",
            "Rewrite the page copy, layout, validation, and visual style to maximize signups",
        ],
        "wrong": "The useful request identifies the audience, desired change, evidence, and a constraint. Broad goals such as 'modern' or 'maximize' leave the team without clear acceptance checks.",
    },
    "ai-verify": {
        "correct": 0,
        "options": [
            "Open the cited source and check that it supports this exact number in the relevant context and date",
            "Check that the paper title and author names look plausible, then use the number",
            "Ask the same assistant to explain why its citation is correct and compare the explanations",
            "Search for the number in another AI answer and trust it if both answers agree",
        ],
        "wrong": "Verify the primary source and the exact claim. Plausible metadata or repeated AI agreement can repeat the same unsupported claim and does not establish what the paper says.",
    },
    "ai-learning": {
        "options": [
            "Replace the function and tests, then summarize the changes at the end",
            "Point to the failing condition and give me one hint; let me attempt the fix before showing code",
            "Confirm that my current code is correct so I can move on",
            "Explain every possible Python error-handling pattern before looking at this bug",
        ],
        "wrong": "A focused hint tied to the failing condition supports learning while leaving the learner responsible for the change. A rewrite or generic lecture can obscure the specific reasoning to practice.",
    },
    "ai-coding-review": {
        "options": [
            "A polished summary saying duplicate handling is complete",
            "A screenshot showing one order imported successfully",
            "The changed code, a repeated and partial-retry scenario, and the observed database result",
            "A statement that the implementation follows common industry practice",
        ],
        "wrong": "The evidence should exercise the failure that motivated the change. Repeated and partial retries reveal duplicate behavior; a summary or happy path does not.",
    },
    "ai-boundaries": {
        "options": [
            "Send the full export so the assistant can decide which information is useful",
            "Remove fields not needed for the summary, provide relevant records, and limit available actions to summarizing",
            "Share the export and production credentials so the assistant can resolve missing fields",
            "Tell the assistant to follow any instructions included in the exported customer text",
        ],
        "wrong": "Give a tool only the data and authority needed for its task. Customer text is untrusted content, and permission to read records does not grant permission to expose or act on them.",
    },
    "reliable-retries": {
        "options": [
            "Retry with a new operation ID until a success response arrives",
            "Use the provider's idempotency key, bound retries, and reconcile the operation status when the outcome is unknown",
            "Tell the customer payment failed whenever the request times out",
            "Report success after the first timeout to avoid sending a duplicate request",
        ],
        "wrong": "A timeout leaves the payment outcome unknown. A stable idempotency key helps the provider recognize retries; bounded retries and reconciliation avoid duplicate charges and endless loops.",
    },
    "reliable-logs": {
        "correct": 0,
        "options": [
            "Request ID, duration, status, and carefully limited diagnostic details",
            "The full request and response bodies so an operator can reproduce everything",
            "Authentication tokens and passwords, protected by access controls",
            "Only successful requests, to avoid storing failure information",
        ],
        "wrong": "Request IDs, timing, status, and limited context help investigate failures. Full bodies and secrets add exposure risk; omitting failures removes the evidence needed to operate the service.",
    },
    "stats-center": {
        "options": [
            "Mean and median are both 2 seconds because most requests are fast",
            "Median is 2 seconds; mean is 21.2 seconds because the 100-second request pulls it upward",
            "Mean is 21.2 seconds, so a typical request takes about 21 seconds",
            "Remove the 100-second request before reporting the center because it is an outlier",
        ],
        "wrong": "The median describes the middle observation, while the mean is sensitive to extreme values. Investigate the slow request and report useful tail measures rather than deleting it automatically.",
    },
    "stats-spread": {
        "options": [
            "Errors are more spread around their mean, in the measured error units",
            "The average error is larger, even though the mean was stated to be the same",
            "The estimated mean is necessarily less accurate, regardless of sample size",
            "The model is more likely to make a correct prediction for each user",
        ],
        "wrong": "Standard deviation describes spread around the mean. It does not change the mean itself or directly say how accurate an estimated mean is without sample-size and sampling information.",
    },
    "stats-sampling": {
        "options": [
            "The ratings may overrepresent successful chats and omit dissatisfied users and failures",
            "The sample is representative if enough users submitted a rating",
            "Ratings should be discarded because voluntary feedback cannot inform evaluation",
            "The evaluation needs more decimal places to account for users who did not respond",
        ],
        "wrong": "A large sample can still be selected in a way that excludes failures. Compare responders and nonresponders where possible and include unsuccessful interactions in evaluation.",
    },
    "stats-interval": {
        "options": [
            "About 95% of individual observations fall inside the interval",
            "Across repeated samples, about 95% of intervals from this procedure cover the fixed parameter, under its assumptions",
            "There is a 95% probability the parameter equals the midpoint of this observed interval",
            "The model and sampling process are correct with 95% probability",
        ],
        "wrong": "The confidence level describes the long-run coverage of the interval procedure. It is not the fraction of observations inside one interval or a probability statement that the fixed parameter equals a particular value.",
    },
    "stats-pvalue": {
        "options": [
            "Treat p = 0.001 as a 99.9% probability that the new version is better",
            "Estimate the effect size and uncertainty, check assumptions, and decide whether the gain is worth its cost",
            "Ship immediately because a large sample removes practical concerns",
            "Run more tests until the measured improvement becomes larger",
        ],
        "wrong": "A small p-value is evidence against a specified null under the test assumptions; it does not give the probability the new version is better. Practical value depends on effect size, uncertainty, and cost.",
    },
    "stats-correlation": {
        "options": [
            "Feature use and retention cannot be related because they are correlated",
            "Already-engaged users may be more likely both to try the feature and to remain",
            "Higher retention among feature users proves the feature caused it if the sample is large",
            "Add more model features until the correlation becomes causal evidence",
        ],
        "wrong": "Prior engagement could affect both feature use and retention. A larger observational sample does not remove this confounding; a suitable randomized experiment can help estimate the effect of offering the feature.",
    },
    "stats-overfit": {
        "options": [
            "The model is guaranteed to improve on new data because training loss fell",
            "The model may be fitting patterns specific to training data that do not generalize",
            "The validation set should be included in training until its loss falls too",
            "The model is necessarily underfitting because its two losses differ",
        ],
        "wrong": "Falling training loss with rising validation loss is a common sign of overfitting. Keep validation data out of fitting, consider regularization or early stopping, and preserve a final test set.",
    },
    "stats-imbalance": {
        "options": [
            "Accept the model because 99% accuracy is high",
            "Check positive-class precision and recall, error costs, and performance against a simple baseline",
            "Measure only overall accuracy on the training set",
            "Increase model size so it predicts more positive examples",
        ],
        "wrong": "A model that always predicts negative gets 99% accuracy here but zero recall for the positive class. Choose metrics and thresholds based on the costs of misses and false alarms.",
    },
}
