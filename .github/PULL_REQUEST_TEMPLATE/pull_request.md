name: "Pull Request"
about: "Use this template when submitting a PR"
title: "Issue #<number> - Short description"
labels: ["pull request"]
assignees: []

body:
  - type: input
    id: issue_reference
    attributes:
      label: "Related Issue"
      description: "Reference the issue number (e.g., #42) this PR closes or relates to"
      placeholder: "e.g., Closes #42"
    validations:
      required: true

  - type: textarea
    id: summary
    attributes:
      label: "PR Summary"
      description: "Provide a short summary of the changes included in this PR"
      placeholder: "Add user profile picture feature..."
    validations:
      required: true

  - type: textarea
    id: changes
    attributes:
      label: "Detailed Changes"
      description: "List major changes made (new files, updated files, removed files, etc.)"
      placeholder: "- Added UserProfile model\n- Updated views.py\n- Added tests"
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: "Checklist"
      options:
        - label: "Code follows PEP 8"
          required: true
        - label: "Tests added/updated for all changes"
          required: true
        - label: "All tests pass with pytest"
          required: true
        - label: "Documentation updated if needed"
          required: True
