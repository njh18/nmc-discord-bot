import json
from replit import db

def dbUpdate(roles):
  permissions = ['admin', 'nmcmanager', 'developer', 'staff']
  if (any(role in permissions for role in roles)):
      roninDb = json.load(open("Database-ronin.json"))
      filtersDb = json.load(open("Database-filters.json"))
      db.set_bulk({
          "roninAdd": roninDb["roninAdd"],
          "filters": filtersDb["filters"]
      })
      print('database updated')