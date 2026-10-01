"""Worked reasoning and transfer practice for the coding exercises."""

CODE_GUIDES = {
    "py-normalize": {
        "steps": [
            "The input and output are both strings; clean the value and return it.",
            "Remove whitespace at the two ends first. Then lowercase the remaining letters.",
            "String methods return a new string, so pass the result of the first method to the next one.",
        ],
        "trace": "For '  Ada@EXAMPLE.COM  ': strip() gives 'Ada@EXAMPLE.COM'; lower() then gives 'ada@example.com'.",
        "practice": "What should normalize_email('  Help@Site.IO ') return?",
        "practice_answer": "'help@site.io'",
    },
    "py-filter": {
        "steps": [
            "The input is a list of order dictionaries; the output should be a new list of IDs.",
            "Visit orders one at a time and read each order's status.",
            "Only when the status equals 'paid', take the id field. Add that value, not the whole dictionary, to the output.",
        ],
        "trace": "For [{'id': 3, 'status': 'paid'}, {'id': 4, 'status': 'new'}], the first row contributes 3 and the second is skipped, so the result is [3].",
        "practice": "For orders with IDs 8 (paid), 9 (refunded), and 10 (paid), what list should be returned?",
        "practice_answer": "[8, 10]",
    },
    "py-count": {
        "steps": [
            "A dictionary is a good result because each status is a key and its number of occurrences is the value.",
            "For each order, get its status and read the current count. A status seen for the first time needs a starting count of zero.",
            "Add one, save the updated value under that status, and return the completed dictionary after the loop.",
        ],
        "trace": "For statuses paid, paid, new: paid changes 0→1→2; new changes 0→1. The result is {'paid': 2, 'new': 1}.",
        "practice": "Trace statuses new, paid, new, new. What dictionary should the function return?",
        "practice_answer": "{'new': 3, 'paid': 1}; dictionary key order is not important for this result.",
    },
    "sql-join": {
        "steps": [
            "The requested output has one field from each table, so both tables must be part of the query.",
            "Start from orders and match each order's user_id to users.id. This connects an order to its buyer.",
            "Select the order ID and email, then filter orders to status 'paid'. Use table-qualified column names because both tables have an id.",
        ],
        "trace": "An order (id 12, user_id 4, paid) joins to user (id 4, email a@example.com), producing (12, a@example.com). An unpaid order is removed by WHERE.",
        "practice": "If order 15 belongs to user 2 whose email is b@example.com and is paid, what row appears in the result?",
        "practice_answer": "(15, 'b@example.com')",
    },
    "py-error": {
        "steps": [
            "Separate conversion failure from a successfully converted but disallowed number.",
            "Put only int(raw) inside try because that conversion can raise ValueError for text or TypeError for an unsupported value.",
            "On either conversion error return None. Otherwise accept values at least 1 and reject 0 or negatives.",
        ],
        "trace": "'4' converts to 4 and is returned; 'four' raises ValueError and returns None; '0' converts successfully but fails the minimum check and returns None.",
        "practice": "What should parse_quantity(-2), parse_quantity('7'), and parse_quantity(None) return, in that order?",
        "practice_answer": "None, 7, None.",
    },
    "sql-table": {
        "steps": [
            "Translate each requirement into one column rule: generated identity, required body, and required user relationship.",
            "Make id an integer identity and primary key so PostgreSQL assigns a unique identifier.",
            "Use NOT NULL for required fields. Add REFERENCES users(id) to user_id so every note points to an existing user.",
        ],
        "trace": "A row with a body and an existing user_id can be inserted without supplying id. A missing body or nonexistent user is rejected by the database.",
        "practice": "If notes should also record a required title, which column definition would you add?",
        "practice_answer": "title text NOT NULL,",
    },
    "think-total": {
        "steps": [
            "The function receives its data as an argument and should return a value; it does not need to read a file or print.",
            "The required operation is addition across all items, which Python's sum performs.",
            "Return that sum directly. The empty list naturally sums to zero, matching the stated rule.",
        ],
        "trace": "sum([4, 6, 2]) adds 4 + 6 + 2 to produce 12; sum([]) produces 0.",
        "practice": "What should total_cost([2.5, 1.5]) return?",
        "practice_answer": "4.0 (numerically equal to 4).",
    },
    "think-unique": {
        "steps": [
            "Two properties are needed at once: a set can quickly tell whether an ID was seen, and a list preserves encounter order.",
            "Walk through the input from left to right. For each new ID, record it in the set and append it to the output list.",
            "Skip IDs already in the set. Return the list after visiting every item; do not convert the set to a list because that loses the order guarantee.",
        ],
        "trace": "For [8, 3, 8], keep 8, keep 3, skip the second 8. The output remains [8, 3].",
        "practice": "What does unique_ids([5, 5, 2, 5, 2, 7]) return?",
        "practice_answer": "[5, 2, 7]",
    },
    "think-boolean": {
        "steps": [
            "The rule says both conditions must hold, so translate the word AND literally into Python's and operator.",
            "The function already receives two boolean values; no loop or conversion is needed.",
            "Return the combined expression. Check the cases where either input is False to ensure neither can publish alone.",
        ],
        "trace": "True and True is True. True and False, False and True, and False and False are all False.",
        "practice": "What should can_publish(False, True) return, and why?",
        "practice_answer": "False, because validity is required as well as approval.",
    },
    "py-default": {
        "steps": [
            "The parameter uses None as a signal that the caller did not supply a list.",
            "Create a new empty list inside the function only in that case; this gives separate calls separate lists.",
            "Append the tag to whichever list is now in tags, then return that list so the caller can use it.",
        ],
        "trace": "Two calls add_tag('new') each begin with their own None and create separate ['new'] lists. Passing ['old'] instead mutates and returns that supplied list as ['old', 'new'].",
        "practice": "What does add_tag('urgent', ['open']) return?",
        "practice_answer": "['open', 'urgent']",
    },
    "sql-revenue": {
        "steps": [
            "First decide which source rows are eligible: only paid orders belong in the totals, so filter them before grouping.",
            "Group the remaining rows by customer_id and calculate SUM(amount) for each group.",
            "The minimum-total condition applies to an aggregate, so use HAVING after GROUP BY. Name the sum total_paid for the output.",
        ],
        "trace": "Customer 1 has two paid amounts 60 and 50, totaling 110, so it passes HAVING >= 100. Customer 2's unpaid 200 is excluded before aggregation.",
        "practice": "A customer has paid orders of 40, 35, and 30. Do they appear with the threshold 100, and with what total?",
        "practice_answer": "Yes: total_paid is 105.",
    },
    "sql-upsert": {
        "steps": [
            "Insert the snapshot value for customer 7 into the two named columns.",
            "The primary key is customer_id, so name it in ON CONFLICT to handle an existing customer row.",
            "On conflict replace total with EXCLUDED.total, which means the value from this attempted insert. This makes a retry safe for an absolute snapshot.",
        ],
        "trace": "If the existing total is 90.00, inserting the new snapshot changes it to 125.50. Repeating the same statement leaves it at 125.50 rather than adding again.",
        "practice": "If customer 7's incoming absolute snapshot is 140.00 and the statement is retried, what should the stored total be?",
        "practice_answer": "140.00 after the first run and still 140.00 after the retry.",
    },
    "pandas-clean": {
        "steps": [
            "Copy the DataFrame first because the prompt requires the input to remain unchanged.",
            "Convert amount to numeric with invalid strings coerced to missing values; this lets one mask handle both invalid and missing entries.",
            "Keep rows where amount is present and at least zero. Use pandas' elementwise & and .loc, then return a copy of the selected rows.",
        ],
        "trace": "['10', 'bad', None, '-3', '0'] becomes [10, NaN, NaN, -3, 0]. The mask keeps 10 and 0; the original DataFrame still has its original strings and values.",
        "practice": "After cleaning amounts ['2.5', '-1', 'oops'], which numeric values remain?",
        "practice_answer": "[2.5]",
    },
    "pandas-daily": {
        "steps": [
            "Parse the timestamp column as datetimes and normalize each instant to UTC before deciding which calendar day it belongs to.",
            "Floor each UTC timestamp to midnight; these midnight values are the grouping keys.",
            "Group the amount Series by those keys, sum each group, then sort the date index. This avoids changing the input DataFrame.",
        ],
        "trace": "2026-01-02 00:30 at +09:00 is 2026-01-01 15:30 UTC. Together with 2026-01-01 16:00 UTC, both values group under 2026-01-01.",
        "practice": "Which UTC date key belongs to 2026-03-01T01:00:00+02:00?",
        "practice_answer": "2026-02-28 00:00:00+00:00, because the instant is 2026-02-28 23:00 UTC.",
    },
    "pandas-merge": {
        "steps": [
            "Orders are the left table and must all survive, so choose a left merge on user_id.",
            "Several orders may refer to one user, but each user should appear once. That relationship is many-to-one.",
            "Ask pandas to validate that relationship. If users has duplicate keys, the merge raises instead of silently multiplying order rows.",
        ],
        "trace": "An order for user 1 gets that user's email. An order for absent user 2 stays in the result with a missing email because the join is left. Duplicate user 1 rows fail validation.",
        "practice": "There are 4 orders and one matching user row per user. How many output rows should a left many-to-one merge have?",
        "practice_answer": "4 rows; missing user matches leave missing email values rather than dropping orders.",
    },
    "sklearn-preprocess": {
        "steps": [
            "Put imputation and scaling into one Pipeline so they run in the intended order and share learned training parameters.",
            "fit_transform(X_train) learns each training-column median, fills training gaps, learns means and scales, and returns transformed training data.",
            "Call transform(X_test) only. It applies the training medians and scales without learning anything from the test set.",
        ],
        "trace": "For training values [1, 3, missing], the median is 2 and the imputed training set is [1, 3, 2]. A missing test value is filled with 2, then scaled using training statistics; its standardized value is 0.",
        "practice": "Should you call fit_transform on X_test after fitting the pipeline on X_train?",
        "practice_answer": "No. Use prep.transform(X_test) so test data cannot change the learned preprocessing parameters.",
    },
    "fastapi-quantity": {
        "steps": [
            "Describe the expected JSON object with a Pydantic model; annotate quantity as an integer.",
            "Put Field(gt=0) on that field so validation rejects zero and negative values before the route runs.",
            "Register a POST route whose parameter is typed as the model. Return a dictionary using body.quantity; FastAPI serializes it as JSON.",
        ],
        "trace": "A request body {'quantity': 3} creates a validated model and returns {'quantity': 3}. A body with quantity 0 fails validation with HTTP 422 before the handler executes.",
        "practice": "What response status should a request with {'quantity': -1} receive under the described validation?",
        "practice_answer": "HTTP 422; the handler should not accept the invalid value.",
    },
    "test-boundaries": {
        "steps": [
            "Translate the rule into expected results: below 50 costs 5; at 50 or above costs 0.",
            "Test one value immediately below the cutoff, the cutoff itself, and one immediately above it.",
            "Use assert actual == expected so a wrong result stops the test with a clear failure at that case.",
        ],
        "trace": "49 is below 50 and expects 5. 50 is at the cutoff and expects 0. 51 is above it and also expects 0.",
        "practice": "What expected fee should you assert for shipping_fee(25)?",
        "practice_answer": "5",
    },
    "numpy-spread": {
        "steps": [
            "Check the sample size first: the n - 1 denominator is undefined for fewer than two observations, so raise ValueError there.",
            "NumPy computes variance with divisor n - ddof; choosing ddof=1 gives the requested n - 1 sample convention.",
            "Take the square root via np.std and convert its NumPy scalar to a regular Python float.",
        ],
        "trace": "For [1, 2, 3], the mean is 2 and squared deviations sum to 2. Dividing by n-1 = 2 gives variance 1 and standard deviation 1.",
        "practice": "What does sample_sd([5]) do, and why?",
        "practice_answer": "It raises ValueError because one observation is not enough for the requested n - 1 sample standard deviation.",
    },
    "scipy-binomial": {
        "steps": [
            "Map the story to the binomial parameters: there are 5 fixed trials, each fails with probability 0.1, and the requested count is exactly 2.",
            "Use the probability mass function because the question asks for one exact count. The counted event can be called a success for the calculation even though it is a failure in the story.",
            "Pass 2 as k, 5 as n, and 0.1 as p. Do not use the cumulative distribution function, which would include several counts.",
        ],
        "trace": "binom.pmf(2, n=5, p=0.1) is 0.0729, or 7.29%. It is the probability of exactly two failures, not at most two.",
        "practice": "Which function call asks for exactly one failure in the same five requests?",
        "practice_answer": "binom.pmf(1, n=5, p=0.1)",
    },
    "numpy-logloss": {
        "steps": [
            "Convert labels and probabilities to NumPy arrays so arithmetic and logarithms operate element by element.",
            "For each example, use -log(p) when the label is 1 and -log(1-p) when the label is 0. The combined formula selects the correct term using y.",
            "Average the individual losses, then return a Python float. The prompt guarantees matching nonempty arrays and probabilities strictly between zero and one.",
        ],
        "trace": "For label 1 with p=0.8, loss is -log(0.8) ≈ 0.223. For label 0 with p=0.2, loss is -log(0.8) ≈ 0.223. Their mean is ≈ 0.223.",
        "practice": "For a positive label y=1 with predicted probability p=0.1, is the loss small or large, and what is its formula?",
        "practice_answer": "Large: -log(0.1) ≈ 2.303. A confident low probability for the true class is strongly penalized.",
    },
}
