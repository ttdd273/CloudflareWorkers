# Cloudflare Workers

This is a sample repository to setup GitHub Action to deploy Cloudflare Workers.

## Git 
- This is a really useful doc for denoting how to stop typing in your password every time you Git push.
- The issue comes from the fact that you need to add the key to `ssh-agent` or else it will forget about the password
- [Link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux)

Or if it's a local setup, we can get around it by doing this:
- `eval "$(ssh-agent -s)"`
- `ssh-add ~/.ssh/id_ed25519`