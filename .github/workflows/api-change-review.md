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

Write for a technical writer who needs to quickly understand what changed and begin a documentation review.

Start with a short overall summary and counts of new, modified, and removed endpoints.

For each changed endpoint, summarize:
- what changed
- what the endpoint does
- what it accepts
- what it returns
- important response status codes

Call out potentially breaking changes separately.

End with specific documentation areas the writer should review, such as endpoint reference pages, request examples, response examples,
field descriptions, authentication documentation, or error-response documentation when implicated by the change.

Do not write or modify the documentation itself. The purpose of this report is to give the technical writer enough context to begin their
documentation review.

If there are no meaningful API contract changes, say so clearly.

Do not edit repository documentation or other source files.

Use the configured `add-comment` safe output for the requested result. Do not make direct GitHub writes.

If the evidence is incomplete, do not publish a speculative compatibility assessment.