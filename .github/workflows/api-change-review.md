---
name: API Change Review
description: Summarize API contract changes in schema.yml for documentation review.
intent: Help technical writers identify API documentation that may need review after an API schema change.
on:
  pull_request:
    branches: [main]
    types: [opened, reopened, synchronize]
    paths:
      - schema.yml
permissions:
  contents: read
  issues: read
  pull-requests: read
strict: true
tools:
  github:
    mode: gh-proxy
    toolsets: [default]
engine:
  id: copilot
  model: gpt-5.4
steps:
  - name: Prepare merge and main schemas
    env:
      GH_TOKEN: ${{ github.token }}
      MERGE_SHA: ${{ github.sha }}
    run: |
      set -euo pipefail
      mkdir -p /tmp/gh-aw/agent/api-schema-diff 
      git show "${MERGE_SHA}:schema.yml" > /tmp/gh-aw/agent/api-schema-diff/merge-commit-schema.yml
      gh api "repos/${GITHUB_REPOSITORY}/contents/schema.yml?ref=main" --jq '.content' | base64 --decode > /tmp/gh-aw/agent/api-schema-diff/main-schema.yml
safe-outputs:
  add-comment:
    target: triggering
    max: 1
---

# API Change Review

Compare the OpenAPI contract in the pull request's GitHub merge ref (`/tmp/gh-aw/agent/api-schema-diff/merge-commit-schema.yml`) with the current `main` version (`/tmp/gh-aw/agent/api-schema-diff/main-schema.yml`). The deterministic preparation step has already retrieved `main`; do not substitute the PR head branch or another baseline.

## Analysis

Analyze the API changes from the perspective of a technical writer.

Identify:

- New endpoints, including:
  - HTTP method and path
  - operation ID and summary, when available
  - what the endpoint does
  - what it accepts
  - what it returns
  - relevant response status codes

- Removed endpoints, including:
  - HTTP method and path
  - what the endpoint did

- Modified endpoints, focusing on changes that would matter to
  API documentation.

- New, removed, or meaningfully changed request and response fields.

- Changes to required fields or accepted values when they affect how
  the API should be documented.

- Potentially breaking changes when there is clear evidence in the
  OpenAPI contract. Distinguish facts shown by the schema from
  inferred client impact.

Do not produce a complete low-level OpenAPI diff.

Do not report changes to enum values, formats, nullability, media types, or individual schema constraints unless they are meaningful to
understanding or documenting the API.

Do not infer API behavior that is not represented in the OpenAPI contract.

If either schema cannot be read or parsed, call `report_incomplete` and explain what evidence is missing rather than guessing.

## Output

Post one concise, reader-friendly Markdown summary as a comment on the triggering PR.

Write for a technical writer who needs to quickly understand **what changed in the API and what documentation may need attention**.

Use this structure:

### API change summary

Start with one or two sentences summarizing the overall change and include counts of new, modified, and removed endpoints.

### What changed

For each endpoint with a meaningful documentation impact, provide:

- **Endpoint:** HTTP method and path
- **Change:** A plain-language summary of what changed
- **Documentation impact:** What a technical writer should review or update

Group related endpoint changes together when the same underlying API change affects multiple endpoints.

Do not provide a detailed description of endpoint behavior unless it is necessary to understand the change.

Do not list unchanged request parameters, response fields, media types, authentication requirements, or status codes.

Do not include operation IDs unless they are useful for distinguishing endpoints.

Do not include implementation-level details or low-level OpenAPI properties unless they are directly relevant to the documentation impact.

### Potentially breaking changes

If the contract contains a potentially breaking change, briefly explain:

- **What changed**
- **Why it may affect API consumers**

Clearly distinguish facts shown by the OpenAPI contract from inferred client impact.

Do not label a change as breaking unless the contract provides clear evidence.

### Documentation review

End with a short list of specific documentation areas the writer should review, such as:

- endpoint reference pages
- request or response examples
- parameter or field descriptions
- authentication documentation
- error-response documentation
- release notes or migration guidance

Only include documentation areas that are relevant to the changes identified.

Keep the overall comment concise. Prefer a high-level summary over exhaustive technical detail.

Do not write or modify the documentation itself.

If there are no meaningful API contract changes, say so clearly.

Do not edit repository documentation or other source files.

Use the configured `add-comment` safe output for the requested result. Do not make direct GitHub writes.

If the evidence is incomplete, do not publish a speculative compatibility assessment.