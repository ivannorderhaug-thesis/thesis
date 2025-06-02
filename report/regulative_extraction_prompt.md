### Task
Your task is to extract components from a regulative statement at the IG Core level using Institutional Grammar 2.0. 

### Context
A statement is regulative if and only if it contains:
- **Attribute (A)**: the actor expected to carry out the action
- **Aim (I)**: the institutionally regulated action
- **Context**: at least one of the following must be present:
  - **Cac (Activation Condition)**
  - **Cex (Execution Constraint)**

If no context is explicitly provided, the statement is still considered regulative by default interpretation: "under all conditions" and "no execution constraints." However, **do not extract** default interpretations as components. Only include Cac or Cex if they are explicitly expressed in the statement.

All other components are optional but should be extracted if they are explicitly present.

#### Definitions
**A (Attribute)**: The actor (individual, corporate entity, or organization) expected to carry out or refrain from the action specified by the Aim (I).
**A,p (Attribute Properties)**: Any descriptive, qualifying, or limiting characteristics, expressed as adjectives, adjectival phrases, or clauses. These must explicitly modify or narrow the scope of the Attribute (A), and may include inherent traits, stable role-based features, or situational qualifiers.
**I (Aim)**: The action verb or verb phrase (for example, “submit,” “cast,” “carry out,” “comply with,” “review,” or “approve”) that describes an institutionally regulated activity or behavior. The Aim is central to the statement, as it is what can be complied with or violated.
**Bdir (Direct Object)**: The animate, inanimate, or abstract element directly acted upon by the Aim. This object may be a physical entity, a conceptual entity, or any specifically identifiable target that experiences the primary impact of the Aim.
**Bdir,p (Direct Object Properties)**: Any descriptive, qualifying, or conditional characteristics that identify inherent, situational, or role-relevant features of the Direct Object (Bdir). These are expressed as adjectives, adjectival phrases, or clauses.
**Bind (Indirect Object)**: The animate, inanimate, or abstract element that is indirectly affected by, or receives the outcome of, applying the Aim (I) to the Direct Object (Bdir). The Indirect Object is used when the involvement or effect is secondary.
**Bind,p (Indirect Object Properties)**: Any descriptive, qualifying, or conditional characteristics that explicitly define the features of the Indirect Object.
**D (Deontic)**: A modal verb or explicit directive that indicates obligation, permission, or prohibition. Examples include “shall,” “must,” “may,” “shall not,” “must not,” “may not,” “is required to,” or “is permitted to.” The Deontic conveys the normative force of the statement.
**Cac (Activation Condition)**: Clauses that describe external conditions, events, or circumstances that trigger the applicability of the institutional statement. These may be temporal, spatial, or situational in nature. Typical indicators include words such as “when,” “upon,” “after,” “before,” “in,” “at,” or “if.”
**Cex (Execution Constraint)**: Clauses or phrases that specify internal constraints on how the Aim is to be carried out once the institutional statement is active. These constraints may pertain to manner, timing, location, rationale, purpose, or affected parties, depending on the type of institution being expressed.
**O (Or Else)**: The consequences that follow from failure to act as specified, or from acting in contradiction to the institutional statement. These consequences may include sanctions, penalties, or payoffs such as fines, revocation of privileges, or denial of benefits.

#### Rules
- Extract components **only when explicitly stated**. Do not infer or fabricate any part of the statement.
- Assign each literal phrase to a **single component** only. Do not duplicate or reuse across components.
- Use **semantic function** to identify components. Do not rely on position or surface syntax.
- **Omit determiners** ("the," "a," etc.) unless they are part of a proper noun or official title.
- Extract **Bind** only if a **Bdir** is also present in the statement.
- Extract **Deontic (D)** only when it modifies an **Aim (I)**. D cannot appear independently.
- If a statement includes **multiple instances** of a component type (e.g., two distinct Aims or multiple Activation Conditions), extract each separately.
- If components (e.g., multiple Aims) share modifiers or objects, extract shared elements once unless their semantic roles differ.
- Detachable descriptors (e.g., "obligatory classes") should be extracted as property components (A,p, Bdir,p, Bind,p).
- Do not extract embedded descriptors separately if this would fragment the phrase or alter its meaning.

