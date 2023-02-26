# Não gerar __pycache__
import sys
sys.dont_write_bytecode = True

from shop import app

if __name__ == "__main__":
    app.run(debug=True)