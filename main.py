import inotify.adapters
import os

def _main():
    paths = []
    inot = inotify.adapters.Inotify()
    inot.add_watch("/bin")
    inot.add_watch("/usr/lib64/discord/Discord")
    addSimlinks("/usr/bin", paths)
    addSimlinks("/bin", paths)

    paths = list(set(paths))
    x = 0
    for p in paths:
        x+=1
        inot.add_watch(p)
    print("start watch")
    programsRun = []
    with open("history", "r") as file:
        for i in file.readlines():
            programsRun.append(i.strip("\n"))
    if programsRun.count('') > 0:
        programsRun.remove('')
    try:
        for event in inot.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if filename.count("so") > 0:
                continue
            if type_names.count("IN_OPEN") > 0 and os.access(path, os.X_OK):
                #print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names)
                programsRun.append(filename)
    except:
        programsRun = list(set(programsRun))
        open("history", "w").close()
        with open("history", "a") as file:
            for i in programsRun:
                file.write(i+"\n")
        print("program exited, data saved")

def addSimlinks(dir, paths):
    for i in os.listdir(dir):
        if os.path.islink(os.path.join(dir,i)):
            ln = os.path.realpath(os.path.join(dir,i))
            if "alternatives" in ln:
                continue
            ln = os.path.abspath(os.path.join(ln, ".."))
            paths.append(ln)
if __name__ == '__main__':
    _main()
