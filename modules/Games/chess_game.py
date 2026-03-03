import random

try:
    import chess
except Exception:
    chess = None


def _print_board(board):
    print("\n" + str(board) + "\n")
    print("Enter a move in UCI like: e2e4 (or: quit)")


def _parse_move(board, text):
    text = (text or "").strip().lower()
    if not text:
        return None

    if text in ["q", "quit", "exit"]:
        return "quit"

    try:
        move = chess.Move.from_uci(text)
        if move in board.legal_moves:
            return move
    except Exception:
        pass

    try:
        move = board.parse_san(text)
        if move in board.legal_moves:
            return move
    except Exception:
        pass

    return None


def play_chess():
    if chess is None:
        print("Chess module not available. Install: python-chess")
        return

    board = chess.Board()

    print("\nDraco Chess (Terminal)\n")
    print("You are White. Draco is Black.\n")

    while True:
        if board.is_game_over():
            result = board.result()
            print("Game over:", result)
            print(board.outcome())
            return

        if board.turn == chess.WHITE:
            _print_board(board)
            user_in = input("Your move: ")
            parsed = _parse_move(board, user_in)
            if parsed == "quit":
                print("Exiting chess.")
                return
            if parsed is None:
                print("Invalid move. Try again.")
                continue
            board.push(parsed)
        else:
            legal = list(board.legal_moves)
            if not legal:
                continue
            move = random.choice(legal)
            board.push(move)
            print(f"Draco played: {move.uci()}")
