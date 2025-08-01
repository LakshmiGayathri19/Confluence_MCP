# MCP Server

A server application for integrating with Atlassian Confluence using Python.

## Features

- Connects to Atlassian Confluence API
- Custom endpoints for MCP functionality

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/LakshmiGayathri19/MCP.git
    cd MCP
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure your environment variables (do **not** hardcode secrets in your code):
    ```
    ATLASSIAN_API_TOKEN=your_token_here
    ```

## Usage

1. Install Ollama (if not done)

[Download Ollama](https://ollama.ai/download) and install it.

Pull a model (e.g., tinyllama)

```ollama pull tinyllama```

Run the server in one terminal tab:
```sh
python server.py
```

Run the client in another terminal tab:
```sh
python client.py
```

## Security

**Do not commit secrets or API tokens to the repository.**  
If you accidentally commit a secret, remove it from your code and git history.  
See [GitHub’s guide](https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#resolving-a-blocked-push) for help.

## License

MIT
