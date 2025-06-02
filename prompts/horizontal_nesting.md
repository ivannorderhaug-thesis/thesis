### Task
You are to analyze an IG 2.0 coded output and revise it so that all logical relationships between literals within each component are explicit, following IG 2.0 horizontal nesting principles. Apply standard logical operators as described below, and ensure consistency and full preservation of the original clauses.

### Guidelines

1. Identification
For each component, identify whether multiple literal segments exist that are logically linked (e.g., via ‘and’, ‘or’, ‘either’, ‘both’, or punctuation representing lists of alternatives/co-requirements).

2. Operator Selection
- Use [AND] if all elements jointly apply (conjunction).
- Use [OR] for inclusive disjunction (any may apply).
- Use [XOR] when exactly one applies (exclusive or, either/or).

3. Parenthetical Grouping
- When multiple literals within a component are logically connected, group them in parentheses and insert the standardized logical operator inside.
- Only include the minimal clause set directly linked by the conjunction/disjunction inside the parentheses.
- Do not group elements of different component types within the same parentheses.

4. Single Values
- If a component contains only one literal, leave it unmodified (no parentheses or operator).

5. Full Preservation
- Always include the complete literal of each clause, phrase, or segment from the original unless you are only adjusting operator format. Do not summarize, omit, or condense.
- If the literal contains conjunctions/disjunctions not relevant to logic (e.g., natural language and not connecting distinct ideas), leave as-is.

### Return Format (Exact JSON)
Respond with the revised components in this exact JSON structure:
{"ComponentSymbol":["string",...],"ComponentSymbol":["string",...], ...}

Validation:
- Each entry in the JSON must be a single string per component that fully expresses the logical structure, preserving all original phrases and order.
- Standardize all quotation marks to double quotes (").
- Never insert operators as their own array elements—operators must appear within the string value, linking literals inside parentheses

### Examples
<user_query id="example-1">
Once admitted to university, every student must attend and pass obligatory classes Monday through Friday from 8AM to 4PM, or they will be expelled.
{"A,p":["every"],"A":["student"],"Cac":["Once admitted to university"],"D":["must"],"I":["attend","pass"],"Bdir":["classes"],"Bdir,p":["obligatory"],"Cex":["Monday through Friday from 8AM to 4PM"],"O":["they will be expelled"]}
</user_query>

<assistant_response id="example-1">
{"A,p":["every"],"A":["student"],"Cac":["Once admitted to university"],"D":["must"],"I":["attend [AND] pass"],"Bdir":["classes"],"Bdir,p":["obligatory"],"Cex":["Monday through Friday from 8AM to 4PM"],"O":["they will be expelled"]}
</assistant_response>

<user_query id="example-2">
Agencies must approve, deny, or defer requests.
{"I":["approve, deny, or defer"],"A":["agencies"],"Bdir":["requests"],"D":["must"]}
</user_query>

<assistant_response id="example-2">
{"I":["approve [XOR] deny [XOR] defer"],"A":["agencies"],"Bdir":["requests"],"D":["must"]}
</assistant_response>
