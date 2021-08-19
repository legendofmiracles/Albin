import chess
import discord
from discord.ext import commands

from config import TOKEN

bot = commands.Bot(command_prefix='&')

isBoard = False
game = []

@bot.command()
async def start(ctx, user: discord.Member = None):
    global board
    global isBoard
    global white_id
    global black_id

    if not user:
        await ctx.channel.send("Tag a user to play.")
        return

    white_id = ctx.author.id
    black_id = user.id

    isBoard = True 
    board = chess.Board()
    msg = f"White: {ctx.message.author.mention}\nBlack: {user.mention}"

    await ctx.channel.send("Board was created.")
    await ctx.channel.send(msg)

@start.error
async def start_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.channel.send("User not found.")


@bot.command()
async def move(ctx, arg):
    if isBoard: 
        try:
            author_id = ctx.author.id

            if board.turn and author_id == white_id: # board.turn returns True if 
                                                     # white to move and false otherwise
                pass
            elif not board.turn and author_id == black_id:
                pass
            else:
                await ctx.channel.send("You can't move for other player.")
                return

            board.push_san(arg)

        except ValueError:
            await ctx.channel.send("Invalid move.")
            return

        if board.is_game_over():
            await ctx.channel.send(board.outcome(claim_draw=True))
            await end(ctx)

        elif board.is_check():
            await ctx.channel.send("Check.")
        else:
            await ctx.message.add_reaction("✅")

        game.append(arg)

    else:
        await ctx.channel.send("Board wasn't created. Use &start to create.")


@bot.command()
async def log(ctx):
    if len(game) == 0:
        await ctx.channel.send("No piece was moved yet.")
        return

    result = ""

    n = 1
    for i in range(len(game)):
        if i % 2: 
            result += " " + game[i] + "\n"
        else:
            result += str(n) + ". " + game[i]

        n += 1

    await ctx.channel.send("```" + str(result) + "```")
    

@bot.command()
async def end(ctx):
    global board
    global game

    await ctx.channel.send("```" + str(board) + "```")
    await ctx.channel.send("Game ended. Board is reset.")
    
    game = [] 
    board.reset()


bot.run(TOKEN)
