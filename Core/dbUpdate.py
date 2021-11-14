import json
from replit import db

def dbUpdate(admin, nmcmanager, developer):
  if (admin or nmcmanager or developer):
      roninDb = json.load(open("Database-ronin.json"))
      filtersDb = json.load(open("Database-filters.json"))
      db.set_bulk({
          "roninAdd": roninDb["roninAdd"],
          "filters": filtersDb["filters"]
      })
      print('database updated')