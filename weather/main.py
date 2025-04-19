from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP



mcp = FastMCP("weather")



def main():
    print("Hello from weather!")


if __name__ == "__main__":
    main()
