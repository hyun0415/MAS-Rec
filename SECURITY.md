# Security notes

## Credentials

- Never commit Hugging Face, GitHub, cloud, or experiment-tracking tokens.
- Use environment variables or a local `.env` file that remains ignored by Git.
- If a token has ever appeared in a notebook or commit, revoke it and issue a new one. Deleting the visible line is not sufficient because Git history and notebook outputs may retain it.

The notebooks in this archive were cleaned to remove embedded Hugging Face token literals and stored outputs before the first repository commit.

