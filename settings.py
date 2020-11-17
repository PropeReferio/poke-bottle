from dotenv import load_dotenv
load_dotenv()

import os
favorite_poke = os.getenv("FAVORITE")

print(favorite_poke)