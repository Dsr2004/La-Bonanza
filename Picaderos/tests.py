from datetime import datetime

inicio = datetime.strptime("2022-10-01", "%Y-%M-%d").date()
fin = datetime.strptime("2022-10-31", "%Y-%M-%d").date()

print(fin-inicio)