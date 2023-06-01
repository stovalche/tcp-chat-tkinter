def outputframe(message, user):
  hor_line = "\u2500"

  term_size = 60
  header = term_size - 2 - len(user)
  if header % 2 == 1:
    half_left = (header + 1) / 2
    le_left = hor_line * int(half_left)
    le_right = hor_line * int(header - half_left)
  else:
    half_left = header / 2
    le_left = hor_line * int(half_left)
    le_right = hor_line * int(header - half_left)

  if user != "":
    head_string = hor_line + "\u257C " + user + " \u257E" + le_left + le_right + hor_line
  else:
    head_string = hor_line + hor_line + hor_line + le_left + le_right + hor_line
  foot_string = hor_line + (hor_line * term_size) + hor_line
  term_size = int(term_size * 9 / 6 + 1)
  sep_string = '-' + ('-' * term_size) + '-'
  value = f"{head_string}\n{message}{foot_string}\n{sep_string}\n"

  return value
