import os

# Pega o caminho da pasta onde o arquivo constants.py está (a pasta tests/)
TEST_PATH = os.path.dirname(__file__)

# Junta o caminho da pasta + assets + people.csv
# Resultado final será algo como: /home/devgege/Documentos
# /dundie-rewards/tests/assets/people.csv
PEOPLE_FILE = os.path.join(TEST_PATH, "assets", "people.csv")
