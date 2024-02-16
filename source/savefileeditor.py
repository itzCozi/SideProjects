import json

# EDITS CRUELTY SQUAD SAVE FILE (FOR CHEATS!!)


def format_save(path):
  with open(path, "r") as f_in:
    save_data = f_in.read()

  savefile_json = json.loads(save_data)
  formatted = json.dumps(savefile_json, indent=2)

  with open(path, "w") as f_out:
    f_out.write(formatted)


def update_values(savefile_path, updates):
  with open(savefile_path, "r") as file:
    savefile_data = file.read()

  savefile_json = json.loads(savefile_data)

  for key, value in updates.items():
    if key in savefile_json:
      savefile_json[key] = value
    else:
      print(f"Warning: Key '{key}' not found in the savefile.")

  with open(savefile_path, "w") as file:
    json.dump(savefile_json, file, indent=4)

updates = {
  "money": 69420
}
update_values("C:/Users/coope/AppData/Roaming/Godot/app_userdata/Cruelty Squad/savegame.save", updates)
