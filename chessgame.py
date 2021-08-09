import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io
import time
from datetime import date


SECONDS_PER_MOVE = 3

STOCKFISH_EXECUTABLE = "/root/stockfish/stockfish_14_linux_x64/stockfish_14_x64"
LC0_EXECUTABLE = "/root/lc0/build/release/lc0"

leelaEngine = chess.engine.SimpleEngine.popen_uci(LC0_EXECUTABLE, timeout=None)

stockfishEngine = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_EXECUTABLE, timeout=None
)

print("loading engines...")
time.sleep(3)
print("starting game")


stockfishEngine.configure({"Skill Level": 8})

myBoard = chess.Board()
myGame = chess.pgn.Game()
node = myGame

while myBoard.is_game_over() == False:
    if myBoard.turn:
        print("white's (stockfish) turn")
        myMove = stockfishEngine.play(
            myBoard, chess.engine.Limit(time=SECONDS_PER_MOVE)
        )
    else:
        print("black's (LC0) turn")
        myMove = leelaEngine.play(myBoard, chess.engine.Limit(time=SECONDS_PER_MOVE))
    node = node.add_variation(myMove.move)
    myBoard.push(myMove.move)
    print("move:", myMove.move)
    print(myBoard)
    print()

print("game over!")
print()

myGame.headers["Event"] = "PYTHON CHESS EXAMPLE"
myGame.headers["White"] = "Stockfish"
myGame.headers["Black"] = "Leela (LC0)"
myGame.headers["Result"] = myBoard.result()
myGame.headers["Site"] = "https://github.com/mattwhite180/chess-example"
myGame.headers["Date"] = date.today()

print(str(myGame))
stockfishEngine.quit()
leelaEngine.quit()
