import inotify.adapters
import os

def main():
  configPath = "/home/oliver/.config"
  print("starting watch")
  inot = inotify.adapters.Inotify()
  inot.add_watch(configPath)
  openedConfigFiles = []
  try:
    for event in inot.event_gen(yield_nones=False):
      (_, type_names, path, filename) = event
      if filename == "" or filename == "\n":
        continue
      else:
        print(filename)
        openedConfigFiles.append(filename)
  except:
    print("program exited")
    with open("untouchedFiles", "r") as f:
      for i in f.readlines():
        openedConfigFiles.append(i.strip("\n"))
    openedConfigFiles = list(set(openedConfigFiles))
    open("untouchedFiles", "w").close()
    with open("untouchedFiles", "w") as f:
      for i in openedConfigFiles:
       f.write(i+"\n")
    print("------------Untouched files------------")
    files = os.listdir(configPath)
    for i in files:
      if i in openedConfigFiles:
        pass
      else:
        print(i) 
      
main()
