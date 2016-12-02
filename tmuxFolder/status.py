import time



out = ""

sep = "#[fg=colour0,bg=default] "


out += "#[fg=colour0,bg=green]" + (time.strftime("%d-%m-%y"))

out += sep

out += "#[fg=colour0,bg=green]" + (time.strftime("%H:%M"))

print(out)
