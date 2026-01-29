from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Deploy-server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a+b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")