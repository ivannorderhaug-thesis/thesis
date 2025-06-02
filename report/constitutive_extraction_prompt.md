### Task
Your task is to extract components from a constitutive statement at the IG Core level using Institutional Grammar 2.0. 

### Context
A statement is constitutive if and only if it contains:
- **E (Constituted Entity)**: the institutional object, role, or concept being defined or modified
- **F (Constitutive Function)**: the action or relational expression that defines, composes, or modifies E
- **Context**: at least one of the following must be present:
  - **Cac (Activation Condition)**
  - **Cex (Execution Constraint)**

If no context is explicitly provided, assume the default interpretation that the statement applies "under all conditions" and with "no execution constraints." However, do not extract these defaults as components. Only extract Cac or Cex if they are explicitly expressed.

All other components are optional but must be extracted if explicitly present.

#### Definitions
**E (Constituted Entity)**: The entity (individual, role, object, or concept) introduced, defined, or modified by the Constitutive Function (F) within the institutional setting.
**E,p (Constituted Entity Properties)**: Descriptive, classifying, or qualifying characteristics (adjectives, adjectival phrases, or clauses) that specify or narrow the scope of the Constituted Entity (E).
**M (Modal)**: An epistemic operator expressing necessity, possibility, or prohibition of the Constitutive Function (F) and its institutional effect. Examples include “shall,” “must,” “may,” or “must not.”
**F (Constitutive Function)**: The verb or phrase that introduces, defines, modifies, or composes the Constituted Entity (E). This may include identity statements (e.g., “is”), compositional verbs (e.g., “consists of”), or other definitional markers (e.g., “constitutes,” “means”).
**P (Constituting Properties)**: The elements (actors, roles, objects, features, or conditions) that define, compose, or qualify the Constituted Entity (E) through the action of F.
**P,p (Constituting Properties Properties)**: Descriptive, classifying, or qualifying characteristics that specify or narrow the scope of individual Constituting Properties (P).
**Cac (Activation Condition)**: Clauses that describe external conditions, events, or circumstances that trigger the applicability of the institutional statement. These may be temporal, spatial, or situational in nature. Typical indicators include words such as “when,” “upon,” “after,” “before,” “in,” “at,” or “if.”
**Cex (Execution Constraint)**: Clauses or phrases that specify internal constraints on how the Aim is to be carried out once the institutional statement is active. These constraints may pertain to manner, timing, location, rationale, purpose, or affected parties, depending on the type of institution being expressed.
**O (Or Else)**: The consequences that follow from failure to act as specified, or from acting in contradiction to the institutional statement. These consequences may include sanctions, penalties, or payoffs such as fines, revocation of privileges, or denial of benefits.

#### Rules
- Extract only those components that are explicitly stated in the input. Do not infer or fabricate.
- Each phrase must be assigned to one component only. Do not duplicate or reuse across multiple components.
- Use semantic function, not sentence position, to identify components.
- Extract **P,p** only when they provide clear, distinguishable qualification of P.
- If the statement contains multiple instances of the same component type (e.g., multiple P or P,p values), extract each separately.
- If components share arguments or modifiers (e.g., multiple P instances linked to one E), extract shared elements only once unless their semantic roles differ.
- Do not separate embedded modifiers from the nouns they define if doing so would result in an ungrammatical or misleading phrase.

### Return Format (Exact JSON)
{"ComponentSymbol":["literals",...],"ComponentSymbol":["literals",...],"ComponentSymbol":["literals",...],...}
### Examples
<user_query id="example-1">
No reimbursement shall be made for disallowed costs.
</user_query>

<assistant_response id="example-1">
{"E":["reimbursement"],"M":["shall"],"F":["be made"],"P,p":["disallowed"],"P":["costs"]}
</assistant_response>

<user_query id="example-2">
Approval of an application for a loan by the Board constitutes a preliminary decision under the MOA
</user_query>

<assistant_response id="example-2">
{"E":["Board Approval"],"E,p":["of an application for a loan by the Board"],"F":["constitutes"],"P,p":["preliminary"],"P":["decision"],"Cex":["under the MOA"]}
</assistant_response>

<user_query id="example-3">
Each agreement will contain a provision requiring the Borrower to comply with all applicable provisions of the Watershed Regulations.
</user_query>

<assistant_response id="example-3">
{"E,p":["Each"],"E":["agreement"],"M":["will"],"F":["contain"],"P":["provision"],"P,p":["requiring the Borrower to comply with all applicable provisions of the Watershed Regulations"]}
</assistant_response>

<user_query id="example-4">
Notwithstanding Section 10231.5 of the Government Code, the requirement for submitting a report imposed under paragraph (1) is inoperative on January 1, 2021.
</user_query>

<assistant_response id="example-4">
{"Cex":["Notwithstanding Section 10231.5 of the Government Code"],"E":["requirement"],"E,p":["for submitting a report imposed under paragraph 1"],"F":["is"],"P":["inoperative"],"Cac":["on January 1, 2021"]}
</assistant_response>

<user_query id="example-5">
Subject to this section, the requirements of this article apply to an electrical corporation that as of January 1, 2010, had 60,000 or fewer customer accounts in California.
</user_query>

<assistant_response id="example-5">
{"Cex":["Subject to this section"],"E":["requirements"],"E,p":["of this article"],"F":["apply to"],"P":["an electrical corporation"],"P,p":["that as of January 1, 2010, had <=60,000 customer accounts in California"]}
</assistant_response>
