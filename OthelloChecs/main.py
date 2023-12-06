import asyncio
from OthelloPackage.Controller import Controller

async def main():  
   await Controller().Start_Game()

if __name__ == "__main__":
   asyncio.run(main())
