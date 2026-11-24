## ADDED Requirements

### Requirement: Every case gets a plain-words card

The report MUST show one card for each case, before the metric sections. The card MUST show the plain question as its title, the prompt as the models received it, and the sentence that says what a right answer does. Each of these comes from the frozen manifest of the iteration.

#### Scenario: Reader opens a report with labelled cases

- **WHEN** a reader who does not know the product opens the report of an iteration whose cases carry a question and an explanation
- **THEN** each case card shows the question, the quoted prompt, and the explanation

### Requirement: Card grid names what each answer did

Each card MUST show a grid with a row for the baseline, a row for each treatment, and one column for each model. Each cell MUST show a short label of what that answer did: green when every content check passed, red when a content check failed. A cell MUST NOT show a fraction.

#### Scenario: Baseline answer writes old code

- **WHEN** the baseline answer of one model fails the check that forbids old code
- **THEN** its cell shows the label of that check in red, and the treatment cell of the same model shows the pass label in green

### Requirement: Forbidden checks name the label first

The aggregator MUST give a run the pass label of its case when every content check passed. Otherwise it MUST take the fail label of a failed forbidden check before the fail label of a failed required check. A check without a fail label MUST give its own text. A word-count check MUST NOT pick the label.

#### Scenario: Answer fails a required and a forbidden check

- **WHEN** an answer misses a required pattern and also matches a forbidden one
- **THEN** its cell shows the fail label of the forbidden check

### Requirement: Cases without labels still render

The report MUST render a card for every case of a manifest that has no card fields. The card then takes the case name as its title and the check texts as its labels.

#### Scenario: Older iteration is aggregated again

- **WHEN** the aggregator runs on an iteration whose frozen manifest predates the card fields
- **THEN** the report shows one card for each case, titled by case name and labelled by check text

### Requirement: Check counts stay in the data and the details

The aggregate MUST keep the assertion counts and the result of every check for each run. Each card MUST list them for each run in a folded details section.

#### Scenario: Reader opens the check details

- **WHEN** a reader opens the check details of a card
- **THEN** each run shows its passed and total checks, and every check with its result and evidence

### Requirement: Card labels stay short

The manifest validator MUST reject a pass label or a fail label longer than four words, and an empty question or explanation. A grid cell then holds one short label.

#### Scenario: Author writes a long pass label

- **WHEN** a manifest has a pass label of five words
- **THEN** the validator rejects the manifest before the first provider call and names the field
