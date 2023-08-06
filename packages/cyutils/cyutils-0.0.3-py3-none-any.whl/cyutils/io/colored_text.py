colors = {
  "standard"   :  "\033[0m",
  "black"   :  "\033[30m",
  "red"     :  "\033[31m",
  "green"   :  "\033[32m",
  "yellow"  :  "\033[33m",
  "blue"    :  "\033[34m",
  "magenta" :  "\033[35m",
  "cyan"    :  "\033[36m",
  "white"   :  "\033[37m"
}

def print_colored(text, color):
  print(colors[color] + text + colors["standard"])