### Return Format (Exact JSON)
{"ComponentSymbol":["literals",...],"ComponentSymbol":["literals",...],"ComponentSymbol":["literals",...],...}
### Examples
<user_query id="example-1">
Upon signing a memorandum of understanding with a private contractor to serve as the oversight authority, the compliance officer must review the contractor’s operational plan within 45 days.
</user_query>

<assistant_response id="example-1">
{"Cac":["Upon signing a memorandum of understanding with a private contractor to serve as the oversight authority"],"A":["officer"],"A,p":["compliance"],"D":["must"],"I":["review"],"Bdir":["contractor’s operational plan"],"Cex":["within 45 days"]}
</assistant_response>

<user_query id="example-2">
Executive committee encourages civic participation.
</user_query>

<assistant_response id="example-2">
{"A":["Executive committee"],"I":["encourages"],"Bdir,p":["civic"],"Bdir":["participation"]}
</assistant_response>

<user_query id="example-3">
The council shall authorize a logistics company to reclaim validated transportation surcharge costs via approved invoicing procedures.
</user_query>

<assistant_response id="example-3">
{"A":["council"],"D":["shall"],"I":["authorize"],"Bdir":["logistics company"],"Bdir,p":["to reclaim validated transportation surcharge costs via approved invoicing procedures"]}
</assistant_response>

<user_query id="example-4">
Once admitted to university, every student must attend obligatory classes Monday through Friday from 8AM to 4PM, or they will be expelled.
</user_query>

<assistant_response id="example-4">
{"A,p":["every"],"A":["student"],"Cac":["Once admitted to university"],"D":["must"],"I":["attend"],"Bdir":["classes"],"Bdir,p":["obligatory"],"Cex":["Monday through Friday from 8AM to 4PM"],"O":["they will be expelled"]}
</assistant_response>

<user_query id="example-5">
Supervisors shall provide constructive feedback to junior staff.
</user_query>

<assistant_response id="example-5">
{"I":["provide"],"A":["Supervisors"],"Bdir,p":["constructive"],"Bdir":["feedback"],"Bind":["staff"],"Bind,p":["junior"],"D":["shall"]}
</assistant_response>

<user_query id="example-6">
The commission shall, by March 1, 2008, transfer to electrical corporations serving customers subject to the renewable energy public goods charge the remaining unencumbered funds in the New Renewable Resources Account.  
</user_query>

<assistant_response id="example-6">
{"A":["commission"],"D":["shall"],"Cex":["by March 1, 2008"],"I":["transfer"],"Bdir":["remaining unencumbered funds"],"Bdir,p":["in the New Renewable Resources Account"],"Bind":["electrical corporations"],"Bind,p":["serving customers subject to the renewable energy public goods charge"]}
</assistant_response>

<user_query id="example-7">
Upon approval by CWC staff, CWC shall pay 50% of Eligible Costs to the applicant for Septic Maintenance.
</user_query>

<assistant_response id="example-7">
{"Cac":["Upon approval by CWC staff"],"A":["CWC"],"D":["shall"],"I":["pay"],"Bdir,p":["50%"],"Bdir":["Eligible Costs"],"Bind":["applicant"],"Cex":["for Septic Maintenance"]}
</assistant_response>

<user_query id="example-8">
Each licensed veterinarian must collect and report monthly to the County Health Department a summary of vaccinations administered according to Health Code Regulation 752.
</user_query >

<assistant_response id="example-8">
{"A,p":["Each","licensed"],"A":["veterinarian"],"D":["must"],"I":["collect","report"],"Cex":["monthly"],"Bind":["County Health Department"],"Bdir":["summary"],"Bdir,p":["of vaccinations administered according to Health Code Regulation 752"]}
</assistant_response>
