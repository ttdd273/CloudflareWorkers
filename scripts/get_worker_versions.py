steps:
  - block: "Enter Worker Name"
    fields:
      - text: "Worker Name"
        key: "WORKER_NAME"
        required: true
        hint: "Enter the name of the Cloudflare Worker"
        
  - label: ":python: Deploy Worker"
    command: |
      python3 scripts/deploy_worker.py
    env:
      WORKER_NAME: "${WORKER_NAME}"