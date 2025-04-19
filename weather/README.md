# This the a weather forecast MCP server.
This server will connect the claude llm to get the real-time forecast of the city metioned.

## tools used
- python3.12
- Accuweather API
- claude desktop

## To run the server
- starting setup 
![initial steup](/weather/initial_setup.png)
- you can get a Accuweather api here [weather API](https://developer.accuweather.com/)
- export the "ACCUWEATHER_API_KEY" in the terminal.
- create .env file and put the api key in it.
- add this snippet to claude_desktop_config.json
```
{
    "mcpServers": {
        "weather": {
            "command": "uv",
            "args": [
                "run", 
    "--with", 
    "mcp[cli]", 
    "mcp", 
    "run", "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather/main.py" ]
        }
    }
}
```
- make sure to save the files and open/restart the claude desktop
- ask a city's weather


## Errors encountered
1. "Server transport closed unexpectedly, this is likely due to the process exiting early. If you are developing this MCP server you can add output to stderr (i.e. `console.error('...')` in JavaScript, `print('...', file=sys.stderr)` in python) and it will appear in this log.
2025-04-19T17:46:10.145Z [weather] [error] Server disconnected. For troubleshooting guidance, please visit our [debugging documentation](https://modelcontextprotocol.io/docs/tools/debugging) {"context":"connection"}"
sol:- create symlink "sudo ln -s $(which uv) /usr/local/bin/uv"