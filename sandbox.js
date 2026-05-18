import asyncio
from dotenv import load_dotenv
from vercel.sandbox import AsyncSandbox as Sandbox

load_dotenv('.env.local')

async def main() -> None:
    sandbox = await Sandbox.create()

    cmd = await sandbox.run_command(
        "echo",
        ["Hello from Vercel Sandbox!"]
    )
    stdout = await cmd.stdout()
    print(f"Message: {stdout}")

    await sandbox.stop()

if __name__ == "__main__":
    asyncio.run(main())
